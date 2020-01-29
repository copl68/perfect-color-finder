from tkinter import *
from tkinter import messagebox
from functools import partial

#Constants and setup
window = Tk()
window_width = 550
window_height = 450
title_height = 50
big_frame_width = window_width/2
big_frame_height = window_height-title_height
window_font = "system"
bg_color = "#f0f0f0"
text_color = "#000000"
window.title("Perfect Color Finder")
window.geometry(str(window_width) + 'x' + str(window_height))
window.resizable(0, 0)
start_color = "#ffffff"

def entry_show_color(event):
    show_color()

def show_color():
    color_code = search_bar.get()
    if (color_code[0] != "#"):
        messagebox.showerror("Invalid Format", 'Include "#" before the code')
        search_bar.delete(0, END)
    elif (len(color_code) != 7):
        messagebox.showerror("Invalid Format", "Not a hex color code")
        search_bar.delete(0, END)
    else:
        hash = False
        for x in color_code:
            if (65 <= ord(x) <= 90):
                x = chr(ord(x) + 32)
            if (x == '#' or 'a' <= x <= 'f' or '0' <= x <= '9'):
                if (x == '#' and not hash):
                    hash = True
                    continue
                elif (x == '#' and hash):
                    messagebox.showerror("Invalid Format", "Not a hex color code")
                    search_bar.delete(0, END)
            else:
                messagebox.showerror("Invalid Format", "Not a hex color code")
                search_bar.delete(0, END)
        search_bar.delete(0, END)
        preview.config(bg=color_code)

def is_hex_value(value, action):
    result_code.config(text="")
    if (action == '1'):
        if (len(search_bar.get()) >= 7):
            return False
        if (65 <= ord(value) <= 90):
            value = chr(ord(value) + 32)
        if (value == '#' or 'a' <= value <= 'f' or '0' <= value <= '9'):
            return True
        else:
            return False
    else:
        return True

def print_code():
    search_bar.delete(0, END)
    result_code.config(text=(preview.cget("bg")))

#Laying out the frames
title_frame = Frame(window, height=title_height, width=550, bg=bg_color)
title_frame.pack(side=TOP)
title_frame.pack_propagate(0)
right_frame = Frame(window, height=window_height-title_height, width=big_frame_width, bg=bg_color)
right_frame.pack(side=RIGHT)
left_frame = Frame(window, height=window_height-title_height, width=big_frame_width, bg=bg_color)
left_frame.pack(side=LEFT)

#Title
title = Label(title_frame, text="Perfect Color Finder", font=(window_font, 24, "bold"), fg="#a022a0", bg=bg_color)
title.place(relx=.5, rely=.5, anchor=CENTER)

#Right side
search = Frame(right_frame, pady=10, bg=bg_color)
search.place(width=big_frame_width)
preview = Frame(right_frame, bg=start_color, highlightthickness=2, highlightbackground="#000000")
preview.place(width=window_width/4, height=window_width/4, x=window_width/8, y=100)
get_code = Frame(right_frame, bg=bg_color)
get_code.place(width=big_frame_width, height=50, y=100+(window_width/4))
result_code_frame = Frame(right_frame, bg=bg_color)
result_code_frame.place(y=310, width=big_frame_width, height=50)

#Search frame
find_label = Label(search, text="Start with a base color (Ex: #cc3f67)", font=(window_font, 8), fg=text_color, bg=bg_color)
find_label.pack(side=TOP, pady=10)
search_bar_frame = Frame(search, bg=bg_color)
search_bar_frame.pack(side=TOP)

#Search bar frame
search_bar = Entry(search_bar_frame, validate="key")
search_bar['validatecommand'] = (search_bar.register(is_hex_value), '%S', '%d')
search_bar.bind("<Return>", entry_show_color)
search_bar.pack(side=LEFT)
search_bar.focus()
search_button = Button(search_bar_frame, text="Go", font=window_font, padx=10, command=show_color, fg=text_color, bg=bg_color)
search_button.pack(side=LEFT, padx=10)

#Get code frame
get_code_btn = Button(get_code, text="Get Color Code", font=window_font, command=print_code, fg=text_color, bg=bg_color)
get_code_btn.pack(expand=True)

#Result code frame
result_code = Label(result_code_frame, text="", font=(window_font, 18), fg="#11aa11", bg=bg_color)
result_code.pack(expand=True)

"""
START LEFT SIDE
"""

#Left side

slider_frames = []
for i in range(1, 7):
    frame = Frame(left_frame, width=big_frame_width, height=big_frame_height/6, highlightthickness=1, highlightbackground='#000000')
    frame.pack()
    slider_frames.append(frame)


#Build slider
color_name = Label(slider_frames[0], text="RED", font=(window_font, 20))
color_name.place(anchor=CENTER, relx=.5, rely=.5)

window.mainloop()
