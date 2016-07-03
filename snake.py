#!/usr/bin/env python

try:

    import os
    import sys
    import random
    import os
    import getopt
    import pygame
    from socket import *
    from pygame.locals import *

except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)


pygame.init()

screen = pygame.display.set_mode((800, 600))

score = 0

black = (0,0,0)
white = (255,255,255)
blue = (0,0,200)
red = (200,0,0)
yellow = (255,255,0)
green = (0,180,0)

flag = 0

increaser = 0

segmentBlockWidth = 10
segmentBlockHeight = 10
segmentXMargin = 1
segmentYMargin = 1

screen_rect = screen.get_rect()

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(black)

class snakeSegment(pygame.sprite.Sprite):

    def __init__(self,x,y):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([segmentBlockWidth, segmentBlockHeight])
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_new = segmentBlockWidth + segmentXMargin
        self.y_new = 0
        self.rect.clamp_ip(screen_rect)

    def moveUp(self):
        self.x_new = 0
        self.y_new = -(segmentBlockWidth + segmentYMargin)

    def moveDown(self):
        self.x_new = 0
        self.y_new = segmentBlockWidth + segmentYMargin
        

    def moveLeft(self):
        self.x_new = -(segmentBlockWidth + segmentXMargin)
        self.y_new = 0
        
    def moveRight(self):
        self.x_new = segmentBlockWidth + segmentXMargin
        self.y_new = 0
    
class snakeFood(pygame.sprite.Sprite) :

    def __init__(self,x,y,color):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10,10])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    

#screen = pygame.display.set_mode((800, 600))

allSprites = pygame.sprite.Group()
allFood = pygame.sprite.Group()




clock = pygame.time.Clock()

snake = []    

yellow_foods = []
mauve_foods = []


goingX = True
goingY = False


for i in range(15):

    x = 250 - (segmentBlockWidth + segmentXMargin)*i
    y = 30

    segment = snakeSegment(x,y)
    snake.append(segment)
    allSprites.add(segment)


    
for j in range(20):

    x1 = random.uniform(0,800)
    y1 = random.uniform(0,600)
    food = snakeFood(x1,y1,yellow)
    yellow_foods.append(food)
    allFood.add(food)

for k in range(30):

    x2 = random.uniform(0,800)
    y2 = random.uniform(0,600)
    poison = snakeFood(x2,y2,(127,0,255))
    mauve_foods.append(poison)
    allFood.add(poison)
        
    
dx = snake[0].x_new
dy = snake[0].y_new


t = True


while t:

    
    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            t = False
        
        elif event.type == KEYDOWN:

            if event.key == K_LEFT:

                if not goingX:
                    snake[0].moveLeft()
                    dx = snake[0].x_new
                    dy = snake[0].y_new
                    goingX = True
                    goingY = False

                   
            if event.key == K_RIGHT:

                if not goingX:
                    snake[0].moveRight()
                    dx = snake[0].x_new
                    dy = snake[0].y_new
                    goingX = True
                    goingY = False
      
            if event.key == K_UP:

                if not goingY:
                    snake[0].moveUp()
                    dx = snake[0].x_new
                    dy = snake[0].y_new
                    goingX = False
                    goingY = True
                
            if event.key == K_DOWN:

                if not goingY:
                    snake[0].moveDown()
                    dx = snake[0].x_new
                    dy = snake[0].y_new
                    goingX = False
                    goingY = True


            if event.key == K_q:
                t = False     
                                
                                
    old_seg = snake.pop()
    allSprites.remove(old_seg)
                       
    x = snake[0].rect.x + dx
    y = snake[0].rect.y + dy

    new_seg = snakeSegment(x,y)
    allSprites.add(new_seg)
    snake.insert(0,new_seg)

    #screen.blit(s_food.image,(200,200))

    
    
    for x in range(20):

        if pygame.sprite.collide_rect(snake[0], yellow_foods[x]):
            allFood.remove(yellow_foods[x])
        
            increaser += 1
            newer_seg = snakeSegment(snake[14].rect.x + segmentBlockWidth, snake[14].rect.y + segmentBlockHeight)
            allSprites.add(newer_seg)
            snake.append(newer_seg)
            
            score = score + 100



    for y in range(30):

        if pygame.sprite.collide_rect(snake[0], mauve_foods[y]):
            flag = -1

    for z in range(len(snake)-3):
        if snake[0].rect.x == snake[z+3].rect.x and snake[0].rect.y == snake[z+3].rect.y:
            flag = -1
            
    if increaser == 37: #can be removed for AI training
        flag = 1
            
    if snake[0].rect.left == 0 or snake[0].rect.right == 800 or snake[0].rect.top == 0 or snake[0].rect.bottom == 600:
        flag = -1

    if flag == 0:
        screen.fill(black)
        score = score + 0.1
        allSprites.draw(screen)
        allFood.draw(screen)

    if flag == -1:
        fonta = pygame.font.Font(None,48)
        text = fonta.render("GAME OVER",True, red)
        textpos = text.get_rect()
        textpos.centerx = screen.get_rect().centerx
        textpos.centery = screen.get_rect().centery
        screen.blit(text, textpos)
        fontb = pygame.font.Font(None,24)
        scoreText = fontb.render("Score : " + str(score), True, blue)
        screen.blit(scoreText, (textpos.centerx - 40 ,textpos.centery + 50))            
        fontc = pygame.font.Font(None, 28)
        instr = fontc.render(" PRESS Q to QUIT", True, (0,255,0))
        screen.blit(instr, (textpos.centerx - 80 , textpos.centery + 90))
        
    if flag == 1: #Can remove this for AI training
        font = pygame.font.Font(None, 60)
        winningText = font.render("WINNER WINNER CHICKEN DINNER", True, (135,206,235))
        pos = winningText.get_rect()
        pos.centerx = screen.get_rect().centerx
        pos.centery = screen.get_rect().centery
        screen.blit(winningText,pos)
        
    
    pygame.display.flip()

    clock.tick(20)
    
   
pygame.quit()

      


        


        
        


        
