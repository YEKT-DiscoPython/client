import json
import pygame
from button import Button
from os import getcwd

SAMPLES_PATH = getcwd() + "/"

def load_json(path):
    global is_playing
    config = json.loads(open(path).read())
    for key, sample in config.items():
        samples[key] = pygame.mixer.Sound(SAMPLES_PATH + sample)
    is_playing = {k: False for k in config.keys()}

def quit_it():
    pygame.quit()

RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
ORANGE = (255,180,0)
BUTTON_STYLE = {"hover_color" : BLUE,
                "clicked_color" : GREEN,
                "clicked_font_color" : BLACK,
                "hover_font_color" : ORANGE}

pygame.mixer.init(44100,16,2,1024)
screen = pygame.display.set_mode((400,150))
pygame.init()

quit_button = Button((0,0,80,20),RED, quit_it,
                 text="Exit", **BUTTON_STYLE)

samples =  {}
is_playing = {}
load_json('test.json')

global channels
channels = [pygame.mixer.Channel(i) for i in range(8)]

while True:
    event = pygame.event.wait()

    if event.type in (pygame.KEYDOWN, pygame.KEYUP):
        key = pygame.key.name(event.key)

    if event.type == pygame.KEYDOWN:
        if (key in samples.keys()) and (not is_playing[key]):
            samples[key].play(fade_ms=50)
            is_playing[key] = True
        elif event.key == pygame.K_ESCAPE:
            pygame.quit()
            raise KeyboardInterrupt
    elif event.type == pygame.KEYUP and key in samples.keys():
        samples[key].fadeout(50)
        is_playing[key] = False

    quit_button.check_event(event)
    quit_button.update(screen)
    pygame.display.update()

pygame.quit()