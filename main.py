import os, sys
import pygame
from pygame.locals import *

pygame.init()
if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()
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


screen = pygame.display.set_mode((600, 480))
pygame.display.set_caption("PyHunt")
pygame.mouse.set_visible(True)

clock = pygame.time.Clock()
loop = True
while loop:
    for event in pygame.event.get():
        print("Event: ", event)
        if event.type == QUIT:
            loop = False
    clock.tick(60)

print("All done...bye")

