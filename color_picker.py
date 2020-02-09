import tkinter
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from functools import partial
from PIL import ImageTk, Image

window = Tk()
tab_control = ttk.Notebook(window)
tab_1 = ttk.Frame(tab_control)
tab_control.add(tab_1, text="Instructions")
tab_2 = ttk.Frame(tab_control)
tab_control.add(tab_2, text="Color Picker")
tab_3 = ttk.Frame(tab_control)
tab_control.add(tab_3, text="Converter")
tab_control.pack(expand=1, fill="both")
tab_control.select(1)
window_width = 550
window_height = 475
title_height = 50
right_frame_width = window_width/2
right_frame_height = window_height - title_height - 30
left_frame_height = right_frame_height - 15
left_frame_width = (int)(right_frame_width - 30)
window_font = "system"
bg_color = "#111111"
text_color = "#ffffff"
title_color = "#00d100"
start_color = "#000000"
center_btn_text = "#000000"
center_btn_bg = "#f0f0f0"
result_color = "#11aa11"
base_color = []
base_color.append(start_color)
prev_color = []
prev_color.append(base_color[0])
sub_btn_color = "#ff0000"
add_btn_color = "#009900"
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
    4 :  "#4444ff",
    5 : "#a020a0"
}
color_code_goal = {
    0 : "#ff0000",
    1 : "#ff8822",
    2 : "#ffff00",
    3 : "#00bb00",
    4 :  "#0000ff",
    5 : "#800080"
}
steps_to_goal = {
    1 : 30,
    2 : 8,
    3 : 3,
    4 : 1.5
}

def entry_show_color(event):
    show_color()

def show_color():
    color_code = search_bar.get()
    base_color[0] = color_code
    if (color_code[0] != "#"):
        messagebox.showerror("Invalid Format", 'Include "#" before the code')
        search_bar.delete(0, END)
        return
    elif (len(color_code) != 7):
        messagebox.showerror("Invalid Format", "Not a hex color code")
        search_bar.delete(0, END)
        return
    for x in range(1,7):
        if(color_code[x] == "#"):
            messagebox.showerror("Invalid Format", "Not a hex color code")
            search_bar.delete(0, END)
            return
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

def add_color(slider_num, add_or_sub):
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
    for x in range(1,5):
        if(x == slider_val):
            curr_r = change_color(curr_r, r_diff, target_r, increment(target_r, slider_val, r_diff, add_or_sub), add_or_sub)
            curr_g = change_color(curr_g, g_diff, target_g, increment(target_g, slider_val, g_diff, add_or_sub), add_or_sub)
            curr_b = change_color(curr_b, b_diff, target_b, increment(target_b, slider_val, b_diff, add_or_sub), add_or_sub)
            break;
    curr_color = "#" + curr_r + curr_g + curr_b
    prev_color[0] = base_color[0]
    base_color[0] = curr_color
    update_darkness(bw.get())

def change_color(curr_code, diff, target, increment, add_or_sub):
    if(add_or_sub == "add"):
        if(abs(diff) > abs(increment)):
            new_code = int(curr_code, base=16) + increment
        elif(abs(diff) <= abs(increment)):
            new_code = int(target, base=16)
    elif(add_or_sub == "sub"):
        if(increment == 0):
            new_code = int(curr_code, base=16)
        elif (increment > 0 and 255-int(curr_code, base=16) > increment):
            new_code = int(curr_code, base=16) + increment
        elif(increment > 0 and 255-int(curr_code, base=16) <= increment):
            new_code = 255
        elif(increment < 0 and int(curr_code, base=16) > abs(increment)):
            new_code = int(curr_code, base=16) + increment
        elif(increment < 0 and int(curr_code, base=16) <= abs(increment)):
            new_code = 0
    ret_val = hex(new_code)[2:4]
    if (len(ret_val) == 1):
        return ("0" + ret_val)
    else:
        return ret_val

