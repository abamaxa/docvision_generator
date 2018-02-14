from aiohttp import web
import multiprocessing as mp
import queue
import os

from simple_question import SimpleQuestion

class Webserver :
    def __init__(self, num_process, queue_size, options) :
        self.queue_size = queue_size
        self.options = options
        self.num_process = num_process
        self.app = self.task_queue = self.done_queue = None
        self.image_counter = 1
        
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
    
    async def status(self, request) :
        try :
            task_size = self.task_queue.qsize()
            done_size = self.done_queue.qsize()
        except :
            task_size = -1
            done_size = -1
            
        html = """
        <html>
        <body>
        Task Queue length: {}<br>
        Done Queue length: {}<br>
        Image no: {}<br>
        <a href="/question">Question</a>
        </body>
        </html>
        """.format(task_size, done_size, self.image_counter)
        
        return web.Response(content_type="html", text=html)
        
    def start_server(self) :
        self.__setup_workers()
        
        self.app = web.Application()
        self.app.router.add_get('/', self.status)
        self.app.router.add_get('/question', self.get_a_question)
        
        web.run_app(self.app)        
        
    def __setup_workers(self) :
        self.task_queue = mp.Queue(self.queue_size)
        self.done_queue = mp.Queue()
        
        for _ in range(self.queue_size) :
            self.__request_question()       
        
        for _ in range(self.num_process):
            mp.Process(target=Webserver.worker, 
                       args=(self.task_queue, self.done_queue)).start()   
    
          
    def __request_question(self) :
        self.task_queue.put((Webserver.make_question, (self.image_counter, self.options))) 
        self.image_counter += 1
        
    @staticmethod  
    def worker(input_queue, output_queue):
        for func, args in iter(input_queue.get, 'STOP'):
            result = func(*args)
            output_queue.put(result)
    
    @staticmethod  
    def make_question(idno, options):
        question = SimpleQuestion(idno, options)
        question.create_page()
            
        zip_file_object, filename = question.as_zip()  
        #filename = question.save_as_zip()
        print("Completed:", filename)
        return zip_file_object, filename
        #return filename
