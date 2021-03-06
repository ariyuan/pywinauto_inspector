import tkinter as tk
from tkinter import *
from tkinter import ttk
from contextlib import redirect_stdout
import io
import element
import definition
import utility
from tkinter import messagebox
from pywinauto.findwindows import *
import gui_debug


def main():
    def reset_text(text, clear=True):
        text_showbox.delete('1.0', END)
        text_showbox.insert(INSERT, text)

    def show():
        """
        show the element print_control_identifier information
        :return:
        """
        # get the value from input box
        input_txt = input_box.get()
        # call print_control_identifier and get the output result
        f = io.StringIO()
        try:
            if input_txt.find('handle') != -1:
                definition.app = element.get_control_by_handle(int(input_txt.split('=')[-1]))
                element_to_print = definition.app
            else:
                element_to_print = element.get_control_by_kw(definition.app,
                                                             **utility.convert_string_to_dict(input_txt))
            definition.current_control = element_to_print
            current_ele.set(
                'Current: {} {}'.format(element_to_print.element_info.name, element_to_print.element_info.control_type))
            with redirect_stdout(f):
                element.print_controls(element_to_print)
        except (AttributeError, TypeError, NameError, ElementNotFoundError) as e:
            messagebox.showinfo("Error", type(e).__name__ + ": " + str(e))
        # print it to text box
        txt = f.getvalue()
        reset_text(txt)
        # save the input to combobox
        if len(input_box['values']) > 20:  # max item is 20, else pop the oldest one
            _list = list(input_box['values'])
            _list.pop(0)
            input_box['values'] = tuple(_list)
        if input_txt not in input_box['values']:
            input_box['values'] = input_box['values'] + (input_txt,)

    def init():
        process_handles = element.get_window_handle_list()
        reset_text(process_handles)

    def highlight():
        input_txt = input_box.get()
        try:
            element_to_highlight = element.get_control_by_kw(definition.app,
                                                             **utility.convert_string_to_dict(input_txt))
            element.highlight(element_to_highlight)
        except Exception as e:
            messagebox.showinfo("Error", type(e).__name__ + ": " + str(e))

    window = tk.Tk()
    window.title("pywinauto inspector")
    window.geometry('900x600')

    # main layout
    Grid.rowconfigure(window, 0)
    Grid.rowconfigure(window, 1, weight=10)
    Grid.columnconfigure(window, 0, weight=1)
    control_panel = tk.Frame(window)
    text_area = tk.Frame(window)
    control_panel.grid(row=0, column=0, sticky="w")
    text_area.grid(row=1, column=0, sticky="nsew")

    # text area layout
    text_area.columnconfigure(0, weight=10)
    text_area.rowconfigure(0, weight=10)
    text_showbox = tk.Text(text_area)
    scrollb = tk.Scrollbar(text_area, command=text_showbox.yview)
    text_showbox['yscrollcommand'] = scrollb.set
    text_showbox.grid(row=0, column=0, sticky='nsew')
    scrollb.grid(row=0, column=1, sticky='nsew')

    # control panel
    input_box = ttk.Combobox(control_panel, width=60)
    input_box['values'] = ['']
    btn_show = tk.Button(control_panel, text="Print", command=show)
    btn_load = tk.Button(control_panel, text="Highlight", command=highlight)
    btn_root = tk.Button(control_panel, text="Root", command=init)
    current_ele = StringVar()
    label_current_element = tk.Label(control_panel, textvariable=current_ele)
    label_current_element.bind("<Button-1>", lambda event, root=window,
                                                    get_element=definition.get_current_control: gui_debug.debug_window(
        root, get_element))
    btn_show.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    btn_load.grid(row=0, column=2, sticky="ew", padx=5)
    btn_root.grid(row=0, column=3, sticky="ew", padx=5)
    input_box.grid(row=0, column=0, sticky="nsew")
    label_current_element.grid(row=0, column=4, sticky="ew", padx=5)

    init()

    window.mainloop()
