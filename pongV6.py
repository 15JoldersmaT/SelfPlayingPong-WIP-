import torch
import pygame
import random
import math
import torch

from torch import nn
import numpy as np

pygame.init()
display = pygame.display.set_mode((1300,800))
pygame.display.set_caption('Pong')

clock = pygame.time.Clock()

wall1Y = 300
wall2Y = 350
runners = []
bestDistance = 0
mutateRate = .4
advancesLeft = 1
advancesRight = 1




bestRunner = ''



bestLeft = 10000
bestRight = 10000

worstLeft = 10000

gameTimer = 1800
gameTimerMax = 1800
leftScore = 10000
rightScore = 10000
lastLeftScore = 10000


rotate = 0
last5LeftAvg = 10000
#0-4
lane = 0

field1 = [0,0,0,
          0,0,0,
          0,0,0]

field2 = [0,0,0,
          0,0,0,
          0,0,0]


leftWins = 0
rightWins = 0
games = 0
show = True
#paddle left = 0 paddle right = 1
paddles = []

class Neural_Network(nn.Module):
    def __init__(self, ):
        super(Neural_Network, self).__init__()

        self.inputSize =6 # updated to 4
        self.outputSize = 1
        self.hiddenSize =600
        
        # weights
        self.W1 = torch.randn(self.inputSize, self.hiddenSize).float() # updated to (4, 3) tensor
        self.W2 = torch.randn(self.hiddenSize, self.outputSize).float() # 3 X 1 tensor
        
    def forward(self, X):
        self.z = torch.matmul(X, self.W1) # 3 X 3 ".dot" does not broadcast in PyTorch
        self.z2 = self.sigmoid(self.z) # activation function
        self.z3 = torch.matmul(self.z2, self.W2.float())
        o = self.sigmoid(self.z3) # final activation function
        return o
        
    def sigmoid(self, s):
        return 1 / (1 + torch.exp(-s))

bestLeftNet = Neural_Network()
bestRightNet = Neural_Network()

bestNet  = Neural_Network()




def normalize(x):

    x = (x -1)/(10-1)
    return x


