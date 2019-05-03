
__author="boukbab mhamed"
__vesrion="1.0"
__licence="BSD"
import pygame as pg

blue = (0,0,255)
green = (0,255,0)
pink = (255,200,200)
pleft=0
pright=0
pg.init()
screen = pg.display.set_mode((480,240))
screen.fill(pink)

myfont = pg.font.SysFont("monospace", 80)
font = pg.font.SysFont("monospace", 20)
text=""
# render text


lunched=True
while lunched:
    
    for event in pg.event.get():
        if event.type==pg.QUIT:
            lunched=False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                text="FORWARD"
                pleft=100
                pright=100
                screen.fill(pink)
            elif event.key == pg.K_DOWN:
                text="BACKWARD"
                pleft=-100
                pright=-100
                screen.fill(pink)
            elif event.key == pg.K_RIGHT:
                text="RIGHT"
                pleft=100
                pright=50
                screen.fill(pink)
            elif event.key == pg.K_LEFT:
                text="LEFT"
                pleft=50
                pright=100
                screen.fill(pink)
            elif event.key == pg.K_RSHIFT :
                text="STOP"
                pleft=0
                pright=0
                screen.fill(pink) 
    label = myfont.render(text, 1, blue)
    lblvalue=font.render("Left :: "+str(pleft)+" Right :: "+ str(pright), 2, green)
    screen.blit(lblvalue, (20, 100))
    screen.blit(label, (20, 20))
    pg.display.update()
