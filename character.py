import pygame
import math
from settings import game_var

class Character:
    def __init__(self, x, y, health, mob_animations, char_type) -> None:
        self.char_type = char_type
        self.score = 0
        self.animation_list = mob_animations[self.char_type]
        self.frame_index = 0 
        self.action = 0 # idle: 0; run:0;
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.health = health
        self.alive = True
        self.image = self.animation_list[self.action][self.frame_index]
        self.flip = False
        self.rect = pygame.Rect(0, 0, 40, 40)
        self.rect.center = (x,y)
        

    def move(self, dx, dy):
        self.running = False
        if dx != 0 or dy != 0:
            self.running = True
        #control flip
        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False

        #control diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/2)
            dy = dy * (math.sqrt(2)/2)

        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        # char alive check 
        if self.health <= 0:
            self.health = 0
            self.alive = False

        # check what player action performing
        if self.running == True:
            self.update_action(1) # 1:run
        else:
            self.update_action(0) # 0:idle

        animation_cooldown = 70
        # handle animation 
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time pass since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            # reset time
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0 
    
    def update_action(self, new_action):
        # check new and previous action
        if new_action != self.action:
            self.action = new_action
            # reset
            self.frame_index = 0
            self.update_time =  pygame.time.get_ticks()

    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        if self.char_type == 0:
            surface.blit(flipped_image, (self.rect.x, self.rect.y - game_var.PLAYER_OFFSET * game_var.PLAYER_SCALE))
        else:
            surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface, game_var.COLOR_RED, self.rect, 1)
