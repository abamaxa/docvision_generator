import multiprocessing as mp
from simple_question import SimpleQuestion
import time

dimension = 300

options = {
    "format" : "png",
    "outputDir" : "output_png_{}".format(dimension),
    "dimensions" : (600, 1000),
    #"dimensions" : (300, 424),
    #"dimensions" : (1275, 1755),
    "outputSize" : (dimension, dimension),
    #outputSize" : (600,int(600 * (1755 / 1275)),
    "saveTiles" : True,
}

print("Question dimensions {dimensions} => {outputSize} output {outputDir} format {format}".format_map(options))

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
    counter = 0
    totalTime = 0.0
    
    for i in range(len(TASKS)):
        totalTime += done_queue.get()
        counter += 1
        if counter % 500 == 0 :
            print("Generated {} images, average {:2f} seconds per image".format(
                counter, totalTime / counter))

    for i in range(numProcess):
        task_queue.put('STOP') 
        
    print("Generated {} images in {:.2f} seconds".format(endNo - startNo, time.time() - start))
        
if __name__ == '__main__':
    NUMBER_OF_PROCESSES = 4
    mp.freeze_support()
    
    generateQuestions(NUMBER_OF_PROCESSES, 1, 10000)
    
    #for i in range(10) :
    #    print(makeQuestion(i))