import multiprocessing as mp
import queue
import os
import logging

from aiohttp import web
import aiohttp_jinja2
import jinja2

from page_generator import FragmentPage, ZipBufferPersistence

class WebserverError(Exception) :
    pass

class Webserver :
    def __init__(self, options) :
        self.queue_size = options["count"]  
        self.options = options   
        self.num_process = options["cpus"]
        self.app = self.task_queue = self.done_queue = None
        self.image_number = options["initial"]
        self.port = options["port"]
        self.image_count = 0
    
    async def get_a_page(self, request):   
        try :
            # Don't block, this method can sometimes raise a queue.Empty
            # exception while waiting for the multiprocess background thread
            # to finish flushing the queue.
            zip_file_object, filename, num_images = self.done_queue.get_nowait()
            
            self.image_count += num_images
            
            # Add a request for another image to the queue.  
            self.__request_page()            
        except queue.Empty :
            # No files available
            return web.Response(status=404, text="No images ready")
              
        zip_bytes = zip_file_object.getvalue()
        headers = {
            "Cache-Control": "no-cache, no-store",
            "Content-Disposition" : 'attachment; filename="{}"'.format(filename)
        }
        return web.Response(content_type="application/zip", body=zip_bytes, headers=headers)
    
    @aiohttp_jinja2.template('status.html')
    async def status(self, request) :
        return self.__get_status()
    
    @aiohttp_jinja2.template('status.html')
    async def update_config(self, request) :
        data = await request.post()
        error_message = None
        try :
            width = int(data['width'])
            if width < 100 or width > 4000 :
                raise WebserverError("Image width must be between 100 and 4000")
            
            length = int(data['height'])
            if length < 100 or length > 4000 :
                raise WebserverError("Image height must be between 100 and 4000")    
            
            tile_size = int(data["tile_size"])
            if tile_size < 100 or tile_size > 4000 :
                raise WebserverError("Tile size must be between 100 and 4000") 

            self.options["dimensions"] = (width, length)
            self.options["outputSize"] = (tile_size, tile_size)
            self.options["format"] = data["format"]
            self.options["color_model"] = data["color_model"]
            self.options["chop"] = data.get("chop", False)
            self.options["augment"] = data.get("augment", False)
            
        except Exception as exception :
            error_message = str(exception)
            
        display = self.__get_status()
        
        if error_message :
            display['error_message'] = error_message
            
        return display
    
    def __get_status(self) :
        try :
            task_size = self.task_queue.qsize()
            done_size = self.done_queue.qsize()
        except :
            task_size = -1
            done_size = -1
            
        display = {
            "task_queue_size": task_size,
            "done_queue_size": done_size,
            "image_number" : self.image_number,
            "image_count" : self.image_count,
            "width" : self.options["dimensions"][0],
            "height" : self.options["dimensions"][1],
            "tile_size" : self.options["outputSize"][0],
            "format" : self.options["format"],
            "chop" : self.options["chop"],
            "augment" : self.options["augment"],
            "color_model" : self.options["color_model"]
        }

        return display        
        
    def start_server(self) :
        self.__setup_workers()
        
        self.app = web.Application()
        self.app.router.add_get('/', self.status)
        self.app.router.add_post('/', self.update_config)
        self.app.router.add_get('/page', self.get_a_page)
        
        aiohttp_jinja2.setup(
            self.app, loader=jinja2.FileSystemLoader('webserver/templates'))        
        
        web.run_app(self.app, port = self.port)        
        
    def __setup_workers(self) :
        self.task_queue = mp.Queue(self.queue_size)
        self.done_queue = mp.Queue()
        
        for _ in range(self.queue_size) :
            self.__request_page()       
        
        for _ in range(self.num_process):
            mp.Process(target=Webserver.worker, 
                       args=(self.task_queue, self.done_queue)).start()   
    
          
    def __request_page(self) :
        self.task_queue.put((Webserver.make_page, (self.image_number, self.options))) 
        self.image_number += 1
        
    @staticmethod  
    def worker(input_queue, output_queue):
        for func, args in iter(input_queue.get, 'STOP'):
            result = func(*args)
            output_queue.put(result)
    
    @staticmethod  
    def make_page(idno, options):
        persister = ZipBufferPersistence(idno, options)
        page = FragmentPage(idno, options, persister)
        
        page.create_page()
        page.save()

        logging.info("Completed:", persister.get_zip_filename())
        return persister.get_zip_buffer(), \
               persister.get_zip_filename(), \
               persister.get_count()
