import time
import argparse
import multiprocessing as mp
import logging

from question_generator import SimpleQuestion, FilePersistence, Webserver
from augmention import ImgAugAugmentor, ImageTiler

def worker(input_queue, output_queue):
    for func, args in iter(input_queue.get, 'STOP'):
        result = func(*args)
        output_queue.put(result)

def make_question(idno, options):
    start = time.time()

    persister = FilePersistence(idno, options)
    question = SimpleQuestion(idno, options)
    
    question.create_page()
    
    tiler = ImageTiler(question, options)
    augmentor = ImgAugAugmentor(question, tiler, options)
    
    for aug_image, aug_frames in augmentor :
        persister.save_image(aug_image, aug_frames)
    
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
        "-x",
        "--overwrite",
        help="Overwrite existing files",
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
        default=300)
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
        "--experimental",
        help="Try code that is work in progress",
        action="store_true")     
   
    parser.add_argument("count", type=int, help="Number of images to create or queue size if in daemon mode")

    args = parser.parse_args()

    options = {
        "format": args.format,
        "outputDir": args.output,
        "dimensions": (args.width, args.height),
        "outputSize": (args.dimension, args.dimension),
        "save_tiles": args.tile,
        "overwrite": args.overwrite,
        "augmentation_file" : args.augmentation_file,
        "draw_debug_rects" : False,
        "draw_final_rects" : True
    }

    print("Image dimensions: {dimensions} format: {format}".format_map(options))
    if args.tile :
        print("Creating tiles of size {outputSize}".format_map(options))

    if args.experimental :
        import question_generator.constructed_page as experimental
        experimental.make_question("test", options)
        
    elif args.daemon :     
        print("Starting webserver, queue size {}".format(args.count))
        server = Webserver(args.num_processes, args.count, 
                                     args.port, args.start, options)
        server.start_server()
    else :
        print("Writing images to: {outputDir} overwrite existing: {overwrite}".format_map(options))
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
