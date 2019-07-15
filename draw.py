import math

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


def draw_dots(draw):
    DOTS.clear()
    for x in range(GRID[0]):
        for y in range(GRID[1]):
            gridx = (x * (SIZE[0] - 1) // (GRID[0] - 1)) - x
            gridy = (y * (SIZE[1] - 1) // (GRID[1] - 1)) - y
            print((gridx, gridy, gridx + DOTRADIUS, gridy + DOTRADIUS))
            draw.ellipse((gridx, gridy, gridx + DOTRADIUS, gridy + DOTRADIUS), fill=DOTCOLOR, outline=DARK)
            DOTS.append([gridx, gridy])


def draw_lines(draw, snake_chars):
    for i, character in enumerate(snake_chars):
        if character == '1':
            selected = BIT_GRID[i]
            print("drawing the grid line from %s, %s" % selected)
            gridax = DOTS[selected[0]][0]
            griday = DOTS[selected[0]][1]
            gridbx = DOTS[selected[1]][0]
            gridby = DOTS[selected[1]][1]
            xy = (gridax, griday, gridbx, gridby)
            print("guessing coords %s, %s, %s, %s\n" % xy)
            draw.line(xy, fill=LINECOLOR, width=1, joint=None)


def draw_snakes(val):
    binstr = "{0:b}".format(val)[::-1]  # reversed
    # for each sixty characters starting from the left: (the resulting snake will be little-endian)
    snake_id = 0
    while True:
        print("snake id %s" % snake_id);
        snake_png = "snake_%s.png" % snake_id
        print("snake img %s" % snake_png);
        im = init_image()
        draw = get_draw(im)
        draw_dots(draw)
        break_out = False
        if len(binstr) < BITS:
            print("done with binstr");
            snake_chars = binstr
            break_out = True
        else:
            snake_chars, binstr = binstr[:BITS], binstr[BITS:]
        print("snake chars to draw is: %s" % snake_chars)
        print("binstr is now %s" % binstr)
        draw_lines(draw, snake_chars)
        im.save(snake_png, "PNG")
        snake_id += 1
        if break_out:
            break


def draw_snakes_main(word):
    val = calculate_word(word)
    draw_snakes(val)


def init_image():
    # trans = [(255, 255, 255, 0) for _ in range(limit_y * limit_x)]
    # im.putdata(trans)
    return Image.new(MODE, SIZE, BGCOLOR)


def get_draw(im):
    return ImageDraw.Draw(im)


def test():
    im = init_image()
    draw = get_draw(im)
    draw_dots(draw)
    im.save("test.png")


def calculate_word(word):
    """The mathematical value of word is:

    nth character: take the nth prime and raise it to the power of char(0) of word; a=1, z=26

    """
    val = 1
    for i, character in enumerate(word):
        val = val * (PRIMES[i] ** (ord(character.upper()) - 64))
    return val
