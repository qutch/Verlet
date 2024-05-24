import pygame
import numpy as np
import math
import random as r
import time

pygame.init()

screen_height = 750
screen_width = 750

screen = pygame.display.set_mode((screen_height, screen_width))

clock = pygame.time.Clock()

class Ball:
    def __init__(self, pos, vel, acc, radius, mass):
        self.pos = np.asarray(pos, dtype=np.float64)
        self.vel = np.asarray(vel, dtype=np.float64)
        self.acc = np.asarray(acc, dtype=np.float64)
        self.radius = radius
        self.mass = mass
    
    def update(self, dt, gravity_x, gravity_y):
        self.calcFloorCollision()
        new_pos = self.pos + (self.vel * dt) + (0.5 * self.acc * dt * dt)
        new_acc = self.calcAcceleration(gravity_x, gravity_y)
        new_vel = self.vel + (0.5 * (self.acc + new_acc) * dt)
        self.pos = new_pos
        self.acc = new_acc
        self.vel = new_vel
    
    def calcFloorCollision(self):
        if self.isTouchingFloor(): # Floor Collision
            self.pos[1] = screen_height - self.radius + 1
            self.vel[1] = -self.vel[1] * 0.8
        if self.isTouchingCeiling(): # Ceiling Collison
            self.pos[1] = self.radius + 1
            self.vel[1] = -self.vel[1] * 0.8
        if self.isTouchingRightWall(): # Right Wall Collision
            self.pos[0] = screen_width - self.radius
            self.vel[0] = -self.vel[0] * 0.8
        if self.isTouchingLeftWall(): # Left Wall Collison
            self.pos[0] = self.radius
            self.vel[0] = -self.vel[0] * 0.8
    
    def isTouchingFloor(self):
        if self.pos[1] + self.radius > screen_height:
            return True
    def isTouchingCeiling(self):
        if self.pos[1] - self.radius < 0:
            return True
    def isTouchingRightWall(self):
        if self.pos[0] + self.radius > screen_width:
            return True
    def isTouchingLeftWall(self):
        if self.pos[0] - self.radius < 0:
            return True
            
    
    def calcAcceleration(self, gravity_x, gravity_y):
        return np.asarray([gravity_x, gravity_y])
    
    def draw(self):
        pygame.draw.circle(screen, "black", self.pos, self.radius)
        
    
    def calcBallCollision(self, balls):
        for other in balls:
            if self is other:
                return
            distance = np.linalg.norm(self.pos - other.pos)
            if distance < self.radius + other.radius:
                
                differenceVector = other.pos - self.pos
                
                magnitude = np.linalg.norm(differenceVector)
                normalVector = differenceVector / magnitude


                overlap = float(self.radius + other.radius - distance)

                if overlap > 0:
                    
                    displacement = normalVector * (overlap/2)

                    self.pos -= displacement
                    other.pos += displacement
                
                normCompSelf = np.dot(self.vel, normalVector) * normalVector
                normCompOther = np.dot(other.vel, normalVector) * normalVector
                
                tangCompSelf = self.vel - normCompSelf
                tangCompOther = other.vel - normCompOther
                
                newNormSelf = (self.mass * normCompSelf + other.mass * normCompOther + other.mass * (normCompOther - normCompSelf))/(self.mass + other.mass)
                newNormOther = (self.mass * normCompSelf + other.mass * normCompOther + self.mass * (normCompSelf - normCompOther))/(self.mass + other.mass)
                
                self.vel = (newNormSelf + tangCompSelf)
                other.vel = (newNormOther + tangCompOther)




                
                # self.vel = 0.8 * self.vel + 10
                # other.vel = -self.vel * 0.8

        
balls = []

gravity_x = 0
gravity_y = 9.8
counter = 1
        
running = True

while running:
    # Gets the mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            ball = Ball((mouse_x, mouse_y), [50,0], [0,0], 10, 5)
            balls.append(ball)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                balls.clear()
            if event.key == pygame.K_g:
                if counter == 1:
                    gravity_y = 9.8
                    gravity_x = 0
                    counter += 1
                elif counter == 2:
                    gravity_y = -9.8
                    gravity_x = 0
                    counter += 1
                elif counter == 3:
                    gravity_y = 0
                    gravity_x = 9.8
                    counter += 1
                elif counter == 4:
                    gravity_y = 0
                    gravity_x = -9.8
                    counter = 1
            
    # Setting a background color
    screen.fill("white")
    
    # pygame.draw.circle(screen, "blue", (screen_height/2, screen_width/2), 360, 4)
    
    for ball in balls:
        ball.calcBallCollision(balls)
        ball.update(0.166, gravity_x, gravity_y)
        ball.draw()
    
    pygame.display.set_caption("Balls: " + str(len(balls)) + " | FPS: " + str(math.ceil(clock.get_fps())))
    
    # Updating the pygame display and setting clock tick to 60
    pygame.display.update()
    clock.tick(60)