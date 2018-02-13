import os

from PIL import Image, ImageDraw, ImageFont


class Draw:
    AlignLeft = 0
    AlignRight = 1
    AlignCenter = 2
    AlignJustify = 3

    def __init__(self, state):
        self.question_state = state
        self.image = None
        self.font = None
        self.draw = None
        self.measure_only = False

    def init_image(self):
        self.image = Image.new('RGB', self.get_image_size())

    def create_draw(self):
        self.cleanup()

        self.font = ImageFont.truetype(
            "fonts/" + self.question_state.font_name,
            self.question_state.font_size)
        self.draw = ImageDraw.Draw(self.image)

    def get_line_height(self):
        return self.draw.textsize("Hg", font=self.font)[1]

    def draw_background(self):
        self.draw.rectangle(((0, 0), self.get_image_size()),
                            fill=self.question_state.background_color)

    def get_image_size(self):
        return (self.question_state.width, self.question_state.height)

    def set_measure_only_mode(self, mode):
        self.measure_only = mode

    def rectangle(self, points, fill=None, outline=None):
        if not self.measure_only:
            self.draw.rectangle(points, fill, outline)

    def draw_line(self, points, width=1, style=None):
        if not self.measure_only:
            self.draw.line(
                points,
                fill=self.question_state.border_color,
                width=width)

    def draw_question_circle(self, top_left):
        if not self.measure_only:
            extra = int(self.question_state.font_size * 0.2)
            point = ((top_left[0] - extra,
                      top_left[1] - extra),
                     (top_left[0] + self.question_state.line_height + extra,
                      top_left[1] + self.question_state.line_height + extra))
            self.draw.ellipse(point,
                              fill=self.question_state.question_fill_color,
                              outline=self.question_state.border_color)

    def __render_text(
            self,
            position,
            line_width,
            word_list,
            align,
            text_color):
        if align in (Draw.AlignLeft, Draw.AlignJustify):
            write_position = position
        else:
            last_text_width, _ = self.draw.textsize(
                " ".join(word_list), font=self.font)
            if align == Draw.AlignRight:
                write_position = (
                    position[0] + (line_width - last_text_width), position[1])
            elif align == Draw.AlignCenter:
                write_position = (
                    position[0] + ((line_width - last_text_width) / 2), position[1])

        if align == Draw.AlignJustify and len(word_list) > 1:
            justify_space = []
            for justify_word in word_list:
                jwidth, _ = self.draw.textsize(justify_word, font=self.font)
                justify_space.append(jwidth)

            extra_space = (line_width - sum(justify_space)
                           ) / (len(word_list) - 1)
            curx = position[0]
            jw_count = 0

            for justify_word, jwidth in zip(word_list, justify_space):
                jw_count += 1
                if jw_count == len(word_list):
                    curx = position[0] + line_width - jwidth

                if not self.measure_only:
                    self.draw.text((curx, position[1]), justify_word,
                                   font=self.font, fill=text_color)

                curx += jwidth + extra_space

        elif not self.measure_only:
            self.draw.text(write_position, " ".join(word_list),
                           font=self.font, fill=text_color)

    def draw_text(
            self,
            position,
            width,
            text,
            align=AlignLeft,
            first_line_offset=0,
            force_color=None):

        if force_color:
            text_color = force_color
        else:
            text_color = self.question_state.text_color

        words = text.split(' ')
        word_list = []
        total_height = 0
        counter = 0

        for word in words:
            counter += 1
            if total_height == 0:
                line_width = width - first_line_offset
            else:
                line_width = width

            text_width, text_height = self.draw.textsize(
                " ".join(word_list + [word]), font=self.font)

            if text_width > line_width or counter == len(words):
                if text_width <= line_width or not word_list:
                    word_list.append(word)
                    if align == Draw.AlignJustify:
                        align = Draw.AlignLeft

                if total_height == 0 and first_line_offset:
                    offset_position = (
                        position[0] + first_line_offset, position[1])
                    self.__render_text(
                        offset_position,
                        line_width,
                        word_list,
                        align,
                        text_color)
                else:
                    self.__render_text(
                        position, line_width, word_list, align, text_color)

                total_line_height = int(
                    text_height * self.question_state.line_spacing)
                position = (position[0], position[1] + total_line_height)
                total_height += total_line_height

                if text_width > width and counter == len(words):
                    self.__render_text(
                        position, width, [word], align, text_color)
                    total_height += total_line_height

                word_list = []

            word_list.append(word)

        return total_height

    def save(self, filename, rect=None, resize_to=None):
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        if rect is None and resize_to is None:
            img = self.image
        else:
            img = self.copy_rect(rect, resize_to)

        img.save(filename)
        
        return img

    def copy_rect(self, rect, resize_to):
        img = Image.new(
            'RGB',
            (rect[1][0] -
             rect[0][0],
             rect[1][1] -
             rect[0][1]))
        img_src = self.image.crop(
            (rect[0][0], rect[0][1], rect[1][0], rect[1][1]))
        img.paste(img_src)
        img = img.resize(resize_to, Image.BILINEAR)
        return img

    def cleanup(self):
        if self.draw:
            del self.draw
            self.draw = None

    @staticmethod
    def debug_rects(img, rectangles, save_as_file):
        draw = ImageDraw.Draw(img)
        for rect in rectangles:
            draw.rectangle(rect, outline="red")
        img.save(save_as_file)
