import tkinter
from tkinter import *
from tkinter import messagebox
from functools import partial

#Constants and setup
window = Tk()
window_width = 550
window_height = 450
title_height = 50
right_frame_width = window_width/2
right_frame_height = window_height-title_height
left_frame_height = right_frame_height - 15
left_frame_width = (int)(right_frame_width - 30)
window_font = "system"
bg_color = "#f0f0f0"
text_color = "#000000"
start_color = "#ffffff"
base_color = []
base_color.append(start_color)
red = "#ff0000"
green = "#009900"
window.title("Perfect Color Finder")
window.geometry(str(window_width) + 'x' + str(window_height))
window.resizable(0, 0)
slider_length = 60
slider_dict = {
    1 : "Very little",
    2 : "Some",
    3 : "A lot",
    4 : "Tons"
}
color_label = {
    0 : "Red",
    1 : "Orange",
    2 : "Yellow",
    3 : "Green",
    4 : "Blue",
    5 : "Purple"
}
color_code_font = {
    0 : "#ff0000",
    1 : "#ff8822",
    2 : "#aaaa00",
    3 : "#009900",
    4 :  "#0000ff",
    5 : "#800080"
}
color_code_goal = {
    0 : "#ff0000",
    1 : "#ff8822",
    2 : "#ffff00",
    3 : "#00bb00",
    4 :  "#0000ff",
    5 : "#800080"
}
color_increments = {
    1 : 9,
    2 : 7,
    3 : 5,
    4 : 3
}

def entry_show_color(event):
    show_color()

def show_color():
    color_code = search_bar.get()
    base_color[0] = color_code
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

def change_label(slider_num, value):
    for widget in slider_frames[int(slider_num)].winfo_children():
        if isinstance(widget, tkinter.Scale):
            widget.config(label=slider_dict[(int)(value)])

def add_color(slider_num):
    result_code.config(text="")
    for widget in slider_frames[slider_num].winfo_children():
        if isinstance(widget, tkinter.Scale):
            slider_val = widget.get()
    curr_color = base_color[0]
    color = color_code_goal[slider_num]
    target_r = color[1:3]
    curr_r = curr_color[1:3]
    target_g = color[3:5]
    curr_g = curr_color[3:5]
    target_b = color[5:7]
    curr_b = curr_color[5:7]
    r_diff = int(str(int(target_r, base=16) - int(curr_r, base=16)), base=10)
    g_diff = int(str(int(target_g, base=16) - int(curr_g, base=16)), base=10)
    b_diff = int(str(int(target_b, base=16) - int(curr_b, base=16)), base=10)
    print("r: " + curr_r)
    print("g: " + curr_g)
    print("b: " + curr_b)
    for x in range(1,5):
        if(x == slider_val):
            print("g_diff/ " + str(int(g_diff/color_increments[slider_val])))
            curr_r = change_color(curr_r, target_r, r_diff, get_increment(r_diff, slider_val))
            curr_g = change_color(curr_g, target_g, g_diff, get_increment(g_diff, slider_val))
            curr_b = change_color(curr_b, target_b, b_diff, get_increment(b_diff, slider_val))
            break;
    curr_color = "#" + str(curr_r) + str(curr_g) + str(curr_b)
    base_color[0] = curr_color
    update_darkness(bw.get())
    print("r: " + curr_r)
    print("g: " + curr_g)
    print("b: " + curr_b)

def change_color(curr, target, diff, increment):
    if (abs(diff) > increment):
        curr = hex(int(curr, base=16) + int(increment))[2:4]
        if (len(curr) == 1):
            curr = "0" + curr
    elif (abs(diff) <= increment):
        curr = target
    return curr

def get_increment(diff, slider_val):
    increment = diff/color_increments[slider_val]
    if(increment < 0):
        increment_sign = -1
    elif(increment >= 0):
        increment_sign = 1
    if(slider_val == 1 and abs(increment) < 17):
        increment = 17*increment_sign
    elif(slider_val == 2 and abs(increment) < 34):
        increment = 34*increment_sign
    elif(slider_val == 3 and abs(increment) < 51):
        increment = 51*increment_sign
    elif(slider_val == 4 and abs(increment) < 68):
        increment = 68*increment_sign
    print("inc: " + str(increment))
    return increment

def update_darkness(value):
    value = float(value)
    if(value < 0):
        update_lightness(abs(value))
    else:
        old_r = int(base_color[0][1:3], base=16)
        old_g = int(base_color[0][3:5], base=16)
        old_b = int(base_color[0][5:7], base=16)
        new_r = hex(int(old_r * (1 - value)))[2:4]
        if(len(new_r) == 1):
            new_r = "0" + new_r
        new_g = hex(int(old_g * (1 - value)))[2:4]
        if (len(new_g) == 1):
            new_g = "0" + new_g
        new_b = hex(int(old_b * (1 - value)))[2:4]
        if (len(new_b) == 1):
            new_b = "0" + new_b
        preview.config(bg="#" + new_r + new_g + new_b)