def increment(code, slider_val, diff, add_or_sub):
    if(add_or_sub == "add"):
        add_sub_factor = 1
    elif(add_or_sub == "sub"):
        add_sub_factor = -1
    if(diff > 0):
        percent = (int(code, base=16)/255)/steps_to_goal[slider_val]
        ret_val = percent * 255 * add_sub_factor
    elif(diff <= 0):
        percent = (1-(int(code, base=16)/255))/steps_to_goal[slider_val]
        ret_val = percent * -255 * add_sub_factor
    return int(ret_val)

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

def center_darkness():
    bw.set(0)
    result_code.config(text="")

def go_to_picker_tab():
    tab_control.select(1)

def clear_ghost_text(event):
    if(text_box.get() == "Ex: (192, 0, 255)" or text_box.get() == "Ex: #30bc82"):
        text_box.delete(0, 'end')
        text_box.insert(0, '')

def add_ghost_text(event):
    if((text_box.get() == "" and conv_title.cget('text')[0] == "D") or (event == "swapped" and conv_title.cget('text')[0] == "D")):
        text_box.delete(0, 'end')
        text_box.insert(0, "Ex: (192, 0, 255)")
    elif((text_box.get() == "" and conv_title.cget('text')[0] == "H") or (event == "swapped" and conv_title.cget('text')[0] == "H")):
        text_box.delete(0, 'end')
        text_box.insert(0, "Ex: #30bc82")

def focus(event):
    tab_3.focus()

def convert_with_event(event):
    convert()

def convert():
    entry = text_box.get()
    if(conv_title.cget('text')[0] == "D"):
        codes = entry[1:-1].split(', ')
        if(len(codes) != 3):
            messagebox.showerror("Invalid Format", 'Please enter a valid color')
            return
        try:
            for code in codes:
                if(not 0<=int(code)<=255):
                    messagebox.showerror("Invalid", 'Please enter a valid color')
                    return
        except:
            messagebox.showerror("Invalid Format", 'Please enter a valid color')
        converted_r = hex(int(codes[0]))[2:4]
        if(len(converted_r) == 1):
            converted_r = "0" + converted_r
        converted_g = hex(int(codes[1]))[2:4]
        if (len(converted_g) == 1):
            converted_g = "0" + converted_g
        converted_b = hex(int(codes[2]))[2:4]
        if (len(converted_b) == 1):
            converted_b = "0" + converted_b
        converted = "#" + converted_r + converted_g + converted_b
        conv_result.config(text=converted)
    else:
        if (entry[0] != "#"):
            messagebox.showerror("Invalid Format", 'Include "#" before the code')
            return
        elif (len(entry) != 7):
            messagebox.showerror("Invalid Format", "Not a hex color code")
            return
        for i in range(1,7):
            if(entry[i] == '#'):
                messagebox.showerror("Invalid Format", "Not a hex color code")
                return
    r = entry[1:3]
    g = entry[3:5]
    b = entry[5:7]
    conv_r = int(r, base=16)
    conv_g = int(g, base=16)
    conv_b = int(b, base=16)
    conv_result.config(text=("(" + str(conv_r) + ", " + str(conv_g) + ", " + str(conv_b) + ")"))


def convert_entry_validate(value, action, index):
    if(conv_title.cget('text')[0] == "D"):
        if(value == "Ex: (192, 0, 255)"):
            return True
        if (action == '1'):
            if(len(value) == 1):
                if(len(text_box.get()) > 0):
                    if (ord(text_box.get()[-1]) == 41 and int(index) == len(text_box.get())):
                        return False
                if (value == '(' or value == ')' or value == ' ' or value == ',' or '0' <= value <= '9'):
                    return True
                else:
                    return False
        else:
            return True
    else:
        if (value == "Ex: #30bc82"):
            return True
        if (action == '1'):
            if (len(text_box.get()) >= 7):
                return False
            if (65 <= ord(value) <= 90):
                value = chr(ord(value) + 32)
            if (value == '#' or 'a' <= value <= 'f' or '0' <= value <= '9'):
                return True
            else:
                return False
        else:
            return True

