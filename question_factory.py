import multiprocessing as mp
from simple_question import SimpleQuestion
import time

options = {
    "format" : "png",
    "outputDir" : "output_png_300",
    "dimensions" : (600, 1000),
    #"dimensions" : (300, 424),
    #"dimensions" : (1275, 1755),
    "outputSize" : (300, 300),
    #outputSize" : (600,int(600 * (1755 / 1275)),
    "saveTiles" : True,
}

questionFactory = SimpleQuestion(options)
        
def worker(input, output):
    for func, args in iter(input.get, 'STOP'):
        result = func(*args)
        output.put(result)
        
def makeQuestion(idno) :
    start = time.time()
        
    questionFactory.createPage(idno)
    questionFactory.save()
    
    return "Generated image id {} in {:.2f} seconds".format(idno, time.time() - start)
    
def generateQuestions(numProcess, startNo, endNo) :
    start = time.time()
    
    TASKS = [(makeQuestion, (i,)) for i in range(startNo, endNo + 1)]

    # Create queues
    task_queue = mp.Queue()
    done_queue = mp.Queue()

    # Submit tasks
    for task in TASKS:
        task_queue.put(task)

    # Start worker processes
    for i in range(numProcess):
        mp.Process(target=worker, args=(task_queue, done_queue)).start()

    # Get and print results
    print('Unordered results:')
    for i in range(len(TASKS)):
        print('\t', done_queue.get())

    for i in range(numProcess):
        task_queue.put('STOP') 
        
    print("Generated {} images in {:.2f} seconds".format(endNo - startNo, time.time() - start))
        
if __name__ == '__main__':
    NUMBER_OF_PROCESSES = 4
    mp.freeze_support()
    
    #generateQuestions(NUMBER_OF_PROCESSES, 1, 1000)
    
    for i in range(10) :
        print(makeQuestion(i))