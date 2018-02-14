import os
import random
import json
import zipfile
from io import BytesIO

from dictionary_generator import TextGen
from util import *
from draw import Draw

class Question(object):
    Layout_HSep_None = 0
    Layout_HSep_BlankLine1 = 0.5
    Layout_HSep_BlankLine2 = 0.75
    Layout_HSep_BlankLine3 = 1.
    Layout_HSep_BlankLine4 = 1.25

    Layout_HSep_SolidLine = 0x8
    Layout_HSep_DashedLine = 0x10
    Layout_HSep_DottedLine = 0x20

    Layout_HLine_Top = 0x40
    Layout_HLine_Bottom = 0x80

    Layout_VSep_None = 0
    Layout_VSep_BlankLine1 = 1
    Layout_VSep_BlankLine2 = 1.25
    Layout_VSep_BlankLine3 = 1.5
    Layout_VSep_BlankLine4 = 1.75

    Layout_VSep_SolidLine = 0x8
    Layout_VSep_DashedLine = 0x10
    Layout_VSep_DottedLine = 0x20

    Layout_VLine_Left = 0x40
    Layout_VLine_Right = 0x80
    Layout_VLine_LeftAndRight = 0x100
    Layout_VLine_Internal = 0x40
    Layout_VLine_ExternalAndInternal = 0x80

    def __init__(self, name, options):
        super(Question, self).__init__()

        self.name = str(name)
        self.options = options
        dimensions = options["dimensions"]
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.image_format = options.get("format", "png")

        self.draw_debug_rects = False

        self.generate_page()

    def generate_page(self):
        self.left_margin = self.width * (0.03 + (0.05 * random.random()))
        self.right_margin = self.width * (0.03 + (0.05 * random.random()))
        self.top_margin = self.height * (0.04 + (0.05 * random.random()))
        self.bottom_margin = self.height * (0.04 + (0.05 * random.random()))

        fontnames = ["verdana.ttf", "times.ttf", "georgia.ttf", "arial.ttf"]

        # Assume that its A4 size, calculate relative to width
        #self.line_height = self.font_size = random.randint(18,24)
        self.line_height = self.font_size = random.randint(
            int(self.width / 70), int(self.width / 50))
        self.font_name = random.choice(fontnames)
        self.question_frames = []
        self.question_text_frames = []

        self.generate_random_style()

        self.minimum_question_gap = self.para_spacing * 1.5

        self.draw = Draw(self)
        self.draw.init_image()        
        self.draw.create_draw()
        
        self.generator = TextGen.get_generator()

        self.line_height = self.draw.get_line_height()

        self.generate_layout()
                
    def draw_page_background(self) :
        self.draw.draw_background()
        self.draw_columns()        

    def generate_random_style(self):
        columns = ((0.66, 1), (0.9, 2), (1., 3))
        hseps_lines = (
            (0.2, Question.Layout_HSep_BlankLine1),
            (0.6, Question.Layout_HSep_BlankLine2),
            (0.85, Question.Layout_HSep_BlankLine3),
            (1.0, Question.Layout_HSep_BlankLine4),
        )

        vseps_lines = (
            (0.2, Question.Layout_VSep_BlankLine1),
            (0.6, Question.Layout_VSep_BlankLine2),
            (0.85, Question.Layout_VSep_BlankLine3),
            (1.0, Question.Layout_VSep_BlankLine4),
        )

        hseps_styles = (
            (0.7, Question.Layout_HSep_None),
            (0.8, Question.Layout_HSep_SolidLine),
            (0.9, Question.Layout_HSep_DashedLine),
            (1.0, Question.Layout_HSep_DottedLine),
        )

        vseps_styles = (
            (0.7, Question.Layout_VSep_None),
            (0.8, Question.Layout_VSep_SolidLine),
            (0.9, Question.Layout_VSep_DashedLine),
            (1.0, Question.Layout_VSep_DottedLine),
        )

        hseps_positions = (
            (0.65, Question.Layout_HSep_None),
            (0.9, Question.Layout_HLine_Bottom),
            (1.0, Question.Layout_HLine_Top),
        )

        vseps_positions = (
            (0.65, Question.Layout_VSep_None),
            (0.85, Question.Layout_VLine_LeftAndRight),
            (0.93, Question.Layout_VLine_Left),
            (1.0, Question.Layout_VLine_Right),
        )

        alignment = (
            (0.65, Draw.AlignLeft),
            (0.85, Draw.AlignJustify),
        )

        self.line_spacing = pick_from_list(
            ((0.65, 1.2), (0.85, 1.3), (1.0, 1.5)))
        self.para_spacing = self.line_height * \
            self.line_spacing * (0.25 + (random.random() * 0.5))

        self.text_align = pick_from_list(alignment)
        self.columns = pick_from_list(columns)

        if self.columns > 1:
            vseps_styles = [(p * .5, a) for p, a in vseps_styles]

        self.horizontal_space = pick_from_list(hseps_lines)
        self.horizontal_linestyle = pick_from_list(hseps_styles)
        self.horizontal_lineposition = pick_from_list(hseps_positions)

        self.vertical_space = pick_from_list(vseps_lines)
        self.vertical_linestyle = pick_from_list(vseps_styles)
        self.vertical_lineposition = pick_from_list(vseps_positions)

        self.horizontal_priority = random.random()
        
        self.background_color = generate_color(random.randint(245, 255))
        self.text_color = generate_color(random.randint(4, 96))

        if random.random() > 0.7:
            self.border_color = generate_color(random.randint(4, 96))
        else:
            self.border_color = self.text_color

        self.horizontal_line_width = random.choice(list(range(1, 5)))
        self.vertical_line_width = random.choice(list(range(1, 5)))

        self.question_fill_color = random.choice(
            [self.border_color, self.text_color, "blue", "grey", "green", "purple"])

    def set_measure_only_mode(self, mode):
        self.draw.measure_only = mode

    def adjust_rect_for_style(self, rect, column=0):
        top = rect[0][1]
        if self.horizontal_lineposition == Question.Layout_HLine_Top:
            top += (self.line_height * self.horizontal_space)

        bottom = rect[1][1]
        if self.horizontal_lineposition == Question.Layout_HLine_Bottom:
            bottom -= (self.line_height * self.horizontal_space)

        left = rect[0][0]
        if column != 0:
            if self.columns == 1 and self.vertical_lineposition in \
               (Question.Layout_VLine_Left,
                    Question.Layout_VLine_LeftAndRight):
                left += self.line_height * self.vertical_space
            elif self.columns > 1 and self.vertical_lineposition == \
                    Question.Layout_VLine_ExternalAndInternal:
                left += self.line_height * self.vertical_space
            elif self.columns > 1 and self.vertical_lineposition == \
                    Question.Layout_VLine_Internal:
                if column != 1:
                    left += self.line_height * self.vertical_space

        right = rect[1][0]
        if column != 0:
            if self.columns == 1 and self.vertical_lineposition in (
                    Question.Layout_VLine_Right, Question.Layout_VLine_LeftAndRight):
                right -= self.line_height * self.vertical_space
            elif self.columns > 1 and self.vertical_lineposition == \
                    Question.Layout_VLine_ExternalAndInternal:
                right -= self.line_height * self.vertical_space
            elif self.columns > 1 and self.vertical_lineposition == \
                    Question.Layout_VLine_Internal:
                if column != self.columns:
                    left -= self.line_height * self.vertical_space

        return ((left, top), (right, bottom))

    def draw_columns(self):
        column = 1

        if self.horizontal_priority > 0.5:
            pass

        for rect in self.raw_frames:
            draw_left_hand_side_vertical_line = False
            
            if self.columns == 1 and self.vertical_lineposition in \
                (Question.Layout_VLine_Left, Question.Layout_VLine_LeftAndRight) :
                draw_left_hand_side_vertical_line = True
                
            elif self.columns > 1 and self.vertical_lineposition == \
                Question.Layout_VLine_ExternalAndInternal:
                draw_left_hand_side_vertical_line = True
                
            elif self.columns > 1 and self.vertical_lineposition == \
                    Question.Layout_VLine_Internal and column != 1:
                draw_left_hand_side_vertical_line = True
                
            if draw_left_hand_side_vertical_line :
                line = (rect[0], (rect[0][0], rect[1][1]))
                self.draw.draw_line(
                    line,
                    self.vertical_line_width,
                    style=self.vertical_linestyle)
                
            draw_right_hand_side_vertical_line = False


            if self.columns == 1 and self.vertical_lineposition in \
                (Question.Layout_VLine_Right, Question.Layout_VLine_LeftAndRight) :
                draw_right_hand_side_vertical_line = True
                
            elif self.columns > 1 and self.vertical_lineposition == \
                Question.Layout_VLine_ExternalAndInternal :
                draw_right_hand_side_vertical_line = True
                
            elif self.columns > 1 and self.vertical_lineposition == \
                    Question.Layout_VLine_Internal and column != self.columns:
                draw_right_hand_side_vertical_line = True
                
            if draw_right_hand_side_vertical_line :
                line = ((rect[1][0], rect[0][1]), rect[1])
                self.draw.draw_line(
                    line,
                    self.vertical_line_width,
                    style=self.vertical_linestyle)

            column += 1

    def generate_layout(self):
        available_width = self.width - self.left_margin - self.right_margin
        column_width = available_width / self.columns
       
        self.text_frames = []
        self.raw_frames = []

        for i in range(self.columns):
            rect = (
                (self.left_margin + (i * column_width), self.top_margin),
                (self.left_margin + ((1 + i) * column_width), self.height - self.bottom_margin)
            )

            self.raw_frames.append(rect)
            text_rect = rect  # self.adjust_rect_for_style(rect, i + 1)
            self.text_frames.append(text_rect)

    def get_current_write_location(self):
        """
        This should return a rectangle specifiying where to write the next
        question.
        """
        if self.text_frames:
            return self.text_frames[0]
        
    def rect_fits_in_current_frame(self, remove_rect):
        height = remove_rect[1][1] - remove_rect[0][1]
        current_frame = self.text_frames[0]

        remaining_height = current_frame[1][1] - current_frame[0][1]
        return height < remaining_height

    def update_current_write_location(self, remove_rect):
        """
        Remove rect specifies an area to remove from the available space, either
        because a question has been written to it or because its too small to
        write the next question into.
        """
        height = remove_rect[1][1] - remove_rect[0][1]
        current_frame = self.text_frames[0]

        remaining_height = current_frame[1][1] - current_frame[0][1]
        if height >= remaining_height:
            self.text_frames.remove(current_frame)
        else:
            self.text_frames.remove(current_frame)
            self.text_frames.insert(
                0, ((current_frame[0][0], current_frame[0][1] + height), current_frame[1]))

    def draw_horizontal_styles(self, rect, is_top):
        left = rect[0][0]
        right = rect[1][0]
        line_gap = int(self.horizontal_space * self.line_height * 0.5)
        if line_gap < self.minimum_question_gap * 0.5:
            line_gap = self.minimum_question_gap * 0.5

        if self.horizontal_lineposition == Question.Layout_HLine_Top and is_top:
            line_top = rect[0][1]
            self.draw.draw_line(
                ((left,
                  line_top),
                 (right,
                  line_top)),
                self.horizontal_line_width,
                style=self.horizontal_linestyle)

        elif self.horizontal_lineposition == Question.Layout_HLine_Bottom and not is_top:
            line_top = rect[0][1] + line_gap
            self.draw.draw_line(
                ((left,
                  line_top),
                 (right,
                  line_top)),
                self.horizontal_line_width,
                style=self.horizontal_linestyle)

        return line_gap + line_gap

    def create_page(self):
        self.draw_page_background()

        question_number = random.randint(1, 20)
        while True:
            rect = self.get_current_write_location()
            if rect is None:
                break

            new_rect, scan_rect = self.write_question(question_number)

            if scan_rect and self.rect_fits_in_current_frame(new_rect):
                self.question_text_frames.append(scan_rect)
                self.question_frames.append(inflate_rect(
                    new_rect, self.line_height * 0.5, self.line_height * 0.5))

                if self.draw_debug_rects:
                    #self.draw.rectangle(scan_rect, outline="red")
                    self.draw.rectangle(new_rect, outline="blue")

                question_number += 1

            self.update_current_write_location(new_rect)

    def save(self, size=None):
        if size:
            output_size = size
        else:
            output_size = self.options.get("outputSize")

        dirname = self.options.get("outputDir", "output")

        if self.options.get("save_tiles", False):
            self.save_tiles(dirname, output_size)
        else:
            self.save_page(dirname)

    def save_page(self, dirname, size=None):
        filename = os.path.join(
            dirname, "{}.{}".format(
                self.name, self.image_format))
        
        if size:
            img = self.draw.save(
                filename, rect=(
                    (0, 0), (self.width, self.height)), resize_to=size)

            question_frames = resize_rects(
                self.question_frames, (self.width, self.height), size)
            question_text_frames = resize_rects(
                self.question_text_frames, (self.width, self.height), size)

            #Draw.debug_rects(img, self.question_frames, "1" + ".png")
        else:
            self.draw.save(filename)
            question_frames = self.question_frames
            question_text_frames = self.question_text_frames

        meta_data = {
            "enclosedQuestions": question_frames,
            "enclosedText": question_text_frames,
            "overlapQuestions": question_frames,
            "overlapText": question_text_frames,
        }

        self.save_meta_data(filename, meta_data)

    def save_tiles(self, dirname, size):
        increment = int((self.height - self.width) / 2)

        tiles = [
            ("top", ((0, 0), (self.width, self.width))),
            ("middle", ((0, increment), (self.width, self.width + increment))),
            ("bottom", ((0, increment * 2), (self.width, self.width + (increment * 2)))),
        ]

        for name, tile in tiles:
            filename = os.path.join(
                dirname, "{}-{}.{}".format(self.name, name, self.image_format))

            img = self.draw.save(filename, tile, size)

            question_frames = resize_offset_rects(
                self.question_frames, tile[0], (self.width, self.width), size)
            question_text_frames = resize_offset_rects(
                self.question_text_frames, tile[0], (self.width, self.width), size)

            enclosed_question_frames = [
                r for r in question_frames if rect_enclosed_by_rect(
                    ((0, 0), size), r)]
            enclosed_question_text_frames = [
                r for r in question_text_frames if rect_enclosed_by_rect(
                    ((0, 0), size), r)]
            overlapped_question_frames = [
                r for r in question_frames if overlap_rect(
                    ((0, 0), size), r)]
            overlapped_question_text_frames = [
                r for r in question_text_frames if overlap_rect(
                    ((0, 0), size), r)]

            meta_data = {
                "enclosedQuestions": enclosed_question_frames,
                "enclosedText": enclosed_question_text_frames,
                "overlapQuestions": overlapped_question_frames,
                "overlapText": overlapped_question_text_frames,
            }

            #Draw.debug_rects(img, question_text_frames, filename + ".png")
            self.save_meta_data(filename, meta_data)

    def save_meta_data(self, filename, metadata):
        metadata.update({
            "width": self.width,
            "height": self.height,
            "filename": os.path.basename(filename),
        })

        filepath = os.path.join("{}.json".format(os.path.splitext(filename)[0]))
        tmp_path = "{}.tmp".format(filepath)
        with open(tmp_path, "w") as jsonfile:
            json.dump(metadata, jsonfile, indent=2)
            
        os.rename(tmp_path, filepath)
        
    def get_meta_data_dict(self, filename = None) :
        enclosed_question_frames = overlapped_question_frames = self.question_frames
        enclosed_question_text_frames = overlapped_question_text_frames = self.question_text_frames
            
        meta_data = {
            "enclosedQuestions": enclosed_question_frames,
            "enclosedText": enclosed_question_text_frames,
            "overlapQuestions": overlapped_question_frames,
            "overlapText": overlapped_question_text_frames,            
            "width": self.width,
            "height": self.height
        }
        
        if filename :
            meta_data["filename"] = os.path.basename(filename)
        
        return meta_data
            
    @staticmethod
    def should_write(name, options) :
        if options.get("overwrite", False) :
            return True
        
        name = str(name)
        dirname = options.get("outputDir", "output")
        image_format = options.get("format", "png")

        if options.get("save_tiles", False):
            file_stems = [os.path.join(
                dirname, "{}-{}".format(name, part))
                          for part in ("top","middle","bottom")]
        else:
            file_stems = [os.path.join(dirname, name)]        
        
        for stem in file_stems :
            if not os.path.exists("{}.{}".format(stem, image_format)) :
                return True
            
            if not os.path.exists("{}.json".format(stem)) :
                return True  
            
        return False
    
    def as_zip(self) :
        zipbuffer = BytesIO()
        filename = self.name + ".zip"
        with zipfile.ZipFile(zipbuffer, 'w') as image_zip:
            image_buffer = BytesIO()
            self.draw.image.save(image_buffer, 
                    self.image_format.upper() == "PNG" and "PNG" or "JPEG")
            
            image_zip.writestr(self.name + "." + self.image_format, 
                           data = image_buffer.getvalue())  
            
            metadata = self.get_meta_data_dict()
            json_buffer = json.dumps(metadata, indent=4)
            image_zip.writestr(self.name + ".json", data = json_buffer)
            
            image_zip.filename = filename
            
        return zipbuffer, filename
    
    def save_as_zip(self) :
        dirname= self.options.get("outputDir", "output")
        os.makedirs(dirname, exist_ok = True)
        filename = os.path.join(dirname, self.name + ".zip")
        
        with zipfile.ZipFile(filename, 'w') as image_zip:
            image_buffer = BytesIO()
            self.draw.image.save(image_buffer, 
                    self.image_format.upper() == "PNG" and "PNG" or "JPEG")
            
            image_zip.writestr(self.name + "." + self.image_format, 
                           data = image_buffer.getvalue())  
            
            metadata = self.get_meta_data_dict()
            json_buffer = json.dumps(metadata, indent=4)
            image_zip.writestr(self.name + ".json", data = json_buffer)
                        
        return filename    

    def generate_question_texts(self):
        pass

    def write_question(self, question_number):
        pass