def swap():
    focus(0)
    conv_result.config(text="")
    if(conv_title.cget('text') == "Decimal to Hex Converter"):
        conv_title.config(text="Hex to Decimal Converter")
        conv_label.config(text="Enter a color in hexadecimal format")
        swap_btn.config(text="Decimal to Hex")
    else:
        conv_title.config(text="Decimal to Hex Converter")
        conv_label.config(text="Enter a color in decimal format")
        swap_btn.config(text="Hex to Decimal")
    add_ghost_text("swapped")

def undo():
    base_color[0] = prev_color[0]
    update_darkness(bw.get())

'''
INSTRUCTIONS TAB
'''

#Title
title_frame = Frame(tab_1, width=window_width, height=75, bg=bg_color)
title_frame.pack()
title_frame.focus()
title_frame.pack_propagate(0)
welcome_to = Label(title_frame, font=(window_font, 16), text='Welcome to', fg=title_color, bg=bg_color)
welcome_to.pack(fill='x')
title = Label(title_frame, font=(window_font, 30), text="Perfect Color Finder", fg=title_color, bg=bg_color)
title.pack(expand=1)
buffer = Frame(tab_1, width=window_width, height=35, bg=bg_color)
buffer.pack()

#Text Areas
text_areas = Frame(tab_1, width=window_width, height=window_width-75-25, bg=bg_color)
text_areas.pack()
text_areas.pack_propagate(0)

#Instructions
buffer = Frame(text_areas, height=window_height-75, width=15, bg=bg_color)
buffer.pack(side=LEFT)
instruction_frame = Frame(text_areas, height=window_height-75-25, width=window_width/2, bg=bg_color)
instruction_frame.pack(side=LEFT)
instruction_frame.grid_propagate(0)
title = Label(instruction_frame, font=(window_font, 20), text="Instructions", bg=bg_color, fg=text_color)
title.grid(row=0, sticky=N)
step_1_frame = Frame(instruction_frame, width=window_width/2, height=(window_height-75-30)/5, bg=bg_color)
step_1_frame.grid(row=1, sticky=W)
step_1 = Label(step_1_frame, pady=10, font=(window_font, 12), justify=LEFT, wraplength=window_width/2, text="1. Enter the base color you would like to start with", bg=bg_color, fg=text_color)
step_1.pack()
step_2_frame = Frame(instruction_frame, width=window_width/2, height=(window_height-75-30)/5, bg=bg_color)
step_2_frame.grid(row=2, sticky=W)
step_2 = Label(step_2_frame, pady=10, font=(window_font, 12), justify=LEFT, wraplength=window_width/2, text="2.  Adjust the slider to select how much of a color you want to add or subtract", bg=bg_color, fg=text_color)
step_2.pack()
step_3_frame = Frame(instruction_frame, width=window_width/2, height=(window_height-75-30)/5, bg=bg_color)
step_3_frame.grid(row=3, sticky=W)
step_3 = Label(step_3_frame, pady=10, font=(window_font, 12), justify=LEFT, wraplength=window_width/2, text="3. Click the add or subtract button", bg=bg_color, fg=text_color)
step_3.pack()
step_4_frame = Frame(instruction_frame, width=window_width/2, height=(window_height-75-30)/5, bg=bg_color)
step_4_frame.grid(row=4, sticky=W)
step_4 = Label(step_4_frame, pady=10, font=(window_font, 12), justify=LEFT, wraplength=window_width/2, text='4. Click "Get Code" once you have found your perfect color', bg=bg_color, fg=text_color)
step_4.pack()

