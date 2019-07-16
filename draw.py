import math
import sys

from PIL import Image, ImageDraw


MODE = "RGBA"
SIZE = (26, 26)
BGCOLOR = "#FFFFFF"
DOTCOLOR = "#000000"
LINECOLOR = "#111111"
DARK = "#000000"
GRID = (6, 6)
BITS = 60
BIT_GRID = [
      (0, 1),   (1, 2),   (2, 3),   (3, 4),   (4, 5),   (0, 6),   (1, 7),   (2, 8),   (3, 9),  (4, 10),  (5, 11),
      (6, 7),   (7, 8),   (8, 9),  (9, 10), (10, 11),  (6, 12),  (7, 13),  (8, 14),  (9, 15), (10, 16), (11, 17),
    (12, 13), (13, 14), (14, 15), (15, 16), (16, 17), (12, 18), (13, 19), (14, 20), (15, 21), (16, 22), (17, 23),
    (18, 19), (19, 20), (20, 21), (21, 22), (22, 23), (18, 24), (19, 25), (20, 26), (21, 27), (22, 28), (23, 29),
    (24, 25), (25, 26), (26, 27), (27, 28), (29, 29), (24, 30), (25, 31), (26, 32), (27, 33), (28, 34), (29, 35),
    (30, 31), (31, 32), (32, 33), (33, 34), (34, 35)
]
DOTS = []
DOTRADIUS = 1
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
          103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]
CHARS = []
LINES = []


