import time
import argparse
import multiprocessing as mp
import logging
import cProfile, pstats, io

from page_generator import ConstructedPage, FilePersistence
from webserver import Webserver

def worker(input_queue, output_queue):
    for func, args in iter(input_queue.get, 'STOP'):
        result = func(*args)
        output_queue.put(result)

def make_question(idno, options):
    start = time.time()

    persister = FilePersistence(idno, options)
    question = ConstructedPage(idno, options, persister)
    foo = question.create_page

    question.create_page()
    question.save()
        
    return (persister.get_count(), time.time() - start)

def generate_questions(num_process, options, start_no, end_no):
    start = time.time()

    tasks = [(make_question, (i, options)) for i in range(start_no, end_no + 1)]

    # Create queues
    task_queue = mp.Queue()
    done_queue = mp.Queue()

    # Submit tasks
    for task in tasks:
        task_queue.put(task)

    # Start worker processes
    for _ in range(num_process):
        mp.Process(target=worker, args=(task_queue, done_queue)).start()

    counter = 0
    total_time = 0.0

    for _ in range(len(tasks)):
        count, time_taken = done_queue.get()
        total_time += float(time_taken)
        counter += count
        if counter % 500 == 0:
            print(
                "Generated {} images, average {:.2f} seconds per image".format(
                    counter, total_time / counter))

    for _ in range(num_process):
        task_queue.put('STOP')

    print("Generated {} images in {:.2f} seconds".format(
        end_no - start_no, time.time() - start))

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t",
        "--tile",
        help="Whether to generate square tiles of"
        "top, middle and bottom of generated image",
        action="store_true")
    parser.add_argument(
        "--daemon",
        help="Instead of writing files to a directory, the process server images over HTTP",
        action="store_true") 
    parser.add_argument(
        "-o",
        "--output",
        help="Directory to write images to",
        default="output")
    parser.add_argument(
        "-w",
        "--width",
        type=int,
        help="Width of generated image",
        default=1275)
    parser.add_argument(
        "-l",
        "--height",
        type=int,
        help="Height of generated image",
        default=1755)
    parser.add_argument(
        "-d",
        "--dimension",
        type=int,
        help="Width of output image",
        default=600)
    parser.add_argument(
        "-s",
        "--start",
        type=int,
        help="Index of first image",
        default=1)
    parser.add_argument(
        "-n",
        "--num_processes",
        type=int,
        help="Number of processes to spawn",
        default=4)
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        help="Port HTTP server listens on",
        default=80)    
    parser.add_argument(
        "-a",
        "--augment",
        help="Augment images",
        action="store_true")         
    parser.add_argument(
        "--augmentation_file",
        help="JSON file containing parameters for the augmentor",
        default="augmentation.json")        
    parser.add_argument(
        "-f",
        "--format",
        help="File format to generate, png (default) or jpg",
        default="png")
    parser.add_argument(
        "-e",
        "--profile",
        help="Profile code",
        action="store_true")    
    
    parser.add_argument("count", type=int, help="Number of images to create or queue size if in daemon mode")

    args = parser.parse_args()

    options = {
        "format": args.format,
        "outputDir": args.output,
        "dimensions": (args.width, args.height),
        "outputSize": (args.dimension, args.dimension),
        "save_tiles": args.tile,
        "augmentation_file" : args.augmentation_file,
        "augment" : args.augment,
        "draw_debug_rects" : False,
        "draw_final_rects" : True
    }

    print("Image dimensions: {dimensions} format: {format}".format_map(options))
    if args.tile :
        print("Creating tiles of size {outputSize}".format_map(options))

    if args.profile :
        pr = cProfile.Profile()
        pr.enable()            
        for i in range(args.start, args.start + args.count) :
            count, elapsed = pr.runcall(make_question, *(str(i), options))
            print(count, elapsed)
            if elapsed > 2 :
                ps = pstats.Stats(pr)
                ps.sort_stats('cumtime')
                ps.print_stats(0.1)
            pr.clear()
        
    elif args.daemon :     
        print("Starting webserver, queue size {}".format(args.count))
        server = Webserver(args.num_processes, args.count, 
                                     args.port, args.start, options)
        server.start_server()
    else :
        print("Writing images to: {outputDir}".format_map(options))
        print("Generating {} images starting at {}".format(args.count, args.start))
        
        if args.num_processes == 0:    
            for i in range(args.start, args.start + args.count) :
                print(make_question(str(i), options))
                
        else:
            mp.freeze_support()
    
            generate_questions(
                args.num_processes,
                options,
                args.start,
                args.start +
                args.count)

if __name__ == '__main__':
    main()
