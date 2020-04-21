import tkinter as tk
from tkinter import *
import pprint

element_properties = ['automation_id', 'class_name', 'control_type', 'enabled', 'framework_id', 'handle', 'name',
                      'process_id', 'rich_text', 'visible']


def debug_window(root, get_element):
    def reset_text(text, clear=True):
        debug_text.delete('1.0', END)
        debug_text.insert(INSERT, text)

    def print_element_info():
        result = {}
        for prop in element_properties:
            result.update({prop: getattr(element.element_info, prop)})
        result.update({'object_type': type(element)})
        result.update({'wrappered_type': type(element.wrapper_object())})
        reset_text(pprint.pformat(result))

    def run_command():
        runline = input_box.get()
        arg = None
        if runline.startswith('.'):
            runline = runline.lstrip('.')
        if runline.find('(') != -1:
            method = runline.split('(')[0]
            arg = runline.split('(')[-1].rstrip(')')
            arg = arg.strip("'")
            runline = method
        try:
            func = getattr(element.wrapper_object(), runline)
            if arg is not None and arg != '':
                ret = func(arg)
            else:
                ret = func()
        except Exception as e:
            ret = type(e).__name__ + ": " + str(e)
        reset_text(ret)

    debug_win = tk.Toplevel(root)
    element = get_element()
    control_panel = tk.Frame(debug_win)
    print_btn = tk.Button(control_panel, text="Print", command=print_element_info)
    run_btn = tk.Button(control_panel, text="Run", command=run_command)
    input_box = tk.Entry(control_panel, width=60)
    debug_text = tk.Text(debug_win)
    print_btn.pack(side=LEFT)
    run_btn.pack(side=LEFT)
    input_box.pack(side=LEFT)
    control_panel.pack(fill=BOTH)
    debug_text.pack()
