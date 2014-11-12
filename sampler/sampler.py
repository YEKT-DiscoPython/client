import json
import pygame
from button import Button
from os import getcwd
from button_style import RED, BLUE, GREEN, BLACK, WHITE, ORANGE, BUTTON_STYLE_1
import time

SAMPLES_PATH = getcwd() + "/"
config_and_status = {"record": False}
db_samples = {}

mode = 0

def load_db(path):
    global db_samples
    db_samples = json.loads(open(path).read())

def load_keys(path):
    global is_playing
    config = json.loads(open(path).read())
    for key, sample in config.items():
        samples[key] = pygame.mixer.Sound(SAMPLES_PATH + db_samples[sample])
    is_playing = {k: False for k in config.keys()}

def quit_it():
    pygame.quit()

def get_time():
    return int(time.time() * 10000)

def start_record():
    global notes
    global start_record_time
    notes = []
    start_record_time = get_time()
    #TODO Start record
    config_and_status['record'] = True
    buttons["record"].function = stop_record
    buttons["record"].text = "Stop Record"
    buttons["record"].render_text()

def stop_record():
    global start_record_time
    global mode
    start_record_time = -1
    temp_notes.clear()
    mode = 1
    #TODO Stop record
    config_and_status['record'] = False
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

clock = pygame.time.Clock()
start_record_time = -1
notes = []
temp_notes = {}

samples =  {}
is_playing = {}
load_db('db_samples.json')
load_keys('test.json')

while True:
    clock.tick(1000)
    if mode == 0:
        event_time = get_time()
        event = pygame.event.poll()
        if event.type != pygame.NOEVENT:
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                key = pygame.key.name(event.key)

            if event.type == pygame.KEYDOWN:
                if (key in samples.keys()) and (not is_playing[key]):
                    if start_record_time != -1:
                        temp_notes[key] = event_time
                    samples[key].play(fade_ms=50)
                    is_playing[key] = True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
            elif event.type == pygame.KEYUP and key in samples.keys():
                if start_record_time != -1:
                    notes.append((event_time - start_record_time, key, event_time - temp_notes[key]))
                samples[key].fadeout(50)
                is_playing[key] = False

            buttons_update(event, buttons)
            pygame.display.update()
    elif mode == 1:
        if start_record_time == -1:
                start_record_time = get_time()

        tick_time = get_time() - start_record_time

        if len(temp_notes) > 0:
            for i in list(temp_notes.keys()):
                if temp_notes[i] <= tick_time:
                    samples[i].fadeout(50)
                    temp_notes.pop(i)

        if len(notes) > 0:
            if notes[0][0] <= tick_time:
                note = notes.pop(0)
                temp_notes[note[1]] = note[0] + note[2] #Set stop time
                samples[note[1]].play(fade_ms=50)

        if len(notes) == 0 and len(temp_notes) == 0:
            mode = 0

pygame.quit()