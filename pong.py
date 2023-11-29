import torch
import pygame
import random
import math
import torch

from torch import nn
import numpy as np

pygame.init()
display = pygame.display.set_mode((700,700))
pygame.display.set_caption('Pong')

clock = pygame.time.Clock()

wall1Y = 300
wall2Y = 350
runners = []
bestDistance = 0
mutateRate = .45

#next line of obstacles
strip = []

bestRunner = ''

obstacles = []

bestLeft = 100000
bestRight = 10000

gameTimer = 1200
gameTimerMax = 1200
leftScore = 10000
rightScore = 10000
#0-4
lane = 0

field1 = [0,0,0,
          0,0,0,
          0,0,0]

field2 = [0,0,0,
          0,0,0,
          0,0,0]

bgColor = (0,random.randint(50, 100),0)
epoch = 0
leftWins = 0
rightWins = 0
games = 0
show = True
#paddle left = 0 paddle right = 1
paddles = []

class Neural_Network(nn.Module):
    def __init__(self, ):
        super(Neural_Network, self).__init__()

        self.inputSize =5 # updated to 4
        self.outputSize = 1
        self.hiddenSize = 55
        
        # weights
        self.W1 = torch.randn(self.inputSize, self.hiddenSize).float() # updated to (4, 3) tensor
        self.W2 = torch.randn(self.hiddenSize, self.outputSize).float() # 3 X 1 tensor
        
    def forward(self, X):
        self.z = torch.matmul(X, self.W1) # 3 X 3 ".dot" does not broadcast in PyTorch
        self.z2 = self.leaky_relu(self.z) # activation function
        self.z3 = torch.matmul(self.z2, self.W2.float())
        o = self.leaky_relu(self.z3) # final activation function
        #print (o)
        return o
        
    def sigmoid(self, s):
        return 1 / (1 + torch.exp(-s))

    def leaky_relu(self, x, alpha=0.01):
        return np.maximum(alpha * x, x)

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
        global bestLeft
        global bestRight
        global bestRightNet
        global bestLeftNet
        global games
        global gameTimerMax
        global bgColor
        global epoch
        gameTimer = gameTimer -1
        if gameTimer <= 0:
            #New game
            games = games+ 1
            
            if leftScore < bestLeft:
                #print ('New High Score for Left!' + str(bestLeft)+ ' It took ' + str(games) + ' games')
                bestLeftNet = paddles[0].net
            if rightScore < bestRight:
                bestRightNet = paddles[1].net
                
            if leftScore < rightScore:
                bgColor = (0,random.randint(50, 100),0)
                epoch += 1
                
                mainBall.x = 350
                mainBall.y = 400
                mainBall.y = mainBall.y
                paddles[0].y = 400
                paddles[1].y = 400
                mainBall.direction = 'leftStraight'

                    
                
                paddles[1].net.W1 = paddles[1].net.W1 + torch.randn_like(paddles[1].net.W1) * mutateRate
                paddles[1].net.W2 = paddles[1].net.W2 + torch.randn_like(paddles[1].net.W2) * mutateRate


                


                      
            elif rightScore < leftScore:
                bgColor = (0,random.randint(50, 100),0)
                epoch += 1

                mainBall.x = 350
                mainBall.y = 400
                paddles[0].y = 400
                paddles[1].y = 400
                mainBall.direction = 'rightStraight'
                #update the paddle that failed


                paddles[0].net.W1 = paddles[0].net.W1 + torch.randn_like( paddles[0].net.W1) * mutateRate
                paddles[0].net.W2 = paddles[0].net.W2 + torch.randn_like( paddles[0].net.W2) * mutateRate

             
                

                

            else:
                bgColor = (0,random.randint(50, 100),0)
                epoch += 1

                mainBall.x = 350
                mainBall.y = 400
                paddles[0].y = 400
                paddles[1].y = 400

                chan = random.randint(1,2)
                if chan == 1:
                    mainBall.direction = 'rightStraight'
                else:
                    mainBall.direction = 'leftStraight'

                chan2 = random.randint(1,2)

                if chan2 == 1:
                    paddles[1].net.W1 = paddles[1].net.W1 + torch.randn_like(paddles[1].net.W1) * mutateRate
                    paddles[1].net.W2 = paddles[1].net.W2 + torch.randn_like(paddles[1].net.W2) * mutateRate

                else:
                    paddles[0].net.W1 = paddles[0].net.W1 + torch.randn_like( paddles[0].net.W1) * mutateRate
                    paddles[0].net.W2 = paddles[0].net.W2 + torch.randn_like( paddles[0].net.W2) * mutateRate

                

                
            gameTimer = gameTimerMax
            leftScore = 10000
            rightScore = 10000
            

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
                
        if self.x < 70:
            
                #right score
            leftScore = leftScore + 300
            

            self.x = 350
            self.y = 400 
            paddles[0].y = 400
            paddles[1].y = 400
            mainBall.direction = 'rightStraight'
           

        if self.x > 630:
                #left score
            
            rightScore = rightScore + 300

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
                oY = (paddle.y-self.y)
                oY2 = (paddle.y)
                oX = (paddle.x)





        Jx =( bX  -oX)
    
        Jy = (bY - oY2)
        
        
        #How #Potential weak point
        dirIn = 0.0
        if mainBall.direction == 'leftStraight':
            dirIn = -.25

        elif mainBall.direction == 'leftDown':
            dirIn = -1.0

        elif mainBall.direction == 'leftUp':
            dirIn = -1.75
        elif mainBall.direction == 'rightstraight':
            dirIn = 1.0
        elif mainBall.direction == 'rightDown':
            dirIn = .25
        elif mainBall.direction == 'rightUp':
            dirIn = 1.75
        

        x2 = (self.x - mainBall.x)
        y2 =( self.y - mainBall.y)

        leftScoreA = (leftScore - 10000) / 10000
        rightScoreA = (rightScore - 10000) / 10000
        spedd = 0
        if mainBall.fast == True:
            spedd = 1
        
        output = self.net.forward(torch.tensor([    
                                                    [dirIn],
                                                    [spedd],
                                                    [oY],
                                                    [x2],
                                                    [y2]
        
                              
                  
                                                    ]).T)

        max_index = torch.argmax(output, dim=1)
        if output[0][0] >= .5 :
            self.direct = 'Down'
 
        else :
            self.direct = 'Up'
            

        if self.direct == 'Down':
            self.y +=  1
            if self.y >600:
                self.y = 600
        if self.direct == 'Up':
            self.y -= 1
            if self.y < 200:
                self.y = 200
        global mutateRate
        
        if self.side == 'left':
            
            #Ball coming from left
            #size of paddle is 30
            if mainBall.x < 130 and mainBall.x > 70 and mainBall.y+10  > self.y and mainBall.y+10 < self.y + 60:
                print ('left1')
                mainBall.x = 131
                if mainBall.y < self.y + 30:
                    mainBall.fast = True
                else:
                    mainBall.fast = False
                if mainBall.direction == 'leftUp' or mainBall.direction == 'leftStraight' or mainBall.direction == 'leftDown':
                    print ('left2')

                    dirChance = random.randint(0,3)
                    mainBall.x = mainBall.x 
                    mainBall.y = mainBall.y 
                    print('Left hit at ' + str(games) + ' games')
                    if dirChance == 1:
                        mainBall.direction = 'rightUp'
                    elif dirChance == 2:
                        mainBall.direction = 'rightStraight'
                    else:
                        mainBall.direction = 'rightDown'

        else:
            #Ball coming from right
            if mainBall.x > 570 and mainBall.x < 630 and mainBall.y+10 > self.y and mainBall.y +10< self.y + 60:
                mainBall.x = 569
                print('right1')
                if mainBall.y < self.y + 30:
                    mainBall.fast = True
                else:
                    mainBall.fast = False
                if mainBall.direction == 'rightUp' or mainBall.direction == 'rightStraight' or mainBall.direction == 'rightDown':
                    dirChance = random.randint(0,3)
                    mainBall.x = mainBall.x 
                    mainBall.y = mainBall.y
                    print ('right2')
                    print('Right hit at ' + str(games) + ' games')
                    if dirChance == 1:
                        mainBall.direction = 'leftUp'
                    elif dirChance == 2:
                        mainBall.direction = 'leftStraight'
                    else:
                        mainBall.direction = 'leftDown'
                        
                    

            



            
        

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

myFont = pygame.font.SysFont("Times New Roman", 18)


while True:
    
    mx, my = pygame.mouse.get_pos()
    display.fill(bgColor)

    # Render the time and display it
    time_surface = myFont.render(f"Time: {epoch}", True, (255,255,255))
    display.blit(time_surface, (10, 10))  # Position it at the bottom of the screen
    

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
