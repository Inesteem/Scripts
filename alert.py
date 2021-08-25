#!/usr/bin/env python3

# Note: Install cronjob with sudo crontab -e
# Add line: */2 * * * * su USERNAME -c "DISPLAY=:0.0  /usr/bin/python3 /usr/share/scripts/alert.py"; 

import psutil
import subprocess

import tkinter as tk
from tkinter import messagebox

import os
duration = 1  # seconds
freq = 440  # Hz

def checkSwap():
    swapMem = psutil.swap_memory()[3]
    if swapMem > 25:
        os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
        root = tk.Tk()
        root.after(60000, root.destroy)
        root.wit<hdraw()
        messagebox.showwarning('swap memory usage increasing', "swap memory is used up for " + str(swapMem) + "%")

def checkMem():
    result = subprocess.run(['free', '-m'], stdout=subprocess.PIPE)
    l=[x.strip() for x in str(result.stdout).split('\\n')]
    l=l[1].split()
    total = float(l[1])
    used = float(l[2])
    usedMem=used/total*100
    if usedMem > 25:
        os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
        root = tk.Tk()
        root.after(60000, root.destroy)
        root.withdraw()
        messagebox.showwarning('memory usage increasing', "memory is used up for %.2f " % (usedMem) + "%")
        
if __name__ == "__main__":
    try:
        checkSwap()
    except Exception as e:
        pass
    try:
        checkMem()
    except Exception as e:
        pass
