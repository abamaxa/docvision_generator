import time
import argparse
import multiprocessing as mp

from simple_question import SimpleQuestion

def worker(input_queue, output_queue):
    for func, args in iter(input_queue.get, 'STOP'):
        result = func(*args)
        output_queue.put(result)


def make_question(idno, options):
    start = time.time()

    question = SimpleQuestion(options)
    question.create_page(idno)
    question.save()

    return (idno, time.time() - start)


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
        _, time_taken = done_queue.get()
        total_time += float(time_taken)
        counter += 1
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
        action="store_false")
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
        default=600)
    parser.add_argument(
        "-l",
        "--height",
        type=int,
        help="Height of generated image",
        default=1000)
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
        "-p",
        "--process",
        type=int,
        help="Number of processes to spawn",
        default=4)
    parser.add_argument(
        "-f",
        "--format",
        help="File format to generate, png (default) or jpg",
        default="png")

    parser.add_argument("count", type=int, help="Number of images to create")

    args = parser.parse_args()

    options = {
        "format": args.format,
        "outputDir": args.output,
        "dimensions": (args.width, args.height),
        #"dimensions" : (300, 424),
        #"dimensions" : (1275, 1755),
        "outputSize": (args.dimension, args.dimension),
        # outputSize" : (600,int(600 * (1755 / 1275)),
        "save_tiles": args.tile,
    }

    print("Tile: {save_tiles} dimensions {dimensions} => {outputSize} " \
          "output {outputDir} format {format}".format_map(options))

    if args.process == 0:
        for i in range(args.start, args.start + args.count) :
            print(make_question(i, options))
    else:
        mp.freeze_support()

        generate_questions(
            args.process,
            options,
            args.start,
            args.start +
            args.count)


if __name__ == '__main__':
    main()
