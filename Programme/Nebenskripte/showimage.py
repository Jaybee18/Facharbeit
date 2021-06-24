import pygame, time

def relu(x):
    return (x if x < 255 else 255) if x > 0 else 0

def showImage(imagearray:list, isGrayScale=False, loopTillClosed:bool=True, tile_size=(10, 10)):
    height = len(imagearray)
    width = len(imagearray[0])

    pygame.init()
    screen = pygame.display.set_mode((tile_size[0] * width, tile_size[1]*height))

    for i in range(height):
        for j in range(width):
            tmp = float(imagearray[i][j])
            if(type(tmp) == float):
                tmp = (tmp, tmp, tmp)
            if isGrayScale:
                color = (relu(tmp[0]*255), relu(tmp[1]*255), relu(tmp[2]*255))
                # don't draw black pixels onto a black background
                if sum(color) == 0:
                    continue
                pygame.draw.rect(screen, color, pygame.Rect(j*tile_size[0], i*tile_size[1], tile_size[0], tile_size[1]))
            else:
                try:
                    pygame.draw.rect( screen, (tmp[ 0 ], tmp[ 1 ], tmp[ 2 ]), pygame.Rect( j * tile_size[ 0 ], i * tile_size[ 1 ], tile_size[ 0 ], tile_size[ 1 ] ) )
                except IndexError:
                    pygame.draw.rect( screen, (tmp[0], tmp[0], tmp[0]), pygame.Rect( j * tile_size[ 0 ], i * tile_size[ 1 ], tile_size[ 0 ], tile_size[ 1 ] ) )
            pygame.display.flip()

    # just wait three seconds if this variable is true
    # else go into a loop
    if not loopTillClosed:
        time.sleep(3)
        pygame.quit()
        return

    # a loop that shows the image till the user closes the showImage window
    # the code from which this method is called is paused for the time
    # this window is active, because of this while loop
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return