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
WINDOW_WIDTH = 550
WINDOW_HEIGHT = 475
TITLE_HEIGHT = 50
RIGHT_FRAME_WIDTH = WINDOW_WIDTH/2
RIGHT_FRAME_HEIGHT = WINDOW_HEIGHT - TITLE_HEIGHT - 30
LEFT_FRAME_HEIGHT = RIGHT_FRAME_HEIGHT - 15
LEFT_FRAME_WIDTH = (int)(RIGHT_FRAME_WIDTH - 30)
WINDOW_FONT = "system"
BG_COLOR = "#111111"
TEXT_COLOR = "#ffffff"
TITLE_COLOR = "#00d100"
START_COLOR = "#000000"
CENTER_BTN_TEXT = "#000000"
CENTER_BTN_BG = "#f0f0f0"
RESULT_COLOR = "#11aa11"
SUB_BUTTON_COLOR = "#ff0000"
ADD_BUTTON_COLOR = "#009900"
SLIDER_LENGTH = 60
base_color = []
base_color.append(START_COLOR)
prev_color = []
prev_color.append(base_color[0])
window.title("Perfect Color Finder")
window.geometry(str(WINDOW_WIDTH) + 'x' + str(WINDOW_HEIGHT))
window.resizable(0, 0)
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
    '''
    Calls the show_color method without the requirement of a parameter

    :param event: Descriptor of the event resulting from pressing "Enter"
    '''
    show_color()

def show_color():
    '''
    Takes the entered hexadecimal code and makes it appear in the preview box or
    shows an error if the code is invalid.
    '''
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
    '''
    Checks to see if the character the user tries to enter is a valid character
    for a hexadecimal value.

    :param value: The character that the users tries to enter.
    :param action: Number determining whether the user tries to enter or delete a character.
    :return: Boolean value of whether or not the entered character is accepted.
    '''
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
    '''
    Outputs the hexadecimal code of the color in the preview box to the window
    '''
    search_bar.delete(0, END)
    result_code.config(text=(preview.cget("bg")))

def change_label(slider_num, value):
    '''
    Changes the label of a color slider

    :param slider_num: The index of the desired slider in slider_frames[]
    :param value: The value of the given slider
    '''
    for widget in slider_frames[int(slider_num)].winfo_children():
        if isinstance(widget, tkinter.Scale):
            widget.config(label=slider_dict[(int)(value)])

def add_color(slider_num, add_or_sub):
    '''
    Brings the current color closer to the color being added

    :param slider_num: The index of the desired slider in slider_frames[]
    :param add_or_sub: If the color is being added or subtracted.
    '''
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
    '''
    Updates a part or the RGB in the hexadecimal value once a color is added or subtracted.

    :param curr_code: The current hexadecimal code of an R, G, or B value
    :param diff: The difference between the current and target hex value
    :param target: The hex value of the target color
    :param increment: How much to add or subtract from the current hex value
    :param add_or_sub: If the color is being added or subtracted

    :return: The updated value of the hexadecimal value
    '''
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
    '''
    Determines how much should be added or subtracted to the current hexadecimal value

    :param code: The target hexadecimal value
    :param slider_val: The index of the desired slider in slider_frames[]
    :param diff: The difference between the current and target hexadecimal value.
    :param add_or_sub: If the color is being added or subtracted

    :return: The value of how much to add or subtract from the current hex value
    '''
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
    '''
    Changes how dark the current color is by making the code go closer to black

    :param value: The value of the darkness slider
    '''
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
    '''
    Changes how light the current color is by making it go closer to white

    :param value: The value of the darkness slider
    '''
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
    '''
    Sets the value of the darkness slider ot 0
    '''
    bw.set(0)
    result_code.config(text="")

def go_to_picker_tab():
    '''
    Sets the current visible tab to the color picker tab
    '''
    tab_control.select(1)