def update_lightness(value):
    old_r = int(base_color[0][1:3], base=16)
    old_g = int(base_color[0][3:5], base=16)
    old_b = int(base_color[0][5:7], base=16)
    new_r = hex(int(old_r + (255 - old_r)*value))[2:4]
    if (len(new_r) == 1):
        new_r = "0" + new_r
    new_g = hex(int(old_g + (255 - old_g)*value))[2:4]
    if (len(new_g) == 1):
        new_g = "0" + new_g
    new_b = hex(int(old_b + (255 - old_b)*value))[2:4]
    if (len(new_b) == 1):
        new_b = "0" + new_b
    preview.config(bg="#" + new_r + new_g + new_b)

#Laying out the frames
title_frame = Frame(window, height=title_height, width=550, bg=bg_color)
title_frame.place(anchor=NW, x=0, y=0)
title_frame.pack_propagate(0)
right_frame = Frame(window, height=right_frame_height, width=right_frame_width, bg=bg_color)
right_frame.place(anchor=NW, x=window_width-right_frame_width, y=title_height)
left_spacer = Frame(window, width=left_frame_width, height=15)
#left_spacer.pack()
left_frame = Frame(window, height=left_frame_height, width=left_frame_width, bg=bg_color)
left_frame.place(anchor=NW, x=0, y=title_height + 7)

#Title
title = Label(title_frame, text="Perfect Color Finder", font=(window_font, 24, "bold"), fg="#a022a0", bg=bg_color)
title.place(relx=.5, rely=.5, anchor=CENTER)

#Right side
search = Frame(right_frame, pady=10, bg=bg_color)
search.place(width=right_frame_width)
preview = Frame(right_frame, bg=start_color, highlightthickness=2, highlightbackground="#000000")
preview.place(width=window_width/4, height=window_width/4, x=window_width/8, y=100)
get_code = Frame(right_frame, bg=bg_color)
get_code.place(width=right_frame_width, height=50, y=100+(window_width/4))
result_code_frame = Frame(right_frame, bg=bg_color)
result_code_frame.place(y=310, width=right_frame_width, height=50)

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
    frame = Frame(left_frame, width=left_frame_width, height=left_frame_height/6, bg=bg_color)
    frame.pack()
    frame.pack_propagate(0)
    slider_frames.append(frame)


#Build sliders
sliders = []
for slider_num in range(0,6):
    button_frame = Frame(slider_frames[slider_num], height=left_frame_height/6, width=40, bg=bg_color)
    button_frame.pack(side=RIGHT)
    button_frame.pack_propagate(0)
    color_name_frame = Frame(slider_frames[slider_num], bg=bg_color, width=left_frame_width-button_frame.cget("width"),
                             height=left_frame_height/18)
    color_name_frame.pack()
    color_name_frame.pack_propagate(0)
    color_name = Label(color_name_frame, bg=bg_color, text=color_label[slider_num], font=(window_font, 15, 'bold'), fg=color_code_font[slider_num])
    color_name.pack(expand=True)
    color_scale = Scale(slider_frames[slider_num], orient=HORIZONTAL, label="Very little", showvalue=0, length=160, from_=1, to=4,
                        sliderlength=slider_length, command=partial(change_label, slider_num))
    color_scale.pack(side=TOP)
    add_btn = Button(button_frame, bg=green, fg="#ffffff", text="+", padx=4, pady=1, font=(window_font, 10), command=partial(add_color, slider_num))
    add_btn.place(anchor=CENTER, relx=.5, y=32, height=18, width=18)
    sub_btn = Button(button_frame, bg=red, fg="#ffffff", text="-", padx=6, font=(window_font, 10))
    sub_btn.place(anchor=CENTER, relx=.5, height=18, width=18, y=slider_frames[slider_num].cget("height")-10)

#Black/White Slider
bw_frame = Frame(window, height=160, width=90)
bw_frame.place(y=140, x=250, anchor=NW)
bw_frame.pack_propagate(0)
lighter = Label(bw_frame, text="Lighter", font=(window_font, 8), fg=text_color, bg=bg_color, width=90)
lighter.pack(side=TOP)
darker = Label(bw_frame, text="Darker", font=(window_font, 8), fg=text_color, bg=bg_color, width=90)
darker.pack(side=BOTTOM)
bw = Scale(bw_frame, showvalue=0, from_=-1, to=1, resolution=.02, command=update_darkness)
bw.place(anchor=CENTER, relx=.5, rely=.5)

#Exit Button
exit_btn = Button(right_frame, text="Exit", font=window_font, command=window.destroy, fg=text_color, bg=bg_color)
exit_btn.place(rely=.98, relx=.98, anchor=SE)

window.mainloop()