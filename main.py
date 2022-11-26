import pygame as py
import random as rnd
import sys
import time

py.init()
screen_size = (1920, 1080)
rec_size = 120
rec_x = int(screen_size[0] / rec_size)
rec_y = int(screen_size[1] / rec_size)

# importing all the necessary images

start_img = py.image.load('images/starting_img.png')
marked_img = py.image.load('images/marked_img.png')
bomb_img = py.image.load('images/bomb_img.png')
zero_img = py.image.load('images/0_img.png')
one_img = py.image.load('images/1_img.png')
two_img = py.image.load('images/2_img.png')
three_img = py.image.load('images/3_img.png')
four_img = py.image.load('images/4_img.png')
five_img = py.image.load('images/5_img.png')
six_img = py.image.load('images/6_img.png')
seven_img = py.image.load('images/7_img.png')
eight_img = py.image.load('images/8_img.png')


class Rectangle:

    def __init__(self, size, neighbors, x, y):
        self.starting_img = py.transform.scale(start_img, (rec_size, rec_size))
        self.marked_img = py.transform.scale(marked_img, (rec_size, rec_size))
        self.revealed_img = images_io[0]
        self.size = size
        self.x = x
        self.y = y
        self.neighbors = neighbors
        self.mine = False
        self.flag = False
        self.revealed = False
        self.num = 0
        self.rect = py.Rect(x, y, size, size)

    def init(self):

        display.blit(self.starting_img, (self.rect.x, self.rect.y))

    def reset(self):
        self.num = 0

    def click(self):
        global left_clicked, right_clicked, pos

        # checking if mouse is on the rectangle

        if self.rect.collidepoint(pos):

            # here we check for the left mouse button:

            if py.mouse.get_pressed()[0] == 1 and not left_clicked:
                left_clicked = True
                self.l_click()
                return True

            elif py.mouse.get_pressed()[0] != 1:
                left_clicked = False

            # here we check for the right mouse button:

            if py.mouse.get_pressed()[2] == 1 and not right_clicked:
                right_clicked = True
                if not self.flag and not self.revealed:
                    # here we draw the flag on this rectangle
                    self.flag = True
                    display.blit(self.marked_img, (self.rect.x, self.rect.y))
                elif not self.revealed:
                    self.flag = False

                    # here we draw the starting img on this rectangle
                    display.blit(self.starting_img, (self.rect.x, self.rect.y))
            elif py.mouse.get_pressed()[2] != 1:
                right_clicked = False

        return False

    def reveal(self):
        display.blit(self.revealed_img, (self.rect.x, self.rect.y))

    def l_click(self):
        global first_click, rectangles
        if not self.flag:
            if not self.revealed:
                # we check if this rectangle is already revealed and then if it is a mine
                if self.mine and first_click:   # on first click we make the mine and surroundings disappear
                    self.mine = False
                if first_click:
                    first_click = False
                    reset_nums()
                    for n in self.neighbors:
                        rectangles[n[0]][n[1]].mine = False
                    give_numbers()
                if self.mine:
                    game_over()
                else:
                    display.blit(self.revealed_img, (self.rect.x, self.rect.y))
                    self.revealed = True


def check_if_ne(iy, ix):
    global rectangles, graph, visited

    for n in graph[iy, ix]:
        if n not in visited:
            visited.append(n)
            try:
                rectangles[n[0]][n[1]].l_click()
                if rectangles[n[0]][n[1]].num == 0:
                    check_if_ne(n[0], n[1])
            except IndexError:
                pass


def game_over():
    global running
    global rectangles
    for yy in rectangles:
        for xx in yy:
            xx.reveal()

    py.display.flip()
    py.time.delay(2000)
    running = False
    # TODO: MAKE AN GAME OVER SCREEN


def init_display_rec(n_graph):
    global rec_y, rec_x, rec_size
    t_rectangles = []
    for yy in range(0, rec_y):
        rectangles_x = []
        for xx in range(0, rec_x):
            neighbors = n_graph[(yy, xx)]
            rectangles_x.append(Rectangle(rec_size, neighbors, xx * rec_size, yy * rec_size))
            rectangles_x[xx].init()
        t_rectangles.append(rectangles_x)
    py.display.flip()
    return t_rectangles


