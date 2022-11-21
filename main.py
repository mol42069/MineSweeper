import pygame as py
import random as rnd

py.init()
screen_size = (1920, 1080)

start_img = py.image.load('images/starting_img.png')
marked_img = py.image.load('images/marked_img.png')
bomb_img = py.image.load('images/bomb_img.png')


class Rectangle:

    def __init__(self, size, neighbors, x, y, starting_img):
        self.starting_img = starting_img
        self.size = size
        self.x = x
        self.y = y
        self.neighbors = neighbors
        self.mine = False
        self.flag = False
        self.num = 0
        self.rect = py.Rect(x, y, size, size)

    def init(self):

        display.blit(self.starting_img, (self.rect.x, self.rect.y))


def init_display_rec(n_graph, starting_img, x=64, y=36, rec_size=30):
    rectangles = []
    for yy in range(0, y):
        rectangles_x = []
        for xx in range(0, x):
            neighbors = n_graph[(yy, xx)]
            rectangles_x.append(Rectangle(rec_size, neighbors, xx * 30, yy * 30, starting_img))
            rectangles_x[xx].init()
        rectangles.append(rectangles_x)
    py.display.flip()
    return rectangles


def generate_neighbors():                                   # generates a dictionary which tells us what the neighbors
    n_graph = {}                                              # of any given rectangle is and returns this dictionary
    for y in range(0, 36):
        for x in range(0, 64):

            if y == 0 or y == 35:
                if y == 0:
                    if x == 0:
                        n_graph.update({(y, x): [(y, x + 1), (y + 1, x), (y + 1, x + 1)]})

                    elif x == 63:
                        n_graph.update({(y, x): [(y + 1, x), (y, x - 1), (y + 1, x - 1)]})

                    else:
                        n_graph.update({(y, x): [(y + 1, x), (y, x + 1), (y, x - 1), (y + 1, x + 1), (y + 1, x - 1)]})
                elif y == 35:
                    if x == 0:
                        n_graph.update({(y, x): [(y - 1, x), (y, x + 1), (y - 1, x + 1)]})

                    elif x == 63:
                        n_graph.update({(y, x): [(y - 1, x), (y, x - 1), (y - 1, x - 1)]})

                    else:
                        n_graph.update({(y, x): [(y - 1, x), (y, x + 1), (y, x - 1), (y - 1, x - 1), (y - 1, x + 1)]})

            elif x == 0 or x == 63:
                if x == 0:
                    n_graph.update({(y, x): [(y + 1, x), (y - 1, x), (y, x + 1), (y + 1, x + 1), (y + 1, x - 1)]})

                if x == 63:
                    n_graph.update({(y, x): [(y + 1, x), (y - 1, x), (y, x - 1), (y + 1, x - 1), (y - 1, x + 1)]})

            else:
                n_graph.update({(y, x): [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1), (y + 1, x + 1), (y + 1, x - 1),
                                (y - 1, x + 1), (y - 1, x - 1)]})

    return n_graph


def generate_bombs(c_difficulty, c_rectangles):

    for iy, yy in enumerate(c_rectangles):
        for ix, xx in enumerate(yy):
            if rnd.randint(0, c_difficulty * 10):
                rectangles[iy][ix].mine = True
            else:
                pass
    return rectangles


def give_numbers(t_graph, t_rectangles):
    for iy, yy in enumerate(t_rectangles):
        for ix, xx in enumerate(t_rectangles):
            for z in t_graph[(iy, ix)]:
                if t_rectangles[z[0]][z[1]].mine:
                    t_rectangles[iy][ix].num += 1

    return t_rectangles


display = py.display.set_mode(screen_size, py.FULLSCREEN)
running = True
# generate the dictionary for the neighbors

graph = generate_neighbors()

# initialize the rectangles in a pattern
rectangles = init_display_rec(graph, start_img, 64, 36, 30)

difficulty = 5          # the higher, the more bombs there are if 0 there are none

# init the bombs

rectangles = generate_bombs(difficulty, rectangles)

# init the number of bombs around the rectangle

rectangles = give_numbers(graph, rectangles)


while running:

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
