import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
from PIL import Image, ImageTk
import os
import time

# -----------------------------Define functions---------------------------------

current = None
position = 0

def play(*args):    
    global current
    global position
            
    if status.get() == 'Paused':        
        
        if current !=  playlist.get('active'):
            current = playlist.get('active')
            position = 0
            mixer.music.load(current)
            mixer.music.play()
            time_slider.set(0)
            slide()            
            
        else:
            mixer.music.unpause()

        status.set('Playing')
        play_button.configure(image = pause_image)
    
    elif status.get() == 'Playing':
        mixer.music.pause()
        status.set('Paused')
        play_button.configure(image = play_image)

def previous():
    previous_song = playlist.curselection()[0] - 1
    playlist.selection_clear('active')
    playlist.selection_set(previous_song)
    playlist.activate(previous_song)
    status.set('Paused')
    play()

def next():
    next_song = playlist.curselection()[0] + 1
    playlist.selection_clear('active')
    playlist.selection_set(next_song)
    playlist.activate(next_song)
    status.set('Paused')
    play()

def slide():
    if status.get() == 'Playing': 
        len = MP3(current).info.length
        time = position + mixer.music.get_pos() / 1000
        pos = time / len
        timescale.set(pos)
    root.after(1000, slide)

def set_position(event):
    global position
    length = MP3(current).info.length
    position = timescale.get() * length
    mixer.music.stop()
    mixer.music.play()
    mixer.music.set_pos(position)
    
def browse():
    global folder_path
    folder_path = filedialog.askdirectory()
    os.chdir(folder_path)
    songs = os.listdir()
    for song in songs:
        playlist.insert(tk.END, song)
    
# -----------------------Initialize window and set variables--------------------

root = tk.Tk()
root.geometry('384x384')
root.resizable(False, False)
root.config(bg = 'black')
root.title('Music Player')

volume = tk.DoubleVar(value = .5)
timescale = tk.DoubleVar(value = 0)

mixer.init()
mixer.music.set_volume(volume.get())

status = tk.StringVar()
status.set('Paused')

directory = os.getcwd()

# --------------------------------Playlist--------------------------------------

playlist = tk.Listbox(
                      fg = 'green', 
                      bg = 'black', 
                      selectforeground = 'black', 
                      selectbackground = 'green', 
                      width = 40
                      )
playlist.place(relx = .5, y = 100, anchor = 'center')

# ----------------------------- Time slider ------------------------------------

time_slider = ttk.Scale(length = 250, variable = timescale)
time_slider.place(relx = .5, y = 225, anchor = tk.CENTER)
time_slider.state(['disabled'])
playlist.bind('<Button-1>', lambda x: time_slider.state(['!disabled', 'selected']))

time_slider.bind('<ButtonRelease-1>', set_position)


# -----------------------------Volume slider------------------------------------

volume_slider = ttk.Scale(variable = volume)
volume_slider.place(relx = .5, y = 325, anchor = tk.CENTER)

volume_slider.bind('<Motion>', lambda x: mixer.music.set_volume(volume.get()))

# ---------------------------------Buttons--------------------------------------

previous_img = Image.open(rf'{directory}\buttons\previous.png').resize([50, 50])
previous_image = ImageTk.PhotoImage(previous_img)
previous_button = tk.Button(image = previous_image, bg = 'green', command = previous)
previous_button.place(x = 142, y = 275, anchor = tk.CENTER)

play_img = Image.open(rf'{directory}\buttons\play.png').resize([50, 50])
play_image = ImageTk.PhotoImage(play_img)
pause_img = Image.open(rf'{directory}\buttons\pause.png').resize([50, 50])
pause_image = ImageTk.PhotoImage(pause_img)
play_button = tk.Button(image = play_image, bg = 'green', command = play)
play_button.place(x = 192, y = 275, anchor = tk.CENTER)

next_img = Image.open(rf'{directory}\buttons\next.png').resize([50, 50])
next_image = ImageTk.PhotoImage(next_img)
next_button = tk.Button(image = next_image, bg = 'green', command = next)
next_button.place(x = 242, y = 275, anchor = tk.CENTER)

folder_img = Image.open(rf'{directory}\buttons\folder.png').resize([25, 25])
folder_image = ImageTk.PhotoImage(folder_img)
folder_button = tk.Button(image = folder_image, command = browse)
folder_button.place(x = 350, y = 100, anchor = tk.CENTER)

root.bind('<Return>', play)
root.bind('<space>', play)

root.mainloop()