def generate_neighbors():                                   # generates a dictionary which tells us what the neighbors
    global rec_x, rec_y
    n_graph = {}                                            # of any given rectangle is and returns this dictionary
    for y in range(0, rec_y):
        for x in range(0, rec_x):

            if y == 0 or y == rec_y:
                if y == 0:
                    if x == 0:
                        n_graph.update({(y, x): [(y, x + 1), (y + 1, x), (y + 1, x + 1)]})

                    elif x == rec_x:
                        n_graph.update({(y, x): [(y + 1, x), (y, x - 1), (y + 1, x - 1)]})

                    else:
                        n_graph.update({(y, x): [(y + 1, x), (y, x + 1), (y, x - 1), (y + 1, x + 1), (y + 1, x - 1)]})
                elif y == rec_y:
                    if x == 0:
                        n_graph.update({(y, x): [(y - 1, x), (y, x + 1), (y - 1, x + 1)]})

                    elif x == rec_x:
                        n_graph.update({(y, x): [(y - 1, x), (y, x - 1), (y - 1, x - 1)]})

                    else:
                        n_graph.update({(y, x): [(y - 1, x), (y, x + 1), (y, x - 1), (y - 1, x - 1), (y - 1, x + 1)]})

            elif x == 0 or x == rec_x:
                if x == 0:
                    n_graph.update({(y, x): [(y + 1, x), (y - 1, x), (y, x + 1), (y + 1, x + 1), (y - 1, x + 1)]})

                if x == rec_x:
                    n_graph.update({(y, x): [(y + 1, x), (y - 1, x), (y, x - 1), (y + 1, x - 1),
                                             (y - 1, x + 1)]})

            else:
                n_graph.update({(y, x): [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1), (y + 1, x + 1), (y + 1, x - 1),
                                         (y - 1, x + 1), (y - 1, x - 1)]})

    return n_graph


def generate_bombs():
    global rectangles, difficulty, total_bombs

    for iy, yy in enumerate(rectangles):
        for ix, xx in enumerate(yy):
            if rnd.randint(0, difficulty) == 1:
                rectangles[iy][ix].mine = True
                total_bombs += 1


def give_numbers():
    global graph, rectangles
    for iy in range(0, rec_y):
        for ix in range(0, rec_x):
            for z in graph[(iy, ix)]:
                try:
                    if rectangles[z[0]][z[1]].mine:
                        rectangles[iy][ix].num += 1
                except IndexError:
                    pass

            if rectangles[iy][ix].mine:
                rectangles[iy][ix].revealed_img = py.transform.scale(bomb_img, (rec_size, rec_size))
            else:
                rectangles[iy][ix].revealed_img = images_io[rectangles[iy][ix].num]


def reset_nums():
    global graph, rectangles
    for iy in range(0, rec_y):
        for ix in range(0, rec_x):
            rectangles[iy][ix].reset()


def check_rec():
    global rectangles, graph, pos
    for iy in range(0, rec_y):
        for ix in range(0, rec_x):
            if rectangles[iy][ix].click():
                if rectangles[iy][ix].num == 0:
                    check_if_ne(iy, ix)


def check_if_won():
    global rectangles, total_bombs, start_time, running
    for yy in rectangles:
        for xx in yy:
            if xx.mine and xx.flag:
                total_bombs -= 1

    if total_bombs == 0:
        print("YOU WON!!!!!")
        won_time = time.time()
        total_time = won_time - start_time
        if total_time > 60:
            total_time = total_time / 60

        print(f"in: {total_time} s")


sys.setrecursionlimit(5000)
stop = True
# TODO: MAKE AN STARTING SCREEN

while stop:
    # images in list in order:
    images_io = [py.transform.scale(zero_img, (rec_size, rec_size)),
                 py.transform.scale(one_img, (rec_size, rec_size)),
                 py.transform.scale(two_img, (rec_size, rec_size)),
                 py.transform.scale(three_img, (rec_size, rec_size)),
                 py.transform.scale(four_img, (rec_size, rec_size)),
                 py.transform.scale(five_img, (rec_size, rec_size)),
                 py.transform.scale(six_img, (rec_size, rec_size)),
                 py.transform.scale(seven_img, (rec_size, rec_size)),
                 py.transform.scale(eight_img, (rec_size, rec_size))]

    display = py.display.set_mode(screen_size, py.FULLSCREEN)
    running = True
    left_clicked = False
    right_clicked = False
    # generate the dictionary for the neighbors

    graph = generate_neighbors()

    # initialize the rectangles in a pattern
    rectangles = init_display_rec(graph)

    difficulty = 5          # the higher, the more bombs there are if 0 there are none

    total_bombs = 0

    # init the bombs

    generate_bombs()

    # init the number of bombs around the rectangle

    give_numbers()

    start_time = time.time()
    first_click = True

    while running:
        visited = []
        # we get the position of the mouse.
        pos = py.mouse.get_pos()
        check_rec()
        py.display.flip()
        check_if_won()

        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
                stop = False

    end_time = time.time()