def clear_ghost_text(event):
    '''
    Deletes the example filler text if the user clicks on the text box

    :param event: Descriptor of the event resulting from focusing on the text box
    '''
    if(text_box.get() == "Ex: (192, 0, 255)" or text_box.get() == "Ex: #30bc82"):
        text_box.delete(0, 'end')
        text_box.insert(0, '')

def add_ghost_text(event):
    '''
    Adds example filler text to the text box when there is nothing else in the text box

    :param event: Descriptor of the event resulting from unfocusing on the textbox
    '''
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
title_frame = Frame(tab_1, width=WINDOW_WIDTH, height=75, bg=BG_COLOR)
title_frame.pack()
title_frame.focus()
title_frame.pack_propagate(0)
welcome_to = Label(title_frame, font=(WINDOW_FONT, 16), text='Welcome to', fg=TITLE_COLOR, bg=BG_COLOR)
welcome_to.pack(fill='x')
title = Label(title_frame, font=(WINDOW_FONT, 30), text="Perfect Color Finder", fg=TITLE_COLOR, bg=BG_COLOR)
title.pack(expand=1)
buffer = Frame(tab_1, width=WINDOW_WIDTH, height=35, bg=BG_COLOR)
buffer.pack()

#Text Areas
text_areas = Frame(tab_1, width=WINDOW_WIDTH, height=WINDOW_WIDTH-75-25, bg=BG_COLOR)
text_areas.pack()
text_areas.pack_propagate(0)

#Instructions
buffer = Frame(text_areas, height=WINDOW_HEIGHT-75, width=15, bg=BG_COLOR)
buffer.pack(side=LEFT)
instruction_frame = Frame(text_areas, height=WINDOW_HEIGHT-75-25, width=WINDOW_WIDTH/2, bg=BG_COLOR)
instruction_frame.pack(side=LEFT)
instruction_frame.grid_propagate(0)
title = Label(instruction_frame, font=(WINDOW_FONT, 20), text="Instructions", bg=BG_COLOR, fg=TEXT_COLOR)
title.grid(row=0, sticky=N)
step_1_frame = Frame(instruction_frame, width=WINDOW_WIDTH/2, height=(WINDOW_HEIGHT-75-30)/5, bg=BG_COLOR)
step_1_frame.grid(row=1, sticky=W)
step_1 = Label(step_1_frame, pady=10, font=(WINDOW_FONT, 12), justify=LEFT, wraplength=WINDOW_WIDTH/2, text="1. Enter the base color you would like to start with", bg=BG_COLOR, fg=TEXT_COLOR)
step_1.pack()
step_2_frame = Frame(instruction_frame, width=WINDOW_WIDTH/2, height=(WINDOW_HEIGHT-75-30)/5, bg=BG_COLOR)
step_2_frame.grid(row=2, sticky=W)
step_2 = Label(step_2_frame, pady=10, font=(WINDOW_FONT, 12), justify=LEFT, wraplength=WINDOW_WIDTH/2, text="2.  Adjust the slider to select how much of a color you want to add or subtract", bg=BG_COLOR, fg=TEXT_COLOR)
step_2.pack()
step_3_frame = Frame(instruction_frame, width=WINDOW_WIDTH/2, height=(WINDOW_HEIGHT-75-30)/5, bg=BG_COLOR)
step_3_frame.grid(row=3, sticky=W)
step_3 = Label(step_3_frame, pady=10, font=(WINDOW_FONT, 12), justify=LEFT, wraplength=WINDOW_WIDTH/2, text="3. Click the add or subtract button", bg=BG_COLOR, fg=TEXT_COLOR)
step_3.pack()
step_4_frame = Frame(instruction_frame, width=WINDOW_WIDTH/2, height=(WINDOW_HEIGHT-75-30)/5, bg=BG_COLOR)
step_4_frame.grid(row=4, sticky=W)
step_4 = Label(step_4_frame, pady=10, font=(WINDOW_FONT, 12), justify=LEFT, wraplength=WINDOW_WIDTH/2, text='4. Click "Get Code" once you have found your perfect color', bg=BG_COLOR, fg=TEXT_COLOR)
step_4.pack()