class Ball:
    def __init__(self, x, y, direction,fast):
        self.x = x
        self.y = y
        self.direction = direction
        self.fast = fast
        self.fast = False

    def main(self,display):
        global show
        if  show == True:
             pygame.draw.rect(display, (255, 165, 0), (self.x,self.y,10,10))
         
    def move(self):
        global gameTimer
        global leftScore
        global rightScore
        global lastLeftScore
        global bestLeft
        global bestRight
        global bestRightNet
        global bestLeftNet
        global games
        global gameTimerMax
        global worstLeft
        global advancesLeft
        global advancesRight
        global rotate
        global last5LeftAvg
        gameTimer = gameTimer -1
        if gameTimer <= 0:
            #New game
            games = games+ 1
            worstLeft = worstLeft - 5
            bestLeft = bestLeft + 5


             #if leftScore < lastLeftScore:
            #    advancesRight = advancesRight - 1
            #    advancesLeft = advancesLeft + 1

            #if leftScore > lastLeftScore:
            #    advancesLeft = advancesLeft - 1
            #    advancesRight = advancesRight + 1

                
                
            if worstLeft < 10000:
                worstLeft = 10000

            
            if leftScore > worstLeft:
                print ('New High Score for Right! ' + str(bestRight)+ ' It took ' + str(games) + ' games')
                worstLeft = leftScore
                bestRightNet = paddles[1].net

                
            elif leftScore < bestLeft:
                bestLeft = leftScore
                bestLeftNet = paddles[0].net


            if advancesLeft < 1:
                advancesLeft = 1

            if advancesRight < 1:
                advancesRight = 1


            if advancesRight > 10:
                advancesRight = 10

            if advancesLeft > 10:
                advancesLeft = 10
                
            paddles[0].net.W1 = bestLeftNet.W1 + torch.randn_like( bestLeftNet.W1) * (mutateRate/advancesLeft)
            paddles[0].net.W2 = bestLeftNet.W2 + torch.randn_like( bestLeftNet.W2) * (mutateRate/advancesLeft)
           
            paddles[1].net.W1 = bestRightNet.W1 + torch.randn_like(bestRightNet.W1) * (mutateRate/advancesRight)
            paddles[1].net.W2 = bestRightNet.W2 + torch.randn_like(bestRightNet.W2) * (mutateRate/advancesRight)
            mainBall.x = 350
            mainBall.y = 400
            mainBall.y = mainBall.y
            paddles[0].y = 400
            paddles[1].y = 400
            mainBall.direction = 'rightStraight'
     
            gameTimer = gameTimerMax
            lastLeftScore = leftScore
            leftScore = 10000
            rightScore = 10000
            advancesLeft = 1
            advancesRight = 1
            

        sped = 1
        if self.fast == True:
            sped = 2
        else:
            sped = 1
        
        if self.direction == 'leftStraight':
            self.x = self.x - sped
        elif self.direction == 'leftUp':
            self.x = self.x - sped
            self.y = self.y - sped

        elif self.direction == 'leftDown':
            self.x = self.x - sped
            self.y = self.y + sped

        elif self.direction == 'rightUp':
            self.x = self.x + sped
            self.y = self.y - sped
        elif self.direction == 'rightDown':
            self.x = self.x + sped
            self.y = self.y + sped
        else:
            self.x = self.x + sped


        if self.y < 200:
            if self.direction == 'rightUp':
                self.direction = 'rightDown'
            if self.direction == 'leftUp':
                self.direction = 'leftDown'
        if self.y > 600:
            if self.direction == 'rightDown':
                self.direction = 'rightUp'
            if self.direction == 'leftDown':
                self.direction = 'leftUp'
                
        if self.x < 100:
            
                #right score
            leftScore = leftScore +100
            
            
            self.fast = False
            self.x = 350
            self.y = 400 
            paddles[0].y = 400
            paddles[1].y = 400
            mainBall.direction = 'rightStraight'
           

        if self.x > 600:
                #left score
            
            #rightScore = rightScore+100
            leftScore = leftScore - 100

            self.fast = False
            self.x = 350
            self.y = 400
            paddles[0].y = 400
            paddles[1].y = 400
            mainBall.direction = 'leftStraight'
           
 
        
        
mainBall = Ball(350,400,'leftStraight',False)

