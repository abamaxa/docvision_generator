import multiprocessing as mp
from simple_question import SimpleQuestion
import time
import argparse
        
def worker(input, output) :
    for func, args in iter(input.get, 'STOP'):
        result = func(*args)
        output.put(result)
        
def makeQuestion(idno, options) :
    start = time.time()
        
    questionFactory = SimpleQuestion(options)
    questionFactory.createPage(idno)
    questionFactory.save()
    
    return (idno, time.time() - start)
    
def generateQuestions(numProcess, options, startNo, endNo) :
    start = time.time()
    
    TASKS = [(makeQuestion, (i,options)) for i in range(startNo, endNo + 1)]

    # Create queues
    task_queue = mp.Queue()
    done_queue = mp.Queue()

    # Submit tasks
    for task in TASKS:
        task_queue.put(task)

    # Start worker processes
    for i in range(numProcess):
        mp.Process(target=worker, args=(task_queue, done_queue)).start()

    counter = 0
    totalTime = 0.0
    
    for i in range(len(TASKS)):
        idno, timeTaken = done_queue.get()
        totalTime += float(timeTaken)
        counter += 1
        if counter % 500 == 0 :
            print("Generated {} images, average {:2f} seconds per image".format(
                counter, totalTime / counter))

    for i in range(numProcess):
        task_queue.put('STOP') 
        
    print("Generated {} images in {:.2f} seconds".format(endNo - startNo, time.time() - start))
        
        
def main() :
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-t", "--tile", help="Whether to generate square tiles of" \
                        "top, middle and bottom of generated image", action="store_false")
    parser.add_argument("-o", "--output", help="Directory to write images to", default="output")
    parser.add_argument("-w", "--width", type=int, help="Width of generated image", default=600)
    parser.add_argument("-l", "--height", type=int, help="Height of generated image", default=1000)
    parser.add_argument("-d", "--dimension", type=int, help="Width of output image", default=300)
    parser.add_argument("-s", "--start", type=int, help="Index of first image", default=1)
    parser.add_argument("-p", "--process", type=int, help="Number of processes to spawn", default=4)
    parser.add_argument("-f", "--format", help="File format to generate, png (default) or jpg", default="png")
    
    parser.add_argument("count", type=int, help="Number of images to create")
    
    args = parser.parse_args()
    
    options = {
        "format" : args.format,
        "outputDir" : args.output,
        "dimensions" : (args.width, args.height),
        #"dimensions" : (300, 424),
        #"dimensions" : (1275, 1755),
        "outputSize" : (args.dimension, args.dimension),
        #outputSize" : (600,int(600 * (1755 / 1275)),
        "saveTiles" : args.tile,
    }    
    
    print("Question dimensions {dimensions} => {outputSize} output {outputDir} format {format}".format_map(options))   
  
    if args.process == 0 :
        print(makeQuestion(1, options))
    else :
        mp.freeze_support()
    
        generateQuestions(args.process, options, args.start, args.start + args.count)

    
if __name__ == '__main__':
    main()
    