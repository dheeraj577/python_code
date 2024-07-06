from tkinter import *

input_text = ""
time_count = None


def time_calculate(event):
    global time_count, input_text

    if time_count is not None:
        window.after_cancel(time_count)

    if event.keysym == "BackSpace":
        input_text = input_text[0: len(input_text) - 1]

    elif event.char:
        input_text += event.char
        time_count = window.after(5000, reset_app)

    return


def reset_app():
    global time_count, input_text
    typing_area.delete('1.0', 'end')
    input_text = ""
    time_count = None
    return


def save_input():
    global input_text
    if input_text == "":
        return
    try:
        f = open('saveOutput.txt', 'r')
    except FileNotFoundError:
        f = open('saveOutput.txt', 'w')
        f.write(input_text)
        input_text = ""
        return
    else:
        cont = f.read()
        if cont == "":
            text_to_write = input_text
        else:
            text_to_write = f'\n{input_text}'

        with open('saveOutput.txt', 'a') as f:
            f.write(text_to_write)
            input_text = ""
    finally:
        return

BORDER_COLOR = "#005C78"
FG_COLOR = '#E88D67'
BG_COLOR = "#006989"

FONT_ST1 = ('Verdana', 14, 'bold')
FONT_ST2 = ('Verdana', 12, 'italic')
HEADING_FONT = ('Arial', 24, 'normal')



heading = "TYPE WITH MAGICAL INK"
instruction = "If you don't press any key for 5 seconds, the text you have written will disappear"

window = Tk()
window.title('Disappearing Text Writing App')
window.config(bg=BG_COLOR, padx=20, pady=10)

heading = Label(text=heading, font=HEADING_FONT, bg=BG_COLOR, fg=FG_COLOR, padx=10, pady=10)
instruction = Label(text=instruction, font=FONT_ST2,
                    fg=FG_COLOR, bg=BG_COLOR, pady=10)
typing_area = Text(font=FONT_ST1, bg=BG_COLOR, fg=FG_COLOR, width=100, height=15, wrap='w',
                   highlightcolor=BORDER_COLOR, highlightthickness=4, highlightbackground=BORDER_COLOR,
                   padx=5, pady=5)
typing_area.bind('<KeyPress>', time_calculate)
reset_btn = Button(text='Reset', fg=FG_COLOR, bg=BG_COLOR, font=FONT_ST1,
                   highlightbackground=FG_COLOR, highlightcolor=FG_COLOR, highlightthickness=0, border=3,
                   command=reset_app, width=50)

save_btn = Button(text='Save', fg=FG_COLOR, bg=BG_COLOR, font=FONT_ST1,
                   highlightbackground=FG_COLOR, highlightcolor=FG_COLOR, highlightthickness=0, border=3,
                   command=save_input, width=50)

heading.grid(row=0, column=0, columnspan=3)
instruction.grid(row=2, column=0, columnspan=3)
typing_area.grid(row=3, column=0, columnspan=3)
reset_btn.grid(row=4, column=0)
save_btn.grid(row=4, column=2)


window.mainloop()