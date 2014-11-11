import json
import pygame
from button import Button
from os import getcwd
from button_style import RED, BLUE, GREEN, BLACK, WHITE, ORANGE, BUTTON_STYLE_1

SAMPLES_PATH = getcwd() + "/"

def load_json(path):
    global is_playing
    config = json.loads(open(path).read())
    for key, sample in config.items():
        samples[key] = pygame.mixer.Sound(SAMPLES_PATH + sample)
    is_playing = {k: False for k in config.keys()}

def quit_it():
    pygame.quit()

def start_record():
    #TODO Start record
    buttons["record"].function = stop_record
    buttons["record"].text = "Stop Record"
    buttons["record"].render_text()

def stop_record():
    #TODO Stop record
    buttons["record"].function = start_record
    buttons["record"].text = "Start Record"
    buttons["record"].render_text()

def buttons_update(event, buttons):
    for button in buttons.values():
        button.check_event(event)
        button.update(screen)

pygame.mixer.init(44100,16,2,1024)
screen = pygame.display.set_mode((400,150))
pygame.init()

buttons = {}
buttons["exit"] = Button((0,0,80,20),RED, quit_it,
                 text="Exit", **BUTTON_STYLE_1)
buttons["record"] = Button((0,0,80,20),RED, start_record,
                 text="Start Record", **BUTTON_STYLE_1)
buttons["record"].rect.center = (screen.get_rect().centerx,10)


samples =  {}
is_playing = {}
load_json('test.json')

global channels
channels = [pygame.mixer.Channel(i) for i in range(8)]

while True:
    event = pygame.event.wait()

    if event.type == pygame.QUIT:
        pygame.quit()

    if event.type in (pygame.KEYDOWN, pygame.KEYUP):
        key = pygame.key.name(event.key)

    if event.type == pygame.KEYDOWN:
        if (key in samples.keys()) and (not is_playing[key]):
            samples[key].play(fade_ms=50)
            is_playing[key] = True
        elif event.key == pygame.K_ESCAPE:
            pygame.quit()
    elif event.type == pygame.KEYUP and key in samples.keys():
        samples[key].fadeout(50)
        is_playing[key] = False

    buttons_update(event, buttons)
    pygame.display.update()

pygame.quit()