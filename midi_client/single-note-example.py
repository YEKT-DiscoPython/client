############################################################################
# A sample program to create a single-track MIDI file, add a note,
# and write to disk.
############################################################################

#Import the library
from make_midi.MidiFile3 import MIDIFile

# Create the MIDIFile Object
MyMIDI = MIDIFile(3)

# Add track name and tempo. The first argument to addTrackName and
# addTempo is the time to write the event.
MyMIDI.addTrackName(0,0,"Sample Track")
MyMIDI.addTempo(0,0, 120)

MyMIDI.addTrackName(1,0,"Sample Track 2")
MyMIDI.addTempo(1,0, 120)

MyMIDI.addTrackName(2,0,"Sample Track 3")
MyMIDI.addTempo(2,0, 120)

# Add a note. addNote expects the following information:
channel = 0
pitch = 60
duration = 1
volume = 100

MyMIDI.addNote(0,channel,pitch,0,duration,volume)

channel = 1
pitch = 60
duration = 2
volume = 100

MyMIDI.addNote(1,channel,pitch,0,duration,volume)

MyMIDI.addNote(2,channel,pitch,2,duration,volume)

MyMIDI.addNote(2,channel,pitch,4,duration,volume)

# And write it to disk.
binfile = open("output.mid", 'wb')
MyMIDI.writeFile(binfile)
binfile.close()

