import pygame
from settings import game_var
from character import Character
from weapon import Weapon
from items import Item

pygame.init()

screen = pygame.display.set_mode((game_var.SCREEN_WIDTH, game_var.SCREEN_HEIGHT))
pygame.display.set_caption(game_var.CAPTION)

#player scale helper 
def scale_img(image, scale=game_var.PLAYER_SCALE):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

#load heart images
heart_empty = scale_img(pygame.image.load(f"./assets/images/items/heart_empty.png").convert_alpha(), game_var.ITEM_SCALE)
heart_half = scale_img(pygame.image.load(f"./assets/images/items/heart_half.png").convert_alpha(), game_var.ITEM_SCALE)
heart_full = scale_img(pygame.image.load(f"./assets/images/items/heart_full.png").convert_alpha(), game_var.ITEM_SCALE)


# load item images
coin_images = []
for x in range(4):
    img = scale_img(pygame.image.load(f"./assets/images/items/coin_f{x}.png").convert_alpha(), game_var.ITEM_SCALE)
    coin_images.append(img)

# load potion image
red_potion = scale_img(pygame.image.load(f"./assets/images/items/potion_red.png").convert_alpha(), game_var.POTION_SCALE)

# define font 
# font need to be fixed
# font = pygame.font.Font("./assets/fonts/AtariClassic.ttf", 20)
font = pygame.font.Font(None, 20)

# load char
mob_animations = []
mob_types = ["elf", "imp", "skeleton", "goblin", "muddy", "tiny_zombie", "big_demon"]
# load player image types
animation_types = ['idle', 'run']
# load images
for mob in mob_types:
    animation_list = []
    for animation in animation_types:
        # for types
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f"./assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
            img = scale_img(img)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)


# function for outputting text onto thhe screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# function for display game info 
def draw_info():
    pygame.draw.rect(screen, game_var.PANEL_COLOR, (0, 0, game_var.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, game_var.COLOR_WHITE, (0, 50), (game_var.SCREEN_WIDTH, 50))
    # draw lives
    half_heart_drawn = False
    for i in range(5):
        if player.health >= ((i + 1) * 20):
            screen.blit(heart_full, (10 + i * 50, 0))
        elif (player.health % 20 > 0) and half_heart_drawn == False:
            screen.blit(heart_half, (10 + i * 50, 0))
            half_heart_drawn = True
        else:
            screen.blit(heart_empty, (10 + i * 50, 0))

    draw_text(f"X:{player.score}", font, game_var.COLOR_WHITE, game_var.SCREEN_WIDTH - 100, 15)
    



# Damage text class
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()

# create player
player = Character(100, 100, 70, mob_animations, 0)

# create enemy 
enemy = Character(200, 300,100, mob_animations, 1)

enemy_list = []
enemy_list.append(enemy)

# arrow
arrow_image = scale_img(pygame.image.load(f"./assets/images/weapons/arrow.png").convert_alpha(), game_var.BOW_SCALE)

# bow 
bow_image = scale_img(pygame.image.load(f"./assets/images/weapons/bow.png").convert_alpha(), game_var.BOW_SCALE)
bow = Weapon(bow_image, arrow_image)


# create sporite group
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()


potion = Item(200, 200, 1, [red_potion])
item_group.add(potion)
coin = Item(400, 400, 0, coin_images)
item_group.add(coin)


# temporary damage text 
# damage_text = DamageText(300, 400, "Hello 15", game_var.COLOR_RED)
# damage_text_group.add(damage_text)

# clock for FPS
clock = pygame.time.Clock()

# player movement
moving_left = False
moving_right = False
moving_up = False
moving_down = False

run = True 
while run:

    clock.tick(game_var.FPS)

    screen.fill(game_var.COLOR_BG)

    # calculate player movement 
    dx = 0
    dy = 0

    if moving_left == True:
        dx = -game_var.SPEED
    if moving_right == True:
        dx = game_var.SPEED
    if moving_up == True:
        dy = -game_var.SPEED
    if moving_down == True:
        dy = game_var.SPEED
    
    player.move(dx, dy)

    player.update()

    player.draw(surface=screen)
    bow.draw(surface=screen)


    # enemy update code 
    for enemy in enemy_list:
        enemy.update()
    
    for enemy in enemy_list:
        enemy.draw(screen)


    # arrow
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)

    for arrow in arrow_group:
        damage, damage_pos = arrow.update(enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), game_var.COLOR_RED)
            damage_text_group.add(damage_text)
    damage_text_group.update()
    item_group.update(player)

    for arrow in arrow_group:
        arrow.draw(screen)
    damage_text_group.draw(screen)
    item_group.draw(screen)
    draw_info()

    
    

    for event in pygame.event.get():
        # quit event
        if event.type == pygame.QUIT:
            run = False

        # take keypress 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False
    
    pygame.display.update()

pygame.quit()