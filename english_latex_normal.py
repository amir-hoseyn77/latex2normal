import pyperclip
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.scrolledtext import ScrolledText
import re
from latex_process import *
########
# GUI commands and functions
def push_only_text(TextBox, text_str):
    """push `text_str` into whole `TextBox` i.e. delete 
    `TextBox` context and paste `text_str` to `TextBox`"""
    TextBox.delete('1.0', tk.END)
    TextBox.insert('1.0', text_str)

def Paste_cmd():
    """Paste from `clipboard` to `text_in`"""
    data = pyperclip.paste()
    push_only_text(Inp_elems['input_text'], data)

def Copy_cmd():
    """Copy from `text_out`(processed) to `clipboard`"""
    data = Inp_elems['output_text'].get('1.0',end_text)
    pyperclip.copy(data)

def Process_cmd(data=None):
    """Process `text_in` and push to `text_out` and `clipboard`"""
    if data == None:
        data = Inp_elems['input_text'].get('1.0',end_text)
    opt_txt = Inp_elems['Option_combo'].get()
    data_out = switch_dict[opt_txt](data)
    push_only_text(Inp_elems['output_text'], data_out)
    Copy_cmd()  # Optional: You can remove it
    return data_out

def Recursive_cmd():
    """Recusive command: process and paste output into `text_in` for sequential Options"""
    data = Process_cmd()
    push_only_text(Inp_elems['input_text'], data)

def Allin1_cmd():
    """Paste, process and copy text from/to clipboard"""
    data = pyperclip.paste()
    push_only_text(Inp_elems['input_text'], data)
    data_out = Process_cmd(data)
    pyperclip.copy(data_out)

# Create GUI elements
def create_GUI():
    window = tk.Tk()
    #
    Text_frame = tk.Frame(window)
    Button_frame = tk.Frame(window)
    Option_frame = tk.Frame(window)
    Text_frame.grid(row=0, column=0)
    Button_frame.grid(row=0, column=1)
    Option_frame.grid(row=0, column=2)
    
    # Text fields
    ## Definition
    Label_in = tk.Label(Text_frame, text=u'متن ورودی', font=('XB Niloofar', '12'))
    text_in = ScrolledText(Text_frame, width=80, height=10, font=('Courier New', '12'))
    Label_out = tk.Label(Text_frame, text=u'متن خروجی', font=('XB Niloofar', '12'))
    text_out = ScrolledText(Text_frame, width=80, height=10, font=('Courier New', '12'))
    ## Arranging
    Label_in.pack(); text_in.pack()
    Label_out.pack(); text_out.pack()

    # Buttons
    ## Definition
    Paste_key = tk.Button(Button_frame, text='Paste', height=4, width=30, command=Paste_cmd)
    Process_key = tk.Button(Button_frame, text='Process->Copy', height=4, width=30, command=Process_cmd)
    Copy_key = tk.Button(Button_frame, text='Copy', height=4, width=30, command=Copy_cmd)
    Recursive_key = tk.Button(Button_frame, text='Process->Paste', height=4, width=30, command=Recursive_cmd)
    ## Arranging
    Paste_key.grid(row=0, column=0, pady=20)
    Process_key.grid(row=1, column=0, pady=20)
    Copy_key.grid(row=2, column=0, pady=20)
    Recursive_key.grid(row=3, column=0, pady=20)
    
    # Options and All in 1
    n = tk.StringVar()
    ## Definition
    Allin1_key = tk.Button(Option_frame, text='All in 1', height=4, width=30, command=Allin1_cmd)
    Option_label = tk.Label(Option_frame, text='Choose Option')
    Option_combo = ttk.Combobox(Option_frame, width=40, state="readonly", textvariable=n)
    Option_combo['values'] = ('latex-->normal','normal-->latex',
    'change numbers(farsi2Eng)','change numbers(Eng2farsi)')
    Option_combo.current(1)
    ## Arranging
    Allin1_key.grid(row=0, column=0, pady=30)
    Option_label.grid(row=1, column=0,)
    Option_combo.grid(row=2, column=0)
    # Globalize Texts for enablong modification
    global Inp_elems
    Inp_elems = {'input_text':text_in, 'output_text':text_out, 'Option_combo':Option_combo}

    window.mainloop()


if __name__ == '__main__':
    end_text = 'end-1c'  # to remove `\n` from output of Text.get()
    switch_dict = {'latex-->normal':latex2norm, 'normal-->latex':norm2latex,
    'change numbers(farsi2Eng)':number_fa2en,'change numbers(Eng2farsi)':number_en2fa}  # available options
    create_GUI()