def draw_dots(draw, offset_x=0, offset_y=0):
    DOTS.clear()
    for y in range(GRID[1]):
        for x in range(GRID[0]):
            gridx = (x * (SIZE[0] - 1) // (GRID[0] - 1)) - x + offset_x
            gridy = (y * (SIZE[1] - 1) // (GRID[1] - 1)) - y + offset_y
            # print((gridx, gridy, gridx + DOTRADIUS, gridy + DOTRADIUS))
            draw.ellipse((gridx, gridy, gridx + DOTRADIUS, gridy + DOTRADIUS), fill=DOTCOLOR, outline=DARK)
            DOTS.append([gridx, gridy])


def draw_lines(draw, snake_chars):
    for i, character in enumerate(snake_chars):
        if character == '1':
            selected = BIT_GRID[i]
            # print("drawing the grid line from %s, %s" % selected)
            gridax = DOTS[selected[0]][0]
            griday = DOTS[selected[0]][1]
            gridbx = DOTS[selected[1]][0]
            gridby = DOTS[selected[1]][1]
            xy = (gridax, griday, gridbx, gridby)
            print("guessing coords %s, %s, %s, %s\n" % xy)
            draw.line(xy, fill=LINECOLOR, width=1, joint=None)


def single_image_output(snake_chars, snake_id, trans=False):
    snake_png = "snake_%s.png" % snake_id
    print("snake img %s" % snake_png)
    im = init_image(MODE, SIZE, BGCOLOR, trans=False)
    draw = get_draw(im)
    draw_dots(draw)
    # print("snake chars to draw is: %s" % snake_chars)
    draw_lines(draw, snake_chars)
    im.save(snake_png, "PNG")


def append_output(snake_chars, offset_x, offset_y, canvas_draw):
    draw_dots(canvas_draw, offset_x, offset_y)
    # print("snake chars to draw is: %s" % snake_chars)
    draw_lines(canvas_draw, snake_chars)


def get_next_dimensions(total_word_length, can_x, snake_id):
    page_margin_x = 2
    page_margin_y = 2
    vertical_line_margin = 5
    horizontal_char_margin = 3
    horizontal_word_margin = 12
    # x props
    num_spaces = len([c for c in CHARS if c == 0])
    num_chars = len([c for c in CHARS if c == 1])
    start_position_x = page_margin_x + (num_spaces * horizontal_word_margin) + (
                num_chars * (SIZE[0] + horizontal_char_margin))
    word_len_x = total_word_length * (SIZE[0] + horizontal_char_margin)
    print("page_margin_x: %s; page_margin_y: %s; vertical_line_margin: %s; horizontal_char_margin: %s; horizontal_word_margin: %s" % (page_margin_x, page_margin_y, vertical_line_margin, horizontal_char_margin, horizontal_word_margin))
    print("num_spaces: %s; num_chars: %s; start_position_x: %s; word_len_x: %s" % (num_spaces, num_chars, start_position_x, word_len_x))
    if snake_id == 0:
        print("snake 0")
        # do we have enough space in this line to write this whole word; if not, advance now to next line
        if (start_position_x + word_len_x) >= (can_x + page_margin_x):
            # new line
            LINES.append(1)
            CHARS.clear()
            # reset x props
            num_spaces = len([c for c in CHARS if c == 0])
            num_chars = len([c for c in CHARS if c == 1])
            start_position_x = page_margin_x + (num_spaces * horizontal_word_margin) + (
                        num_chars * (SIZE[0] + horizontal_char_margin))
    offset_y = page_margin_y + (len(LINES) * (SIZE[1] + vertical_line_margin))
    offset_x = start_position_x
    CHARS.append(1)
    if snake_id == (total_word_length - 1):
        # append a space
        print("append space")
        CHARS.append(0)
    return offset_x, offset_y


def loop_snakes(val, trans=False, canvas_draw=None, can_x=0):
    binstr = "{0:b}".format(val)[::-1]  # reversed
    total_word_length = math.ceil(len(binstr) / BITS)
    # for each BITS characters starting from the left: (the resulting snake will be little-endian)
    snake_id = 0
    while True:
        # print("snake id %s" % snake_id)
        # print("binstr is now %s" % binstr)
        break_out = False
        if len(binstr) < BITS:
            snake_chars = binstr
            break_out = True
        else:
            snake_chars, binstr = binstr[:BITS], binstr[BITS:]
        if canvas_draw is None:
            single_image_output(snake_chars, snake_id, trans=trans)
        else:
            offset_x, offset_y = get_next_dimensions(total_word_length, can_x, snake_id)
            append_output(snake_chars, offset_x, offset_y, canvas_draw)
        snake_id += 1
        if break_out:
            break


def draw_snakes_main(words, trans=False, single_word_images=True, can_x=0, can_y=0):
    canvas_draw = None
    can_im = None
    if single_word_images is False:
        print("dsm: single word")
        can_im = init_image(MODE, [can_x, can_y], BGCOLOR, trans=trans)
        canvas_draw = get_draw(can_im)
    for word in words.split():
        val = calculate_word(word)
        loop_snakes(val, trans=trans, canvas_draw=canvas_draw, can_x=can_x)
    if single_word_images is False:
        can_im.save("canvas.png", "PNG")


def init_image(mode, size, bgcolor, trans=False):
    im = Image.new(mode, size, bgcolor)
    if trans:
        trans = [(255, 255, 255, 0) for _ in range(size[0] * size[1])]
        im.putdata(trans)
    return im


def get_draw(im):
    return ImageDraw.Draw(im)


def test():
    im = init_image(MODE, SIZE, BGCOLOR, trans=False)
    draw = get_draw(im)
    draw_dots(draw)
    im.save("test.png")


def calculate_word(word):
    """The mathematical value of word is:

    nth character: take the nth prime and raise it to the power of char(n) of word; a=1, z=26

    """
    val = 1
    for i, character in enumerate(word):
        val = val * (PRIMES[i] ** (ord(character.upper()) - 64))
    return val


def main(word, single_word_images, can_x, can_y, trans):
    if trans == 1:
        trans = True
    else:
        trans = False
    if single_word_images == 1:
        print("single word images!")
        single_word_images = True
    else:
        print("single big canvas!")
        single_word_images = False
    draw_snakes_main(word, trans=trans, single_word_images=single_word_images, can_x=can_x, can_y=can_y)


if __name__ == "__main__":
    if len(sys.argv) != 6:
        raise Exception("draw.py word single_word_images(1|0) can_x(0|255) can_y(0|255) trans(0|1)")
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
