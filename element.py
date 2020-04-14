from pywinauto import Desktop, Application
from _ctypes import COMError


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
    for ele in Desktop(backend='uia').windows():
        control_type = ele.element_info.control_type
        title = ele.element_info.name
        class_name = ele.element_info.class_name
        content = u"{} {}\n".format('[ title={}, class_name={}, control_type={} ]'.format(title, class_name, control_type),
                                    ' [ handle=' + str(ele.handle) + ' ]')
        output += content
    return output


def get_control_by_handle(handle):
    return Desktop(backend='uia').window(handle=handle)


def get_control_by_kw(root, **kwargs):
    return root.window(**kwargs)
