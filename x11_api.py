import ctypes


x11 = ctypes.CDLL('libX11.so')


x11.XOpenDisplay.argtypes = (ctypes.c_void_p, )
x11.XOpenDisplay.restype = ctypes.c_void_p
x11.XRootWindow.argtypes = (ctypes.c_void_p, ctypes.c_int)
x11.XRootWindow.restype = ctypes.c_void_p
x11.XStoreName.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)
x11.XStoreName.restype = None
x11.XCloseDisplay.argtypes = (ctypes.c_void_p, )
x11.XCloseDisplay.restype = None


dpy = None
root = None


def init() -> None:
    global dpy, root
    dpy = x11.XOpenDisplay(None)
    assert dpy
    root = x11.XRootWindow(dpy, 0)
    assert root


def set_status(text: str) -> None:
    x11.XStoreName(dpy, root, text.encode('utf-8'))


def destroy() -> None:
    x11.XCloseDisplay(dpy)
