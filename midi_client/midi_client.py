from open_midi.MIDI import *

class Note:
    def __init__(self, s_time, length, channel, pitch, velocity):
        self.s_time = s_time
        self.length = length
        self.channel = channel
        self.pitch = pitch
        self.velocity = velocity
        
print('Hello! This is a CLI midi editor. Choose one:')
while True:
    print('1. Open a track\n'
          '2. Build a new track\n'
          '3. Exit')
    a = int(input())

    if a == 1:

        midi_file = open('1.mid', 'rb').read()
        opus = midi2opus(midi_file)
        notes = []
        for i in range(1, len(opus)):
            length = 0
            s_time = 0
            channel = 0
            pitch = 0
            velocity = 0
            for event in opus[i]:
                if event[0] == 'note_on':
                    s_time = event[1]
                    channel = event[2]
                    pitch = event[3]
                    velocity = event[4]
                elif event[0] == 'note_off':
                    length = event[1]
                    a = Note(s_time,length,channel,pitch,velocity)
                    notes.append(a)
        for note in notes:
            print(note.s_time,note.length,note.pitch)
                     
        o_file = open('2.mid', 'wb')
        o_file.write(opus2midi(opus))
        o_file.close()
    elif a == 2:
        print('Not yet')
    elif a == 3:
        break
