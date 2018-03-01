def inflate_rect(rect, inflate_by_x, inflate_by_y):
    return (
        (
            rect[0][0] - inflate_by_x,
            rect[0][1] - inflate_by_y
        ),
        (
            rect[1][0] + inflate_by_x,
            rect[1][1] + inflate_by_y
        ),
    )

def resize_rects(rect_list, current_size, new_size):
    new_rects = []
    xscale = new_size[0] / current_size[0]
    yscale = new_size[1] / current_size[1]

    for rect in rect_list:
        new_rects.append((
            (rect[0][0] * xscale, rect[0][1] * yscale),
            (rect[1][0] * xscale, rect[1][1] * yscale)
        ))

    return new_rects

## The following are only used by image tiler

def offset_rects(rect_list, offset):
    new_rects = []
    xoffset = -offset[0]
    yoffset = -offset[1]

    for rect in rect_list:
        new_rect = (
            (rect[0][0] + xoffset, rect[0][1] + yoffset),
            (rect[1][0] + xoffset, rect[1][1] + yoffset)
        )
        new_rects.append(new_rect)

    return new_rects

def resize_offset_rects(rect_list, offset, current_size, new_size):
    new_rects = []
    xoffset = -offset[0]
    yoffset = -offset[1]

    for rect in rect_list:
        new_rects.append((
            (rect[0][0] + xoffset, rect[0][1] + yoffset),
            (rect[1][0] + xoffset, rect[1][1] + yoffset)
        ))

    return resize_rects(new_rects, current_size, new_size)

def rect_enclosed_by_rect(enclosing_rect, test_rect):
    return (
        (test_rect[0][0] >= enclosing_rect[0][0]) and
        (test_rect[0][0] <= enclosing_rect[1][0]) and
        (test_rect[1][0] >= enclosing_rect[0][0]) and
        (test_rect[1][0] <= enclosing_rect[1][0]) and
        (test_rect[0][1] >= enclosing_rect[0][1]) and
        (test_rect[0][1] <= enclosing_rect[1][1]) and
        (test_rect[1][1] >= enclosing_rect[0][1]) and
        (test_rect[1][1] <= enclosing_rect[1][1])
    )

def overlap_rect(enclosing_rect, test_rect):
    return (
        ((test_rect[0][0] >= enclosing_rect[0][0]) and
         (test_rect[0][0] <= enclosing_rect[1][0])) or
        ((test_rect[1][0] >= enclosing_rect[0][0]) and
         (test_rect[1][0] <= enclosing_rect[1][0])) or
        ((test_rect[0][1] >= enclosing_rect[0][1]) and
         (test_rect[0][1] <= enclosing_rect[1][1])) or
        ((test_rect[1][1] >= enclosing_rect[0][1]) and
         (test_rect[1][1] <= enclosing_rect[1][1]))
    )


