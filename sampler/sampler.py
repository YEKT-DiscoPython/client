import json
import pygame
from button import Button
from os import getcwd
from button_style import RED, BLUE, GREEN, BLACK, WHITE, ORANGE, BUTTON_STYLE_1
import time
from tkinter import Tk, Entry, Text, Button as Tk_button, Scrollbar, END
from copy import deepcopy
import urllib.request
import urllib.parse
import urllib.error
import requests
import http.cookiejar

SAMPLES_PATH = getcwd() + "/"
config_and_status = {"record": False, "key_to_sample": {}}
db_samples = {}
session = {"auth": 0, "user":"", "session":""}

mode = 0

def load_db(path):
    global db_samples
    db_samples = json.loads(open(path).read())


def load_keys(keys):
    global is_playing
    config = json.loads(keys)
    for key, sample in config.items():
        samples[key] = pygame.mixer.Sound(SAMPLES_PATH + db_samples[sample])
        samples[sample] = pygame.mixer.Sound(SAMPLES_PATH + db_samples[sample])
        config_and_status["key_to_sample"][key] = sample
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
    start_record_time = -1
    temp_notes.clear()
    #TODO Stop record
    config_and_status['record'] = False
    buttons["record"].function = start_record
    buttons["record"].text = "Start Record"
    buttons["record"].render_text()

def play_record():
    global play_notes
    global mode
    global temp_notes
    global start_record_time
    start_record_time = -1
    play_notes = deepcopy(notes)
    temp_notes.clear()
    mode = 1

def buttons_update(event, buttons):
    for button in buttons.values():
        button.check_event(event)
        button.update(screen)

def change_keys():
    new_keys = config_and_status["keys"]
    valid = 0
    while(not valid):
        new_keys = editor(new_keys)
        try:
            load_keys(new_keys)
            valid = 1
        except Exception:
            pass

def change_menu(active_buttons):
    screen_rect = screen.get_rect()
    screen_rect.bottom = 30
    screen.fill(BLACK, screen_rect)
    for i in buttons.keys():
        if i in active_buttons:
            buttons[i].show()
        else:
            buttons[i].hide()

def menu1():
    global mode
    buttons_on_this = ("record", "keys", "upload")
    change_menu(buttons_on_this)
    mode = 0

def menu2():
    global mode
    buttons_on_this = ("edit", "play", "upload", "download")
    change_menu(buttons_on_this)
    mode = 2

def create_menu():
    global menu_buttons
    menu_items = (("Create", menu1), ("Edit", menu2), ("Exit", quit_it))
    screen_rect = screen.get_rect()
    menu_width = screen_rect.width / len(menu_items)
    temp_x = 0
    for i in menu_items:
        menu_buttons[i[0].lower()] = Button((temp_x,0,menu_width,30),RED, i[1], text=i[0], **BUTTON_STYLE_1)
        temp_x += menu_width

def login(user, password):
    if len(user) == 0 or len(password) == 0:
        return 1
    try:
        s = requests.Session()
        session["url"] = "http://discopython.inhavk.ru/"
        r = s.get(session["url"])
        i = r.text.find("csrfmiddlewaretoken")
        session["csrfmiddlewaretoken"] = r.text[i+28:i+28+32]
        r = s.post(session["url"], data={"username": user, "password": password, "sign_in": 0, "csrfmiddlewaretoken": session["csrfmiddlewaretoken"]})
        if r.text.find("Введите правильный логин и пароль") != -1:
            return 2
        session["session"] = s
#        session["url_id"] = r.url
    except Exception:
        print("Все плохо!")
    return 0

def editor(text):
    def callback(*args):
        nonlocal text
        text = text1.get('1.0', 'end')
        root.destroy()

    root = Tk()
    root.title("Editor")
    root.geometry("400x500")
    text1=Text(root,height=25,width=30,font='Arial 12')
    text1.pack(side='left')
    text1.insert("1.0",text)
    scrollbar = Scrollbar(root)
    scrollbar.pack(side='right')
    scrollbar['command'] = text1.yview
    text1['yscrollcommand'] = scrollbar.set
    button = Tk_button(root, text="Change", width=30, command=callback)
    button.pack(side='top')
    root.mainloop()
    return text

def check_login():
    def callback(*args):
        if login(user.get(), password.get()) == 0:
            session["auth"] = 1
            session["username"] = user.get()
        root.destroy()

    root = Tk()
    root.title("Log In")
    root.geometry("300x90")
    user = Entry(root, bd = 5, width=40)
    user.focus()
    user.pack()
    password = Entry(root, bd = 5, show="*", width=40)
    password.pack()
    button = Tk_button(root, text="Log In", width=30, command=callback)
    button.pack()
    root.bind("<Return>", callback)
    root.mainloop()

