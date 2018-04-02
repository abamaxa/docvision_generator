import multiprocessing as mp
import queue
import os

from aiohttp import web
import aiohttp_jinja2
import jinja2

from page_generator import ConstructedPage, ZipBufferPersistence

class Webserver :
    def __init__(self, num_process, queue_size, port, first_image_number, options) :
        self.queue_size = queue_size
        self.options = options
        self.num_process = num_process
        self.app = self.task_queue = self.done_queue = None
        self.image_number = first_image_number
        self.port = port
        self.image_count = 0
    
    async def get_a_question(self, request):   
        try :
            # Don't block, this method can sometimes raise a queue.Empty
            # exception while waiting for the multiprocess background thread
            # to finish flushing the queue. If problematic use
            # __get_a_question_using_filesystem instead.
            zip_file_object, filename = self.done_queue.get_nowait()
            
            # Add a request for another image to the queue.  
            self.__request_question()            
        except queue.Empty :
            # No files available
            return web.Response(status=404, text="No images ready")
              
        zip_bytes = zip_file_object.getvalue()
        headers = {
            "Cache-Control": "no-cache, no-store",
            "Content-Disposition" : 'attachment; filename="{}"'.format(filename)
        }
        return web.Response(content_type="application/zip", body=zip_bytes, headers=headers)
    
    async def get_a_question_using_filesystem(self, request) :
        try :
            # Don't block
            filename = self.done_queue.get_nowait()
            # Make sure there is work in the queue  
            self.__request_question()            
        except queue.Empty :
            # No files available
            return web.Response(status=404, text="No images ready")

        headers = {
            "Content-Type" : "application/zip",
            "Cache-Control": "no-cache, no-store",
            "Content-Disposition" : 'attachment; filename="{}"'.format(os.path.basename(filename))
        }

        return web.FileResponse(filename, headers=headers)
    
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
                raise ValueError("Image width must be between 100 and 4000")
            
            length = int(data['height'])
            if length < 100 or length > 4000 :
                raise ValueError("Image height must be between 100 and 4000")    
            
            tile_size = int(data["tile_size"])
            if tile_size < 100 or tile_size > 4000 :
                raise ValueError("Tile size must be between 100 and 4000")              
            
            self.options["dimensions"] = (width, length)
            self.options["outputSize"] = (tile_size, tile_size)
            self.options["format"] = data["format"]
            if data.get("save_tiles") :
                self.options["save_tiles"] = True
            else :
                self.options["save_tiles"] = False
            
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
            "width" : self.options["dimensions"][0],
            "height" : self.options["dimensions"][1],
            "tile_size" : self.options["outputSize"][0],
            "format" : self.options["format"],
            "save_tiles" : self.options["save_tiles"],
        }

        return display        
        
    def start_server(self) :
        self.__setup_workers()
        
        self.app = web.Application()
        self.app.router.add_get('/', self.status)
        self.app.router.add_post('/', self.update_config)
        self.app.router.add_get('/question', self.get_a_question)
        
        aiohttp_jinja2.setup(
            self.app, loader=jinja2.FileSystemLoader('webserver/templates'))        
        
        web.run_app(self.app, port = self.port)        
        
    def __setup_workers(self) :
        self.task_queue = mp.Queue(self.queue_size)
        self.done_queue = mp.Queue()
        
        for _ in range(self.queue_size) :
            self.__request_question()       
        
        for _ in range(self.num_process):
            mp.Process(target=Webserver.worker, 
                       args=(self.task_queue, self.done_queue)).start()   
    
          
    def __request_question(self) :
        self.task_queue.put((Webserver.make_question, (self.image_number, self.options))) 
        self.image_number += 1
        
    @staticmethod  
    def worker(input_queue, output_queue):
        for func, args in iter(input_queue.get, 'STOP'):
            result = func(*args)
            output_queue.put(result)
    
    @staticmethod  
    def make_question(idno, options):
        persister = ZipBufferPersistence(idno, options)
        question = SimpleQuestion(idno, options, persister)
        
        question.create_page()
        question.save()

        print("Completed:", filename)
        return persister.get_zip_buffer(), persister.get_zip_filename()
