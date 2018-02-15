"""
Provides a tool for downloading and saving images from the daemon version
of the question generator (launched uing the --daemon command line).
"""

import aiohttp
import asyncio
import re
import zipfile
import os
import io
import requests
import time
import argparse
import json

class DaemonClient :
    def __init__(self, image_server_url, save_to_directory, verbose = False) :
        self.image_server_url = image_server_url
        self.save_to_directory = save_to_directory
        self.images_downloaded = 0
        self.http_session = None
        self.image_filename = 1
        self.verbose = verbose
        
        os.makedirs(save_to_directory, exist_ok=True)
        
    async def __init_http_sesssion(self) :
        self.http_session = aiohttp.ClientSession() 
        
    async def __download_image(self) :
        if self.http_session is None :
            await self.__init_http_sesssion()
            
        async with self.http_session.get(self.image_server_url) as response :
            if response.content_type == "application/zip" and response.status == 200 :
                self.__extract_files_from_zip(
                    io.BytesIO(await response.read()), response.headers)
                 
    def __extract_files_from_zip(self, zip_bytes_file_obj, headers) :   
        m = re.search('filename="(\d+\.zip)"', headers.get('Content-Disposition'))
        if m :
            zip_filename = m.group(1)
        else :
            raise Exception("Suspicious zip file - did not receive a filename in the header")

        with zipfile.ZipFile(zip_bytes_file_obj, 'r') as image_zip:
            zip_item_list = image_zip.infolist() 
            
            save_as_filename_map = self.__map_filenames(zip_item_list)
            
            for zip_item in zip_item_list :
                self.__extract_file(image_zip, zip_item, save_as_filename_map)
                        
        self.__update_file_counters() 
        
    def __map_filenames(self, zip_item_list) :
        save_as_filename_map = {}
        
        for zip_item in zip_item_list :
            stem, extension = os.path.splitext(zip_item.filename)
            
            save_as_filename = os.path.join(
                self.save_to_directory, 
                "{}{}".format(str(self.image_filename), extension))     
            
            save_as_filename_map[zip_item.filename] = save_as_filename
            
        return save_as_filename_map
        
    def __extract_file(self, zip_file, zip_item, save_as_filename_map) :
        save_as_filename = save_as_filename_map[zip_item.filename]
        
        zip_item_bytes = zip_file.read(zip_item)
        
        if save_as_filename.endswith(".json") :
            json_string = self.__update_json_filename_entry(zip_item_bytes, save_as_filename_map)
            self.__save_json_file(json_string, save_as_filename)
            
        else :
            self.__save_image_file(zip_item_bytes, save_as_filename)
        
        if self.verbose :
            print("Extracting {} to {}".format(zip_item.filename, save_as_filename))                
    
    def __update_json_filename_entry(self, zip_item_bytes, save_as_filename_map) :
        json_data = json.loads(zip_item_bytes)
        
        for save_as_filename in save_as_filename_map.values() :
            if save_as_filename.endswith(".json") :
                continue
            
            json_data["filename"] = os.path.basename(save_as_filename)
            
        return json.dumps(json_data, indent=4)
           
    def __update_file_counters(self) :             
        self.image_filename += 1
        self.images_downloaded += 1
        
        if self.images_downloaded % 100 == 0 :
            print("Downloaded {} images".format(self.images_downloaded))
            
    def __save_json_file(self, json_string, save_as_filename) :
        with open(save_as_filename, "w") as output_file :
            output_file.write(json_string)   
            
    def __save_image_file(self, image_bytes, save_as_filename) :
        with open(save_as_filename, "wb") as output_file :
            output_file.write(image_bytes)       
            
    def __download_image_sync(self) :
        response = requests.get(self.image_server_url)
        
        if response.status_code == 200 :
            self.__save_image_zip(io.BytesIO(response.content), response.headers)
        else :
            print(response.text)
            
    def download_images(self, first_image_filename, number_of_images_to_get) : 
        self.image_filename = first_image_filename
        self.images_downloaded = 0
        
        try :
            start_time = time.time()
            
            loop = asyncio.get_event_loop()
         
            while self.images_downloaded  < number_of_images_to_get :
                loop.run_until_complete(self.__download_image())
              
            loop.run_until_complete(self.http_session.close())  
            loop.close()   
                       
            print("Downloaded {} images in {:.2f} seconds".format(
                number_of_images_to_get, time.time() - start_time))
            
        except aiohttp.client_exceptions.ClientConnectionError as connect_error :
            print("Unable to connect to an image server at", self.image_server_url)
            
    
if __name__ == '__main__' :
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-v", "--verbose", action="store_true", 
                        help="Produce verbose output on progress")    
    parser.add_argument("-s", "--start", type=int, default=1, 
                        help="Integer filename of first image (images are names in a sequence 1.png, 2.png etc)")
    parser.add_argument("-c", "--count", type=int, default=1, 
                        help="Number of images to download")
    parser.add_argument("url",  help="url to download images from")
    
    args = parser.parse_args()    
    
    client = DaemonClient(args.url, "www_output", args.verbose)
    client.download_images(args.start, args.count)