#Guide
guide_frame = Frame(text_areas, height=WINDOW_HEIGHT-75-30, width=WINDOW_WIDTH/2, bg=BG_COLOR)
guide_frame.pack(side=LEFT)
guide_frame.grid_propagate(0)
guide_frame.pack_propagate(0)
guide_label = Label(guide_frame, font=(WINDOW_FONT, 20), text="Guide", bg=BG_COLOR, fg=TEXT_COLOR)
guide_label.pack(fill='x')
color_names = Frame(guide_frame, width=100, height=250, bg=BG_COLOR)
color_names.place(anchor=NE, x=WINDOW_WIDTH/4, y=50)
color_names.pack_propagate(0)
color_codes = Frame(guide_frame, width=100, height=250, bg=BG_COLOR)
color_codes.place(anchor=NW, x=WINDOW_WIDTH/4, y=50)
color_codes.pack_propagate(0)
for x in range(0,6):
    name = Label(color_names, font=(WINDOW_FONT,  15, 'bold'), text=(color_label[x].upper() + " -"), fg=color_code_font[x], bg=BG_COLOR)
    name.pack(fill='x', pady=5)
    code = Label(color_codes, font=(WINDOW_FONT, 15), text=color_code_goal[x], bg=BG_COLOR, fg=TEXT_COLOR)
    code.pack(fill='x', pady=5)
cont_btn = Button(guide_frame, text="Continue", font=WINDOW_FONT, command=go_to_picker_tab, fg=TEXT_COLOR, bg=BG_COLOR)
cont_btn.place(rely=.983, relx=.78, anchor=SE)

'''
COLOR FINDER TAB
'''

#Laying out the frames
tab_2_frame = Frame(tab_2, height=WINDOW_HEIGHT, width=WINDOW_WIDTH, bg=BG_COLOR)
tab_2_frame.pack()
title_frame = Frame(tab_2, height=TITLE_HEIGHT, width=550, bg=BG_COLOR)
title_frame.place(anchor=NW, x=0, y=0)
title_frame.pack_propagate(0)
right_frame = Frame(tab_2, height=RIGHT_FRAME_HEIGHT, width=RIGHT_FRAME_WIDTH, bg=BG_COLOR)
right_frame.place(anchor=NW, x=WINDOW_WIDTH-RIGHT_FRAME_WIDTH, y=TITLE_HEIGHT)
left_spacer = Frame(tab_2, width=LEFT_FRAME_WIDTH, height=15)
left_frame = Frame(tab_2, height=LEFT_FRAME_HEIGHT, width=LEFT_FRAME_WIDTH, bg=BG_COLOR)
left_frame.place(anchor=NW, x=0, y=TITLE_HEIGHT + 7)

#Title
title = Label(title_frame, text="Perfect Color Finder", font=(WINDOW_FONT, 24, "bold"), fg=TITLE_COLOR, bg=BG_COLOR)
title.place(relx=.5, rely=.5, anchor=CENTER)

#Right side
search = Frame(right_frame, pady=10, bg=BG_COLOR)
search.place(width=RIGHT_FRAME_WIDTH)
preview = Frame(right_frame, bg=START_COLOR, highlightthickness=2, highlightbackground="#ffffff")
preview.place(width=WINDOW_WIDTH/4, height=WINDOW_WIDTH/4, x=WINDOW_WIDTH/8, y=100)
get_code = Frame(right_frame, bg=BG_COLOR)
get_code.place(width=RIGHT_FRAME_WIDTH, height=50, y=100+(WINDOW_WIDTH/4))
result_code_frame = Frame(right_frame, bg=BG_COLOR)
result_code_frame.place(y=310, width=RIGHT_FRAME_WIDTH, height=50)
undo_img = Image.open('undo.jpg')
undo_img = undo_img.resize((20, 15), Image.ANTIALIAS)
undo_img = ImageTk.PhotoImage(undo_img)
undo_btn = Button(right_frame, image=undo_img, height=20, width=20, command=undo)
undo_btn.place(anchor=CENTER, relx=.85, rely=.43)