class paddle:
    def __init__(self,x, y, net,side):
        self.x = x
        self.y = y
        self.net = net
        self.side = side
        if self.side == 'left':
            self.x = 100
        else:
            self.x = 590
                
        
        

    def main(self,display):
        global show
        if  show == True:
            pygame.draw.rect(display, (255,0,0), (self.x,self.y,20,60))

            pygame.draw.rect(display, (255,255,255), (self.x,self.y,20,30))
         
    def move(self):
        global mainBall
        global leftScore
        global rightScore
        global gameTimer
        global gameTimerMax
        global advancesLeft
        global advancesRight

        gameTimerA = (gameTimer-gameTimerMax)/gameTimerMax
        
        bX = mainBall.x
        bY = mainBall.y

        yX = mainBall.x - self.x
        yY = self.y

        oY2 = 0
        oY = 0
        oX = 0
        for paddle in paddles:
            if paddle.side != self.side:
                oY = (paddle.y-self.y)/100
                oY2 = (paddle.y)/100
                oX = (paddle.x)/100





        Jx =( bX  -oX)/100
    
        Jy = (bY - oY2)/100
        
        
        #How #Potential weak point
        dirIn = 0.0
        if mainBall.direction == 'leftStraight':
            dirIn = -.25

        elif mainBall.direction == 'leftDown':
            dirIn = -1.0

        elif mainBall.direction == 'leftUp':
            dirIn = -1.75
        elif mainBall.direction == 'rightStraight':
            dirIn = 1.0
        elif mainBall.direction == 'rightDown':
            dirIn = .25
        elif mainBall.direction == 'rightUp':
            dirIn = 1.75
        

        x2 = (self.x - mainBall.x)/100
        y2 =( self.y - mainBall.y)/100

        leftScoreA = (leftScore - 10000) / 10000
        rightScoreA = (rightScore - 10000) / 10000
        spedd = 0
        if mainBall.fast == True:
            spedd = 1
        
        output = self.net.forward(torch.tensor([    
                                                   
                                                    [spedd],
                                                    [x2],
                                                    [y2],
                                                    [oY],
                                                    [dirIn],
                                                    [Jy]

                                                    ]).T)

        max_index = torch.argmax(output, dim=1)
        if output[0][0] >= .5 :
            self.direct = 'Down'
            if output[0][0] > .8:
                self.direct = 'DownFast'
 
        else :
            self.direct = 'Up'
            if output[0][0] < .2:
                self.direct = 'UpFast'
                
        if self.direct == 'DownFast':
            self.y +=  2
            if self.y >600:
                self.y = 600

        if self.direct == 'UpFast':
            self.y -= 2
            if self.y < 200:
                self.y = 200

        if self.direct == 'Down':
            self.y +=  1
            if self.y >600:
                self.y = 600
        if self.direct == 'Up':
            self.y -= 1
            if self.y < 200:
                self.y = 200
        global mutateRate
        
        if self.side == 'right':
            
            #Ball coming from left
            #size of paddle is 30
            if mainBall.x < 130 and mainBall.x > 100 and mainBall.y+10  > self.y and mainBall.y+10 < self.y + 60:
                if mainBall.y < self.y + 30:
                    mainBall.fast = True
                else:
                    mainBall.fast = False
                if mainBall.direction == 'leftUp' or mainBall.direction == 'leftStraight' or mainBall.direction == 'leftDown':
                    dirChance = random.randint(0,3)
                    mainBall.x = mainBall.x 
                    mainBall.y =  mainBall.y 
                    print('Left hit at ' + str(games) + ' games')
                    if dirChance == 1:
                        mainBall.direction = 'rightUp'
                    elif dirChance == 2:
                        mainBall.direction = 'rightDown'
                    else:
                        mainBall.direction = 'rightStraight'

                leftScore = leftScore - 50
                advancesRight = advancesRight + 1
                if advancesRight < 1:
                    advancesRight = 1

        else:
            #Ball coming from right
            if mainBall.x > 570 and mainBall.x < 600 and mainBall.y+10 > self.y and mainBall.y +10< self.y + 60:
                if mainBall.y < self.y + 30:
                    mainBall.fast = True
                else:
                    mainBall.fast = False
                if mainBall.direction == 'rightUp' or mainBall.direction == 'rightStraight' or mainBall.direction == 'rightDown':
                    dirChance = random.randint(0,3)
                    mainBall.x = mainBall.x
                    mainBall.y = mainBall.y
                    print('Right hit at ' + str(games) + ' games')
                    if dirChance == 1:
                        mainBall.direction = 'leftUp'
                    elif dirChance == 2:
                        mainBall.direction = 'leftDown'
                    else:
                        mainBall.direction = 'leftStraight'
                leftScore = leftScore + 50
                advancesLeft = advancesLeft + 1
                if advancesLeft < 1:
                    advancesLeft = 1
                        
                    
                    

            



            
        

net1 = Neural_Network()

p1 = paddle(100,400,net1, 'left')
p1.x = 100
p1.y = 400
p1.side = 'left'
p1.net = net1
paddles.append(p1)
paddles.append(p1)
paddles[0] = p1


net2 = Neural_Network()

p2 = paddle(590,400,net1,'right')
p2.x = 590
p2.y = 400
p2.side = 'right'
p2.net = net2
paddles[1] = p2

speedy = 100

while True:
    
    mx, my = pygame.mouse.get_pos()

    display.fill((0,0,0))

    for paddle in paddles:
        paddle.move()
        paddle.main(display)

    mainBall.move()
    mainBall.main(display)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        if event.type == pygame.KEYUP:
            if event.key==pygame.K_q:
               speedy = 90000
            if event.key==pygame.K_w:
                speedy = 60
            if event.key==pygame.K_s:
                if show == True:
                    show = False
                else:
                    show = True

        if speedy < 30:
            speedy = 30

    keys = pygame.key.get_pressed();
    
    #for tile in tiles:
    #    tile.main(display)

    
    clock.tick(speedy)

    pygame.display.update()
