import time
import os
import argparse
import multiprocessing as mp
import logging
import cProfile, pstats, io
import random

from page_generator import FragmentPage, FilePersistence
from webserver import Webserver

def worker(input_queue, output_queue):
    for func, args in iter(input_queue.get, 'STOP'):
        result = func(*args)
        output_queue.put(result)

def make_page(idno, options):
    start = time.time()

    persister = FilePersistence(idno, options)
    page = FragmentPage(idno, options, persister)

    page.create_page()
    page.save()
        
    return (persister.get_count(), time.time() - start)

def generate_pages(options):
    num_process = options["cpus"]
    start_no = options["initial"]
    end_no = options["initial"] + options["count"]
    
    start = time.time()

    tasks = [(make_page, (i, options)) for i in range(start_no, end_no + 1)]

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
        if counter % 500 == 0 and counter:
            print(
                "Generated {} images, average {:.2f} seconds per image".format(
                    counter, total_time / counter))

    for _ in range(num_process):
        task_queue.put('STOP')

    print("Generated {} images in {:.2f} seconds".format(
        end_no - start_no, time.time() - start))

def get_args() :
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t",
        "--template",
        help="Name (as set in json file - not file name/path) of the template to use. " \
        "This file containing this template must reside in the templates directory. " \
        "If not set templates are choosen at random")
    parser.add_argument(
        "--daemon",
        help="Instead of writing files to a directory, the process server images over HTTP",
        action="store_true") 
    parser.add_argument(
        "-o",
        "--outputDir",
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
        "-i",
        "--initial",
        type=int,
        help="Index of first image",
        default=1)
    parser.add_argument(
        "--cpus",
        type=int,
        help="Number of processes to spawn, defaults to the number of CPUs available",
        default=0)
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
        "-c",
        "--chop",
        help="Chop up image into subimages",
        action="store_true")            
    parser.add_argument(
        "--augmentation_file",
        help="JSON file containing parameters for the augmentor",
        default="augmentation.json")        
    parser.add_argument(
        "--color_model",
        help="Color model to store images as RGB (default) or HSV",
        choices=["RGB","HSV"],
        default="RGB")
    parser.add_argument(
        "-f",
        "--format",
        help="File format to generate, png or jpg (default)",
        choices=["jpg", "png"],
        default="jpg")    
    parser.add_argument(
        "-e",
        "--profile",
        help="Profile code",
        action="store_true")    
    parser.add_argument(
        "-s",
        "--single",
        help="Generate a page with a single rendering of a template - for testing",
        action="store_true")  
    parser.add_argument(
        "--random_seed",
        help="Seeds the random number generator with a particular value for EACH PAGE, "
        "creating identical pages. For debugging single pages only.")     
    parser.add_argument(
        "--deterministic",
        help="Seeds the random number generator with known values, creating same data sets on each run",
        action="store_true")         
    parser.add_argument(
        "--log_level",
        type=int,
        help="Set the level of debug logging, with 4 as most detailed through to 0 as least detailed, default 2",
        choices=[0,1,2,3,4],
        default=2)
    
    parser.add_argument("count", type=int, help="Number of images to create or queue size if in daemon mode")

    return parser.parse_args()

def setup_logging(args) :
    log_levels = [logging.FATAL, logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    logging.basicConfig(level=log_levels[args.log_level])    

def main():
    args = get_args()
    
    setup_logging(args)
    
    options = dict(args.__dict__)
    options.update({
        "format": args.format.strip(),
        "dimensions": (args.width, args.height),
        "outputSize": (args.dimension, args.dimension),
        "draw_debug_rects" : False,
        "draw_final_rects" : False,
        "color_model" : args.color_model.upper()
    })
        
    if not args.cpus :
        options["cpus"] = os.cpu_count()
        
    logging.info("Image dimensions: {dimensions} format: {format}".format_map(options))

    if args.profile :
        pr = cProfile.Profile()
        pr.enable()            
        for i in range(args.initial, args.initial + args.count) :
            count, elapsed = pr.runcall(make_page, *(str(i), options))
            print(count, elapsed)
            if elapsed > 2 :
                ps = pstats.Stats(pr)
                ps.sort_stats('cumtime')
                ps.print_stats(0.1)
            pr.clear()
        
    elif args.daemon :     
        logging.info("Starting webserver, queue size {}".format(args.count))
        server = Webserver(options)
        server.start_server()
    else :
        logging.info("Writing images to: {outputDir}".format_map(options))
        logging.info("Generating {} images starting at {}".format(args.count, args.initial))
        
        if options["cpus"] == 1 :    
            for i in range(args.initial, args.initial + args.count) :
                num, elapsed = make_page(str(i), options)
                print("{} - {} images in {:.2f} seconds".format(i, num, elapsed))
                
        else:
            mp.freeze_support()
            generate_pages(options)

if __name__ == '__main__':
    main()