#Search frame
find_label = Label(search, text="Start with a base color (Ex: #cc3f67)", font=(WINDOW_FONT, 8), fg=TEXT_COLOR, bg=BG_COLOR)
find_label.pack(side=TOP, pady=10)
search_bar_frame = Frame(search, bg=BG_COLOR)
search_bar_frame.pack(side=TOP)

#Search bar frame
search_bar = Entry(search_bar_frame, validate="key")
search_bar['validatecommand'] = (search_bar.register(is_hex_value), '%S', '%d')
search_bar.bind("<Return>", entry_show_color)
search_bar.pack(side=LEFT)
search_bar.focus()
search_button = Button(search_bar_frame, text="Go", font=WINDOW_FONT, padx=10, command=show_color, fg=TEXT_COLOR, bg=BG_COLOR)
search_button.pack(side=LEFT, padx=10)

#Get code frame
get_code_btn = Button(get_code, text="Get Color Code", font=WINDOW_FONT, command=print_code, fg=TEXT_COLOR, bg=BG_COLOR)
get_code_btn.pack(expand=True)

#Result code frame
result_code = Label(result_code_frame, text="", font=(WINDOW_FONT, 18), fg=RESULT_COLOR, bg=BG_COLOR)
result_code.pack(expand=True)

#Black/White Slider
bw_frame = Frame(tab_2, height=160, width=90, bg=BG_COLOR)
bw_frame.place(y=140, x=250, anchor=NW)
bw_frame.pack_propagate(0)
lighter = Label(bw_frame, text="Lighter", font=(WINDOW_FONT, 8), fg=TEXT_COLOR, bg=BG_COLOR, width=90)
lighter.pack(side=TOP)
darker = Label(bw_frame, text="Darker", font=(WINDOW_FONT, 8), fg=TEXT_COLOR, bg=BG_COLOR, width=90)
darker.pack(side=BOTTOM)
bw = Scale(bw_frame, showvalue=0, from_=-1, to=1, resolution=.02, command=update_darkness, bg=BG_COLOR,
           troughcolor=TEXT_COLOR, highlightbackground=BG_COLOR)
bw.place(anchor=CENTER, relx=.5, rely=.5)
center_btn = Button(bw_frame, text="O", font=(WINDOW_FONT, 10), fg=CENTER_BTN_TEXT, bg=CENTER_BTN_BG, command=center_darkness)
center_btn.place(height = 18, width = 18, anchor=CENTER, rely=.5, relx = .8)

#Left side
slider_frames = []
for i in range(1, 7):
    frame = Frame(left_frame, width=LEFT_FRAME_WIDTH, height=LEFT_FRAME_HEIGHT/6, bg=BG_COLOR)
    frame.pack()
    frame.pack_propagate(0)
    slider_frames.append(frame)

