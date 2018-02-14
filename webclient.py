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

class DaemonClient :
    def __init__(self, image_server_url, save_to_directory) :
        self.image_server_url = image_server_url
        self.save_to_directory = save_to_directory
        self.images_downloaded = 0
        self.http_session = None
        
        os.makedirs(save_to_directory, exist_ok=True)
        
    async def __init_http_sesssion(self) :
        self.http_session = aiohttp.ClientSession() 
        
    async def __download_image(self) :
        if self.http_session is None :
            await self.__init_http_sesssion()
            
        async with self.http_session.get(self.image_server_url) as response :
            if response.content_type == "application/zip" and response.status == 200 :
                self.__save_image_zip(io.BytesIO(await response.read()), response.headers)
            #else :
                #print(await response.text())
                #print('.', end='')
                 
    def __save_image_zip(self, zip_bytes_file_obj, headers) :   
        m = re.search('filename="(\d+\.zip)"', headers.get('Content-Disposition'))
        if m :
            filename = m.group(1)
            print("Received file:", filename)
            
        with zipfile.ZipFile(zip_bytes_file_obj, 'r') as image_zip:
            image_zip.extractall(self.save_to_directory)
            
        self.images_downloaded += 1
            
    def __download_image_sync(self) :
        response = requests.get(self.image_server_url)
        
        if response.status_code == 200 :
            self.__save_image_zip(io.BytesIO(response.content), response.headers)
        else :
            print(response.text)
            
    def download_images(self, number_of_images_to_get) : 
        try :
            start_time = time.time()
            self.images_downloaded = 0
            loop = asyncio.get_event_loop()
         
            while self.images_downloaded  < number_of_images_to_get :
                loop.run_until_complete(self.__download_image())
                
            loop.close()   
            print("Downloaded {} images in {:.2f} seconds".format(
                number_of_images_to_get, time.time() - start_time))
        except aiohttp.client_exceptions.ClientConnectionError as connect_error :
            print("Unable to connect to an image server at", self.image_server_url)
            
    
if __name__ == '__main__' :
    parser = argparse.ArgumentParser()
    
    parser.add_argument("count", type=int, help="Number of images to download")
    parser.add_argument("url",  help="url to download images from")
    
    args = parser.parse_args()    
    client = DaemonClient(args.url, "www_output")
    client.download_images(args.count)