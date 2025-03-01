from tkinter import *
import math
import os
import sys
import ctypes
import winsound

#---------------------------SYSTEM FUNCTION MANAGEMENTS------------------------------#

def resource_path(relative_path):
    """To add the files in the pyinstaller otherwise it was not adding the data like icons,pngs,music etc."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def bring_in_front():
    window.attributes('-topmost', 1)
    window.after(1000, lambda: window.attributes('-topmost', 0))
    ctypes.windll.user32.SetForegroundWindow(window.winfo_id())


# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text,text="00:00")
    label.config(text="Timer")
    check_mark.config(text="")
    global reps
    reps = 0
# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        bring_in_front()
        winsound.PlaySound("break.wav",winsound.SND_ALIAS)
        label.config(text="Long Break",fg=RED)

    elif reps % 2 == 0:
        count_down(short_break_sec)
        bring_in_front()
        winsound.PlaySound("break.wav", winsound.SND_ALIAS)
        label.config(text="Break", fg=PINK)

    else:
        count_down(work_sec)
        bring_in_front()
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
        label.config(text="Work", fg=GREEN)



# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
"""so the complete countdown functionality will be here defined and work.. :) """
def count_down(count):
    count_min = math.floor(count/60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text,text=f"{count_min}:{count_sec}")   #text= is the keyword argument here (kwargs).
    if count > 0:
        global timer
        timer = window.after(1000,count_down,count-1) #after function wait for M Seconds specified and do something after that.
    else:
        start_timer()
        mark = ""
        completed_sessions = math.floor(reps/2)
        for _ in range(completed_sessions):
            mark += "✔️"
            check_mark.config(text=mark)

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.config(padx=50,pady=50)
window.title("Pomodoro") #pomodoro means tomato in italian.
window.minsize(height=250,width=300)
window.config(bg=YELLOW)
label = Label(text="Timer",font=(FONT_NAME,35,),fg=GREEN,bg=YELLOW)
label.grid(column=1,row=0)

canvas = Canvas(height=230,width=224,bg=YELLOW,highlightthickness=0)
tomato_img = PhotoImage(file=resource_path("tomato.png")) #that's how we can use image in an canvas.
canvas.create_image(103,112,image=tomato_img)
timer_text = canvas.create_text(103,130,text="00:00",fill="white",font=(FONT_NAME,35,"bold"))
canvas.grid(column=1,row=1)

#buttons
button_start = Button(text="Start",width=8, command=start_timer) #commad was not taking count() function directly so we created another function to trigger  count function.
button_start.grid(column=0,row=2)
button_reset = Button(text="Reset",width=8,command=reset_timer)
button_reset.grid(column=2,row=2)

#checkmarks mechanism
check_mark = Label(text="")
check_mark.grid(column=1,row=3)

window.mainloop()