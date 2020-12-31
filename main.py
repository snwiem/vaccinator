import os, sys
import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')

for font in pygame.font.get_fonts():
    print(font)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound:', fullname)
        raise SystemExit(message)
    return sound


class Ghost(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = ghost_img
        self.rect = ghost_rect
        self.alpha = 255
        self.fade = False

    def update(self):
        if self.fade:
            self.alpha = max(0, self.alpha-5)
            self.image = ghost_img.copy()
            self.image.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)


WIDTH = 1024
HEIGHT = 561
MOUSE_VISIBLE = False
MAX_BULLETS = 5

font1 = pygame.font.SysFont('Comic Sans MS', 45)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyHunt")
pygame.mouse.set_visible(MOUSE_VISIBLE)

background_img, background_rect = load_image('forest_01_1024.jpg')

clock = pygame.time.Clock()
loop = True

gunshot_snd = load_sound('gun-gunshot-01.wav')
reload_snd = load_sound('gun-cocking-01.wav')
crosshair_img, crosshair_rect = load_image('crosshair_100.png', -1)
ghost_img, ghost_rect = load_image('ghost_01.png')
bullet_img, bullet_rect = load_image('bullet_02.png')
bullet_img = pygame.transform.scale(bullet_img, (20, 60))
bullet_rect = bullet_img.get_rect()
screen.blit(background_img, background_rect)

num_bullets = MAX_BULLETS
is_reloading = False
reload_time = 320
RELOAD_EVENT = USEREVENT+1

num_shots = 0
num_hits = 0


def render_bullets():
    for bullet in range(0, num_bullets):
        screen.blit(bullet_img, (850 + (bullet * 30), HEIGHT - bullet_rect.height - 20))


def render_texts():
    text = f'{num_hits}'
    shots_img = font1.render(text, True, (255, 255, 255), (0, 0, 0))
    shots_rect = shots_img.get_rect()
    shots_rect_dest = pygame.rect.Rect(17, HEIGHT - shots_rect.height - 23, shots_rect.width+6, shots_rect.height+6)
    screen.blit(background_img, shots_rect_dest, shots_rect_dest)
    screen.blit(shots_img, shots_rect_dest)


render_bullets()
render_texts()

while loop:
    for event in pygame.event.get():
        if event.type == QUIT:
            loop = False
            break
        if event.type == RELOAD_EVENT:
            if num_bullets == MAX_BULLETS:
                pygame.time.set_timer(RELOAD_EVENT, 0)
                is_reloading = False
            else:
                reload_snd.play()
                num_bullets += 1
        if event.type == MOUSEBUTTONDOWN and not is_reloading:
            left, middle, right = pygame.mouse.get_pressed()
            if left:
                if num_bullets > 0:
                    gunshot_snd.play()
                    for b in range(num_bullets-1, MAX_BULLETS):
                        r = pygame.rect.Rect(850+b*30, HEIGHT-bullet_rect.height-20, bullet_rect.width, bullet_rect.height)
                        screen.blit(background_img, r, r)
                    num_bullets -= 1
                    num_shots += 1
            elif right:
                #reload_snd.play()
                #num_bullets = MAX_BULLETS
                is_reloading = True
                pygame.time.set_timer(RELOAD_EVENT, reload_time)
    # copy background at last cursor position
    screen.blit(background_img, crosshair_rect, crosshair_rect)
    crosshair_rect.center = pygame.mouse.get_pos()
    # overwrite new cursor position
    screen.blit(crosshair_img, crosshair_rect)

    render_bullets()
    render_texts()

    # update screen
    pygame.display.flip()
    clock.tick(60)

print("All done...bye")

