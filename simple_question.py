import random
import string
from functools import partial

from draw import Draw
from base_question import Question


class SimpleQuestion(Question):
    ROMAN_DIGITS = [
        "i",
        "ii",
        "iii",
        "iv",
        "v",
        "vi",
        "vii",
        "viii",
        "ix",
        "x",
        "xi"
        "xii",
        "xiii",
        "xiv",
        "xv"]

    def generate_page(self):
        super(SimpleQuestion, self).generate_page()

        self.para_margin = int(random.choice(
            [0, 2.2 * self.line_height, 1.8 * self.line_height]))
        self.sub_para_prefix = int(random.randint(0, 2) * self.line_height * 0.3)
        if self.para_margin:
            self.sub_para_margin = int(self.para_margin)
        else:
            self.sub_para_margin = int(random.choice(
                [0, 2.2 * self.line_height, 1.8 * self.line_height]))

        self.sub_para_terminator = random.choice([".", ")", ")."])
        if random.random() < 0.5:
            self.sub_para_digits = string.ascii_lowercase
        else:
            self.sub_para_digits = SimpleQuestion.ROMAN_DIGITS

    def get_horizontal_padding(self):
        return self.vertical_space * self.line_height * 0.5

    def get_text_rect(self, rect):
        hspace = self.get_horizontal_padding()
        return ((rect[0][0] + hspace, rect[0][1]),
                (rect[1][0] - hspace, rect[1][1]))

    def write_question_header(self, rect):
        text_rect = self.get_text_rect(rect)

        return self.draw_horizontal_styles(text_rect, True)

    def write_question_footer(self, rect, height_consumed):
        text_rect = self.get_text_rect(rect)

        bottom_rect = (
            (text_rect[0][0],
             rect[0][1] +
                height_consumed),
            text_rect[1])

        return self.draw_horizontal_styles(bottom_rect, False)

    def write_paragraphs(
        self,
        rect,
        question_number,
        paragraph,
        subparagraph,
        endparagraph,
        height_consumed):
        text_rect = self.get_text_rect(rect)

        width = text_rect[1][0] - text_rect[0][0]
        paragraph_number = 0
        text_height = 0
        top = text_rect[0][1] + height_consumed

        for text in paragraph:
            left = text_rect[0][0] + self.para_margin
            offset = 0
            if paragraph_number == 0:
                if self.para_margin == 0:
                    self.draw.draw_question_circle(
                        (text_rect[0][0], top + text_height))
                    offset = self.font_size * 1.5
                    number_color = self.background_color
                else:
                    number_color = self.text_color

                self.draw.draw_text(
                    (text_rect[0][0],
                     top + text_height),
                    width,
                    str(question_number) + ".",
                    Draw.AlignLeft,
                    force_color=number_color)

            text_height += self.draw.draw_text((
                left,
                top + text_height),
                width - self.para_margin,
                text,
                self.text_align,
                first_line_offset=offset)

            paragraph_number += 1
            if paragraph_number != len(paragraph) or (subparagraph or endparagraph):
                text_height += self.para_spacing

        paragraph_number = 0
        for text in subparagraph:
            if self.sub_para_margin:
                self.draw.draw_text(
                    (text_rect[0][0] +
                     self.para_margin +
                     self.sub_para_prefix,
                     top +
                     text_height),
                    width -
                    self.para_margin -
                    self.sub_para_prefix,
                    self.sub_para_digits[paragraph_number] +
                    self.sub_para_terminator,
                    self.text_align)

            text_height += self.draw.draw_text(
                (text_rect[0][0] +
                 self.para_margin +
                 self.sub_para_prefix +
                 self.sub_para_margin,
                 top +
                 text_height),
                width -
                self.para_margin -
                self.sub_para_prefix -
                self.sub_para_margin,
                text,
                self.text_align)

            paragraph_number += 1
            if paragraph_number != len(subparagraph) or endparagraph:
                text_height += self.para_spacing

        paragraph_number = 0
        for text in endparagraph:
            text_height += self.draw.draw_text((
                text_rect[0][0] + self.para_margin,
                top + text_height),
                width - self.para_margin,
                text,
                self.text_align)

            paragraph_number += 1
            if paragraph_number != len(endparagraph):
                text_height += self.para_spacing

        scan_rect = \
        (
            (
                text_rect[0][0] - self.line_height * 0.5, 
                text_rect[0][1] + height_consumed - self.line_height * 0.5
            ), 
            (
                text_rect[1][0] + self.line_height * 0.5, 
                text_rect[0][1] + height_consumed + text_height + self.line_height * 0.5
            ), 
        )

        return scan_rect, text_height

    def calculate_area_consumed(self, rect, height_consumed):
        return (rect[0], (rect[1][0], rect[0][1] + height_consumed))

    def write_simple_question(self, number, rect, text):
        """
        Number = 1-20, a-g
        Usually in a margin but can be indented.
        Often bold and followed by dot or bracket.
        """
        height = self.write_question_header(rect)

        scan_rect, text_height = self.write_paragraphs(
            rect, number, text, [], [], height)

        height += text_height
        height += self.write_question_footer(rect, height)

        return self.calculate_area_consumed(rect, height), scan_rect

    def write_multipart_question(
            self,
            number,
            rect,
            text,
            subparagraph,
            endparagraph):
        height = self.write_question_header(rect)

        scan_rect, text_height = self.write_paragraphs(
            rect, number, text, subparagraph, endparagraph, height)

        height += text_height
        height += self.write_question_footer(rect, height)

        return self.calculate_area_consumed(rect, height), scan_rect

    def generate_question_texts(self, sentence=False):
        if sentence:
            return self.generator.generate_sentence()[2]
        else:
            return self.generator.generate_sentence()[2]

    def write_question(self, question_number):
        trys = 0
        new_rect = scan_rect = None
        while True:
            rect = self.get_current_write_location()
            if rect is None:
                break

            trys += 1
            self.set_measure_only_mode(True)

            subparagraph = []
            endparagraph = []
            paragraph = [self.generate_question_texts()]
            if trys < 3:
                if random.random() < 0.5:
                    paragraph.append(self.generate_question_texts())

                if random.random() < 0.75:
                    for _ in range(random.randint(1, 3)):
                        subparagraph.append(self.generate_question_texts(True))

            if trys < 2 and random.random() < 0.5:
                endparagraph.append(self.generate_question_texts())

            if subparagraph or endparagraph:
                func = partial(self.write_multipart_question, question_number,
                               rect, paragraph, subparagraph, endparagraph)
            else:
                func = partial(
                    self.write_simple_question,
                    question_number,
                    rect,
                    paragraph)

            new_rect, scan_rect = func()
            if self.rect_fits_in_current_frame(new_rect):
                self.set_measure_only_mode(False)
                new_rect, scan_rect = func()
                break

            elif trys > 4:
                scan_rect = None
                break

        return new_rect, scan_rect
