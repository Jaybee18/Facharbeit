import pygame as pg

def visualize(nn, fade=False):
    pg.init()
    screen = pg.display.set_mode((600, 600))
    input_range = (1, 1)
    start = (0, 0)
    step_size = 0.001

    for i in range(int(input_range[0] / step_size)):
        for j in range(int(input_range[1] / step_size)):
            res = nn.predict([(i*step_size)+start[0], (j*step_size)+start[1]])[0]
            if not fade:
                res = round(res)
            pg.draw.circle(screen, (int(255-res*255), int(res*255), 0), (int(600/int(input_range[0] / step_size)*i), 600-int(600/int(input_range[1] / step_size)*j)), 1)

    condition = True
    while condition:
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                condition = False