def upload_track():
    def callback(*args):
        r = session["session"].get(session["url"]+"upload")
        i = r.text.find("csrfmiddlewaretoken")
        session["csrfmiddlewaretoken"] = r.text[i+28:i+28+32] #Грязные хаки
        data = json.dumps(notes)#.encode()
        files = {"source": ("{}_{}.json".format(session["username"], track_name.get()), data, 'application/octet-stream', {'Expires': '0'})}
        r = session["session"].post(session["url"]+"upload", files=files, data={"csrfmiddlewaretoken": session["csrfmiddlewaretoken"]})
        root.destroy()

    root = Tk()
    root.title("Upload")
    root.geometry("300x90")
    track_name = Entry(root, bd = 5, width=40)
    track_name.focus()
    track_name.pack()
    button = Tk_button(root, text="Upload", width=30, command=callback)
    button.pack()
    root.bind("<Return>", callback)
    root.mainloop()

def rr_upload_track():
    r = session["session"].get(session["url"]+"upload")
    i = r.text.find("csrfmiddlewaretoken")
    session["csrfmiddlewaretoken"] = r.text[i+28:i+28+32] #Грязные хаки
    data = json.dumps(notes)#.encode()

    files = {"source": ("{}{}.json".format(session["username"], get_time()), data, 'application/octet-stream', {'Expires': '0'})}
    r = session["session"].post(session["url"]+"upload", files=files, data={"csrfmiddlewaretoken": session["csrfmiddlewaretoken"]})
    print(r.text)

def download_track():
    def callback(*args):
        global notes
        if len(track_id.get()):
            r = session["session"].get(session["url"]+"download/"+track_id.get())
            notes = json.loads(r.text)
        root.destroy()

    root = Tk()
    root.title("Download")
    root.geometry("300x90")
    track_id = Entry(root, bd = 5, width=20)
    track_id.focus()
    track_id.pack()
    button = Tk_button(root, text="Download", width=30, command=callback)
    button.pack()
    root.bind("<Return>", callback)
    root.mainloop()

def edit_track():
    global notes
    text = json.dumps(notes)
    #Что-то тут ужас какой-то. Впрочем, здесь везде ужас...
    text = text.replace("[[","[\n    [")
    text = text.replace("],","],\n")
    text = text.replace("\n[","\n    [")
    text = text.replace("]]","]\n]")
    valid = 0
    while not valid:
        try:
            text = editor(text)
            notes = json.loads(text)
            valid = 1
        except Exception:
            pass

check_login()
if not session["auth"]:
    exit()

pygame.mixer.init(44100,16,2,1024)
screen = pygame.display.set_mode((400,150))
pygame.init()

buttons = {}
menu_buttons = {}
create_menu()

buttons["record"] = Button((0,40,80,20),RED, start_record,
                 text="Start Record", **BUTTON_STYLE_1)
buttons["keys"] = Button((90,40,80,20),RED, change_keys,
                 text="Keys", **BUTTON_STYLE_1)
buttons["upload"] = Button((180,40,80,20),RED, upload_track,
                 text="Upload", **BUTTON_STYLE_1)
buttons["edit"] = Button((0,40,80,20),RED, edit_track,
                 text="Edit", **BUTTON_STYLE_1)
buttons["edit"].hide()
buttons["play"] = Button((90,40,80,20),RED, play_record,
                 text="Play", **BUTTON_STYLE_1)
buttons["play"].hide()
buttons["download"] = Button((270,40,80,20),RED, download_track,
                 text="Download", **BUTTON_STYLE_1)
buttons["download"].hide()

clock = pygame.time.Clock()
start_record_time = -1
notes = []
play_notes = []
temp_notes = {}

samples =  {}
is_playing = {}
load_db('db_samples.json')
config_and_status["keys"] = open('test.json').read()
load_keys(config_and_status["keys"])

while True:
    clock.tick(1000)
    event_time = get_time()
    event = pygame.event.poll()
    if event.type != pygame.NOEVENT:
            buttons_update(event, menu_buttons)
            buttons_update(event, buttons)
            pygame.display.update()
    if mode == 0:
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
                    notes.append((event_time - start_record_time, config_and_status["key_to_sample"][key], event_time - temp_notes[key]))
                samples[key].fadeout(50)
                is_playing[key] = False
    elif mode == 1:
        if start_record_time == -1:
                start_record_time = get_time()

        tick_time = event_time - start_record_time

        if len(temp_notes) > 0:
            for i in list(temp_notes.keys()):
                if temp_notes[i] <= tick_time:
                    samples[i].fadeout(50)
                    temp_notes.pop(i)

        if len(play_notes) > 0:
            if play_notes[0][1] not in db_samples.keys():
                play_notes.pop(0)
            elif play_notes[0][0] <= tick_time:
                if play_notes[0][1] not in samples.keys():
                    samples[play_notes[0][1]] = pygame.mixer.Sound(SAMPLES_PATH + db_samples[play_notes[0][1]])
                note = play_notes.pop(0)
                temp_notes[note[1]] = note[0] + note[2] #Set stop time
                samples[note[1]].play(fade_ms=50)

        if len(play_notes) == 0 and len(temp_notes) == 0:
            mode = 0

pygame.quit()