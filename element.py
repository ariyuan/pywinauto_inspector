from pywinauto import Desktop, Application
from _ctypes import COMError

# get app list from desktop, it returns a list of UIAWrapper with handle number
desktop = Desktop(backend='uia').windows()


def print_controls(control):
    print_control_func = getattr(control, 'print_control_identifiers')
    try:
        print_control_func()
    except COMError:
        print('Com error occurred')


def highlight(control):
    try:
        control.wrapper_object().set_focus()
        control.wrapper_object().draw_outline()
    except COMError:
        print('Com error occurred')


def get_window_handle_list():
    output = ""
    for ele in desktop:
        content = u"{} {}\n".format(repr(ele), str(ele.handle))
        output += content
    return output


def get_control_by_handle(handle):
    return Desktop(backend='uia').window(handle=handle)


def get_control_by_kw(root, **kwargs):
    return root.window(**kwargs)

# # foreach with the handle number, eg excel handle = 396126
# app = Desktop(backend='uia').window(handle=396126)
# # above is a WindowSpecification object, which can be called with print_control_identifiers
# worksheet_config = app.window(best_match='Worksheet ConfigurationCustom')
# print_controls(worksheet_config)