#Guide
guide_frame = Frame(text_areas, height=window_height-75-30, width=window_width/2, bg=bg_color)
guide_frame.pack(side=LEFT)
guide_frame.grid_propagate(0)
guide_frame.pack_propagate(0)
guide_label = Label(guide_frame, font=(window_font, 20), text="Guide", bg=bg_color, fg=text_color)
guide_label.pack(fill='x')
color_names = Frame(guide_frame, width=100, height=250, bg=bg_color)
color_names.place(anchor=NE, x=window_width/4, y=50)
color_names.pack_propagate(0)
color_codes = Frame(guide_frame, width=100, height=250, bg=bg_color)
color_codes.place(anchor=NW, x=window_width/4, y=50)
color_codes.pack_propagate(0)
for x in range(0,6):
    name = Label(color_names, font=(window_font,  15, 'bold'), text=(color_label[x].upper() + " -"), fg=color_code_font[x], bg=bg_color)
    name.pack(fill='x', pady=5)
    code = Label(color_codes, font=(window_font, 15), text=color_code_goal[x], bg=bg_color, fg=text_color)
    code.pack(fill='x', pady=5)
cont_btn = Button(guide_frame, text="Continue", font=window_font, command=go_to_picker_tab, fg=text_color, bg=bg_color)
cont_btn.place(rely=.983, relx=.78, anchor=SE)

'''
COLOR FINDER TAB
'''

#Laying out the frames
tab_2_frame = Frame(tab_2, height=window_height, width=window_width, bg=bg_color)
tab_2_frame.pack()
title_frame = Frame(tab_2, height=title_height, width=550, bg=bg_color)
title_frame.place(anchor=NW, x=0, y=0)
title_frame.pack_propagate(0)
right_frame = Frame(tab_2, height=right_frame_height, width=right_frame_width, bg=bg_color)
right_frame.place(anchor=NW, x=window_width-right_frame_width, y=title_height)
left_spacer = Frame(tab_2, width=left_frame_width, height=15)
left_frame = Frame(tab_2, height=left_frame_height, width=left_frame_width, bg=bg_color)
left_frame.place(anchor=NW, x=0, y=title_height + 7)

#Title
title = Label(title_frame, text="Perfect Color Finder", font=(window_font, 24, "bold"), fg=title_color, bg=bg_color)
title.place(relx=.5, rely=.5, anchor=CENTER)

#Right side
search = Frame(right_frame, pady=10, bg=bg_color)
search.place(width=right_frame_width)
preview = Frame(right_frame, bg=start_color, highlightthickness=2, highlightbackground="#ffffff")
preview.place(width=window_width/4, height=window_width/4, x=window_width/8, y=100)
get_code = Frame(right_frame, bg=bg_color)
get_code.place(width=right_frame_width, height=50, y=100+(window_width/4))
result_code_frame = Frame(right_frame, bg=bg_color)
result_code_frame.place(y=310, width=right_frame_width, height=50)
undo_img = Image.open('undo.jpg')
undo_img = undo_img.resize((20, 15), Image.ANTIALIAS)
undo_img = ImageTk.PhotoImage(undo_img)
undo_btn = Button(right_frame, image=undo_img, height=20, width=20, command=undo)
undo_btn.place(anchor=CENTER, relx=.85, rely=.43)

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
result_code = Label(result_code_frame, text="", font=(window_font, 18), fg=result_color, bg=bg_color)
result_code.pack(expand=True)

#Black/White Slider
bw_frame = Frame(tab_2, height=160, width=90, bg=bg_color)
bw_frame.place(y=140, x=250, anchor=NW)
bw_frame.pack_propagate(0)
lighter = Label(bw_frame, text="Lighter", font=(window_font, 8), fg=text_color, bg=bg_color, width=90)
lighter.pack(side=TOP)
darker = Label(bw_frame, text="Darker", font=(window_font, 8), fg=text_color, bg=bg_color, width=90)
darker.pack(side=BOTTOM)
bw = Scale(bw_frame, showvalue=0, from_=-1, to=1, resolution=.02, command=update_darkness, bg=bg_color,
           troughcolor=text_color, highlightbackground=bg_color)
