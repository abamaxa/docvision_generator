from aiohttp import web
import multiprocessing as mp

from simple_question import SimpleQuestion

class Webserver :
    def __init__(self, num_process, queue_size, options) :
        self.queue_size = queue_size
        self.options = options
        self.num_process = num_process
        self.app = self.task_queue = self.done_queue = None
        self.image_counter = 1
        
    async def handle(self, request):
        # Make sure there is work in the queue  
        while not self.task_queue.full() :
            self.request_question()
                    
        # Don't block
        try :
            result = self.done_queue.get(False)
        except mp.Queue.Empty :
            # Error
            return web.Response(status=404, text="No images ready")
              
        zipdata = result.getvalue()
        headers = {
            "Cache-Control": "no-cache, no-store",
            "Content-Disposition" : 'attachment; filename="image.zip"'
        }
        return web.Response(content_type="application/zip", body=zipdata, headers=headers)
        
    def start_server(self) :
        self.setup_workers()
        
        self.app = web.Application()
        self.app.router.add_get('/', self.handle)
        
        web.run_app(self.app)        
        
    def setup_workers(self) :
        self.task_queue = mp.Queue(self.queue_size)
        self.done_queue = mp.Queue()
        
        for _ in range(self.queue_size) :
            self.request_question()       
        
        for _ in range(self.num_process):
            mp.Process(target=Webserver.worker, 
                       args=(self.task_queue, self.done_queue)).start()   
    
          
    def request_question(self) :
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
            
        return question.as_zip()  