#Build sliders
sliders = []
for slider_num in range(0,6):
    button_frame = Frame(slider_frames[slider_num], height=LEFT_FRAME_HEIGHT/6, width=40, bg=BG_COLOR)
    button_frame.pack(side=RIGHT)
    button_frame.pack_propagate(0)
    color_name_frame = Frame(slider_frames[slider_num], bg=BG_COLOR, width=LEFT_FRAME_WIDTH-button_frame.cget("width"),
                             height=LEFT_FRAME_HEIGHT/18)
    color_name_frame.pack()
    color_name_frame.pack_propagate(0)
    color_name = Label(color_name_frame, bg=BG_COLOR, text=color_label[slider_num], font=(WINDOW_FONT, 15, 'bold'), fg=color_code_font[slider_num])
    color_name.pack(expand=True)
    color_scale = Scale(slider_frames[slider_num], orient=HORIZONTAL, label="Very little", showvalue=0, length=160, from_=1, to=4,
                        sliderlength=SLIDER_LENGTH, command=partial(change_label, slider_num), fg="#ffffff",
                        bg=color_code_font[slider_num], highlightbackground=BG_COLOR, font=(WINDOW_FONT, 10, 'bold'), troughcolor=BG_COLOR)
    color_scale.pack(side=TOP)
    add_btn = Button(button_frame, bg=ADD_BUTTON_COLOR, fg="#000000", text="+", padx=4, pady=1, font=(WINDOW_FONT, 10, 'bold'), command=partial(add_color, slider_num, "add"))
    add_btn.place(anchor=CENTER, relx=.5, y=32, height=18, width=18)
    sub_btn = Button(button_frame, bg=SUB_BUTTON_COLOR, fg="#000000", text="--", padx=6, font=(WINDOW_FONT, 10, 'bold'), command=partial(add_color, slider_num, "sub"))
    sub_btn.place(anchor=CENTER, relx=.5, height=18, width=18, y=slider_frames[slider_num].cget("height")-10)

#Exit Button
exit_btn = Button(window, text="Exit", font=WINDOW_FONT, command=window.destroy, fg=TEXT_COLOR, bg=BG_COLOR)
exit_btn.place(rely=.98, relx=.98, anchor=SE)

'''
CONVERTER TAB
'''

#Title
tab_3.bind('<Button-1>', focus)
title_frame = Frame(tab_3, width=WINDOW_WIDTH, height=TITLE_HEIGHT + 50, bg=BG_COLOR)
title_frame.pack()
title_frame.bind('<Button-1>', focus)
title_frame.pack_propagate(0)
conv_title = Label(title_frame, text="Decimal to Hex Converter", font=(WINDOW_FONT, 24, 'bold'), fg=TITLE_COLOR, bg=BG_COLOR)
conv_title.pack(expand=1)
conv_title.bind('<Button-1>', focus)

#Search Bar
tab_3_frame = Frame(tab_3, height=WINDOW_HEIGHT, width=WINDOW_WIDTH, bg=BG_COLOR)
tab_3_frame.pack()
search = Frame(tab_3, width=WINDOW_WIDTH-100, height=WINDOW_HEIGHT-100, bg=BG_COLOR)
search.place(anchor=CENTER, relx=.5, rely=.65)
search.bind('<Button-1>', focus)
search.pack_propagate(0)
conv_label = Label(search, text="Enter a color in decimal format", font=(WINDOW_FONT, 16), fg=TEXT_COLOR, bg=BG_COLOR)
conv_label.pack(pady=10)
conv_label.bind('<Button-1>', focus)
search_bar_frame = Frame(search, width=WINDOW_WIDTH-100, height=40, bg=BG_COLOR)
search_bar_frame.pack(pady=20)
text_box = Entry(search_bar_frame, validate="key")
text_box['validatecommand'] = (text_box.register(convert_entry_validate), '%S', '%d', '%i')
text_box.pack(side=LEFT, padx=3, pady=3)
add_ghost_text(0)
search.focus()
text_box.bind('<Button-1>', clear_ghost_text)
text_box.bind('<FocusOut>', add_ghost_text)
text_box.bind('<Return>', convert_with_event)
go_btn = Button(search_bar_frame, text="Go", font=WINDOW_FONT, padx=10, fg=TEXT_COLOR, bg=BG_COLOR, command=convert)
go_btn.pack(side=LEFT, padx=10)

#Result and swap button
conv_result = Label(search, text="", font=(WINDOW_FONT, 18), fg=RESULT_COLOR, bg=BG_COLOR)
conv_result.pack(side=TOP, pady=30)
conv_result.bind('<Button-1>', focus)
swap_btn = Button(search, text="Hex to Decimal", padx=10, font=WINDOW_FONT, command=swap, fg=TEXT_COLOR, bg=BG_COLOR)
swap_btn.pack(side=TOP, pady=50)

window.mainloop()