bw.place(anchor=CENTER, relx=.5, rely=.5)
center_btn = Button(bw_frame, text="O", font=(window_font, 10), fg=center_btn_text, bg=center_btn_bg, command=center_darkness)
center_btn.place(height = 18, width = 18, anchor=CENTER, rely=.5, relx = .8)

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
                        sliderlength=slider_length, command=partial(change_label, slider_num), fg="#ffffff",
                        bg=color_code_font[slider_num], highlightbackground=bg_color, font=(window_font, 10, 'bold'), troughcolor=bg_color)
    color_scale.pack(side=TOP)
    add_btn = Button(button_frame, bg=add_btn_color, fg="#000000", text="+", padx=4, pady=1, font=(window_font, 10, 'bold'), command=partial(add_color, slider_num, "add"))
    add_btn.place(anchor=CENTER, relx=.5, y=32, height=18, width=18)
    sub_btn = Button(button_frame, bg=sub_btn_color, fg="#000000", text="--", padx=6, font=(window_font, 10, 'bold'), command=partial(add_color, slider_num, "sub"))
    sub_btn.place(anchor=CENTER, relx=.5, height=18, width=18, y=slider_frames[slider_num].cget("height")-10)

#Exit Button
exit_btn = Button(window, text="Exit", font=window_font, command=window.destroy, fg=text_color, bg=bg_color)
exit_btn.place(rely=.98, relx=.98, anchor=SE)

'''
CONVERTER TAB
'''

#Title
tab_3.bind('<Button-1>', focus)
title_frame = Frame(tab_3, width=window_width, height=title_height + 50, bg=bg_color)
title_frame.pack()
title_frame.bind('<Button-1>', focus)
title_frame.pack_propagate(0)
conv_title = Label(title_frame, text="Decimal to Hex Converter", font=(window_font, 24, 'bold'), fg=title_color, bg=bg_color)
conv_title.pack(expand=1)
conv_title.bind('<Button-1>', focus)

#Search Bar
tab_3_frame = Frame(tab_3, height=window_height, width=window_width, bg=bg_color)
tab_3_frame.pack()
search = Frame(tab_3, width=window_width-100, height=window_height-100, bg=bg_color)
search.place(anchor=CENTER, relx=.5, rely=.65)
search.bind('<Button-1>', focus)
search.pack_propagate(0)
conv_label = Label(search, text="Enter a color in decimal format", font=(window_font, 16), fg=text_color, bg=bg_color)
conv_label.pack(pady=10)
conv_label.bind('<Button-1>', focus)
search_bar_frame = Frame(search, width=window_width-100, height=40, bg=bg_color)
search_bar_frame.pack(pady=20)
text_box = Entry(search_bar_frame, validate="key")
text_box['validatecommand'] = (text_box.register(convert_entry_validate), '%S', '%d', '%i')
text_box.pack(side=LEFT, padx=3, pady=3)
add_ghost_text(0)
search.focus()
text_box.bind('<Button-1>', clear_ghost_text)
text_box.bind('<FocusOut>', add_ghost_text)
text_box.bind('<Return>', convert_with_event)
go_btn = Button(search_bar_frame, text="Go", font=window_font, padx=10, fg=text_color, bg=bg_color, command=convert)
go_btn.pack(side=LEFT, padx=10)

#Result and swap button
conv_result = Label(search, text="", font=(window_font, 18), fg=result_color, bg=bg_color)
conv_result.pack(side=TOP, pady=30)
conv_result.bind('<Button-1>', focus)
swap_btn = Button(search, text="Hex to Decimal", padx=10, font=window_font, command=swap, fg=text_color, bg=bg_color)
swap_btn.pack(side=TOP, pady=50)

window.mainloop()