import tkinter.ttk as ttk
import tkinter.filedialog
import pygame.mixer
import tkinter
import codecs
import glob
import os

def onKeyPress(event):
    if samples.get(event.char):
        assigned = 0
        for channel in channels:
            if channel.get_sound() == samples[event.char]:
                assigned = 1
                break
        if not assigned:
            for channel in channels:
                if not channel.get_busy():
                    channel.play(samples[event.char])
                    break

def onKeyRelease(event):
    if samples.get(event.char):
         for channel in channels:
            if channel.get_sound() == samples[event.char]:
                channel.stop()
                break

def openFile(key):
    path = tkinter.filedialog.askopenfilename(filetypes=[('WAVE files', '.wav')])
    if path != '':
        samples[key] = pygame.mixer.Sound(codecs.encode(path, 'utf-8'))

def loadPreset(path):
    if path != None:
        for channel in channels:
            if channel.get_sound() != None:
                channel.stop()
        i = 0
        for filename in glob.glob(os.path.join(path, '*.wav')):
            if i < len(keys):
                samples[keys[i]] = pygame.mixer.Sound(filename)
                i += 1
          
pygame.mixer.init(44100,16,2,1024)

root = tkinter.Tk()
root.title('KeyPads')
root.bind('<KeyPress>',   onKeyPress)
root.bind('<KeyRelease>', onKeyRelease)

mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0)
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

ttk.Button(mainframe, text='w', command=lambda:openFile('w')).grid(column=0, row=0)
ttk.Button(mainframe, text='e', command=lambda:openFile('e')).grid(column=0, row=1)
ttk.Button(mainframe, text='r', command=lambda:openFile('r')).grid(column=0, row=2)
ttk.Button(mainframe, text='t', command=lambda:openFile('t')).grid(column=0, row=3)
ttk.Button(mainframe, text='y', command=lambda:openFile('y')).grid(column=0, row=4)
ttk.Button(mainframe, text='u', command=lambda:openFile('u')).grid(column=0, row=5)
ttk.Button(mainframe, text='i', command=lambda:openFile('i')).grid(column=0, row=6)
ttk.Button(mainframe, text='o', command=lambda:openFile('o')).grid(column=0, row=7)
ttk.Button(mainframe, text='s', command=lambda:openFile('s')).grid(column=1, row=0)
ttk.Button(mainframe, text='d', command=lambda:openFile('d')).grid(column=1, row=1)
ttk.Button(mainframe, text='f', command=lambda:openFile('f')).grid(column=1, row=2)
ttk.Button(mainframe, text='g', command=lambda:openFile('g')).grid(column=1, row=3)
ttk.Button(mainframe, text='h', command=lambda:openFile('h')).grid(column=1, row=4)
ttk.Button(mainframe, text='j', command=lambda:openFile('j')).grid(column=1, row=5)
ttk.Button(mainframe, text='k', command=lambda:openFile('k')).grid(column=1, row=6)
ttk.Button(mainframe, text='l', command=lambda:openFile('l')).grid(column=1, row=7)

keys = ['w', 'e', 'r', 't', 'y', 'u', 'i', 'o',
        's', 'd', 'f', 'g', 'h', 'j', 'k', 'l']

global samples
samples =  {}

global channels
channels = [pygame.mixer.Channel(i) for i in range(8)]

loadPreset('808 Drum Machine')

global presets
presets = ('Yamaha RX-11', '808 Drum Machine', 'New Order', 'Electric Piano','Supersaw', 'Church Organ')
pnames = tkinter.StringVar(value=presets)

preset_list = tkinter.Listbox(mainframe, listvariable=pnames, height=10)
preset_list.grid(column=0, row=8)
ttk.Button(mainframe, text='Apply preset', command=lambda:loadPreset(presets[int(preset_list.curselection()[0])])).grid(column=1, row=8)

root.mainloop()
