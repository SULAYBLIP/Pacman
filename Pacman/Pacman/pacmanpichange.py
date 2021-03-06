from pygame import*
pacpic = image.load('mazeorange.png')
screen= display.set_mode((700,700))
x,y = 0,0
print(pacpic.get_width(),pacpic.get_height())
running = True
while running:
    for evnt in event.get():
        if evnt.type == QUIT:
            running = False
    for x in range (pacpic.get_width()):
        for y in range (pacpic.get_height()):
            if pacpic.get_at((x,y)) == (0,0,0):
                draw.line(screen,(255,255,255),(x,y),(x,y),2)
            else:
                draw.line(screen,(0),(x,y),(x,y),1)
    save = screen.subsurface(Rect(0,0,pacpic.get_width(),pacpic.get_height()))
    image.save(save,"I'm_an_artist.png")
    display.flip()

#Lime Green
#Orange
#Navy
#Teal
#magenta (255,0,255)



quit()    
