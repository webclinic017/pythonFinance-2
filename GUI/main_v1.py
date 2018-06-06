#! /usr/bin/env python
#
# GUI module generated by PAGE version 4.9
# In conjunction with Tcl version 8.6
#    Jun 05, 2018 04:47:04 PM
import sys

import os

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

import main_v1_support
global ROOT_DIR
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
global global_filepath
global_filepath = ROOT_DIR + '\\DataFiles\\'
#TODO vom dataprovider lesen und dann zuweisen (irgendeine aktie abfragen)
global glob_stock_data_labels_dict
glob_stock_data_labels_dict = {'High': 'high', 'Low':'low', 'Open':'open',
                               'Close':'close', 'Volume':'volume', 'Date': 'date'}


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    top = Framework (root)
    main_v1_support.init(root, top)
    root.mainloop()

w = None
def create_Framework(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    top = Framework (w)
    main_v1_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Framework():
    global w
    w.destroy()
    w = None


class Framework:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = 'wheat'  # X11 color: #f5deb3
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("1200x874+32+0")
        top.title("Framework")
        top.configure(background="#eaeaea")
        top.configure(highlightbackground="wheat")
        top.configure(highlightcolor="black")



        self.menubar = Menu(top,font="TkMenuFont",bg='#ff0000',fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.file = Menu(top,tearoff=0)
        self.menubar.add_cascade(menu=self.file,
                background="#00ffff",
                compound="left",
                font=('Purisa',12,'normal','roman',),
                foreground="#000000",
                label="File")
        self.file.add_command(
                activebackground="#d9d9d9",
                activeforeground="#000000",
                background="#ffff00",
                command=main_v1_support.save,
                font="TkMenuFont",
                foreground="#000000",
                label="Save")
        self.file.add_command(
                activebackground="#f4bcb2",
                activeforeground="#000000",
                background="wheat",
                command=main_v1_support.load_params,
                font="TkMenuFont",
                foreground="#000000",
                label="Load Parameters")
        self.file.add_separator(
                background="#ffff00")
        self.file.add_command(
                activebackground="#d9d9d9",
                activeforeground="#000000",
                background="#ebebeb",
                command=main_v1_support.quit,
                compound="top",
                font="TkMenuFont",
                foreground="#000000",
                label="Quit")
        self.edit = Menu(top,tearoff=0)
        self.menubar.add_cascade(menu=self.edit,
                background="#990000",
                font=('Purisa',12,'normal','roman',),
                foreground="#ffff00",
                label="Edit")


        self.Strategy = Frame(top)
        self.Strategy.place(relx=0.01, rely=0.01, relheight=0.39, relwidth=0.99)
        self.Strategy.configure(relief=GROOVE)
        self.Strategy.configure(borderwidth="2")
        self.Strategy.configure(relief=GROOVE)
        self.Strategy.configure(background="#c0c0c0")
        self.Strategy.configure(highlightbackground="#d9d9d9")
        self.Strategy.configure(highlightcolor="black")
        self.Strategy.configure(width=1185)

        self.Scrolledlistbox_selectStrategy = ScrolledListBox(self.Strategy)
        self.Scrolledlistbox_selectStrategy.place(relx=0.01, rely=0.03
                , relheight=0.45, relwidth=0.98)
        self.Scrolledlistbox_selectStrategy.configure(background="white")
        self.Scrolledlistbox_selectStrategy.configure(disabledforeground="#a3a3a3")
        self.Scrolledlistbox_selectStrategy.configure(font="TkFixedFont")
        self.Scrolledlistbox_selectStrategy.configure(foreground="black")
        self.Scrolledlistbox_selectStrategy.configure(highlightbackground="#d9d9d9")
        self.Scrolledlistbox_selectStrategy.configure(highlightcolor="wheat")
        self.Scrolledlistbox_selectStrategy.configure(selectbackground="#c4c4c4")
        self.Scrolledlistbox_selectStrategy.configure(selectforeground="black")
        self.Scrolledlistbox_selectStrategy.configure(width=10)

        self.Frame2 = Frame(top)
        self.Frame2.place(relx=0.01, rely=0.78, relheight=0.1, relwidth=0.98)
        self.Frame2.configure(relief=GROOVE)
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief=GROOVE)
        self.Frame2.configure(background="#ebebeb")
        self.Frame2.configure(highlightbackground="#d9d9d9")
        self.Frame2.configure(highlightcolor="black")
        self.Frame2.configure(width=1175)

        self.ButtonRunStrategy = Button(self.Frame2)
        self.ButtonRunStrategy.place(relx=0.02, rely=0.24, height=44, width=142)
        self.ButtonRunStrategy.configure(activebackground="#f4bcb2")
        self.ButtonRunStrategy.configure(activeforeground="#000000")
        self.ButtonRunStrategy.configure(background="wheat")
        self.ButtonRunStrategy.configure(disabledforeground="#a3a3a3")
        self.ButtonRunStrategy.configure(foreground="#000000")
        self.ButtonRunStrategy.configure(highlightbackground="wheat")
        self.ButtonRunStrategy.configure(highlightcolor="black")
        self.ButtonRunStrategy.configure(pady="0")
        self.ButtonRunStrategy.configure(text='''Run Screening Once''')

        self.ButtonRunStrategyRepetitive = Button(self.Frame2)
        self.ButtonRunStrategyRepetitive.place(relx=0.16, rely=0.24, height=44
                , width=137)
        self.ButtonRunStrategyRepetitive.configure(activebackground="#f4bcb2")
        self.ButtonRunStrategyRepetitive.configure(activeforeground="#000000")
        self.ButtonRunStrategyRepetitive.configure(background="wheat")
        self.ButtonRunStrategyRepetitive.configure(disabledforeground="#a3a3a3")
        self.ButtonRunStrategyRepetitive.configure(foreground="#000000")
        self.ButtonRunStrategyRepetitive.configure(highlightbackground="wheat")
        self.ButtonRunStrategyRepetitive.configure(highlightcolor="black")
        self.ButtonRunStrategyRepetitive.configure(pady="0")
        self.ButtonRunStrategyRepetitive.configure(text='''Run Strategy Repetitive''')

        self.Scrolledtext_params = ScrolledText(top)
        self.Scrolledtext_params.place(relx=0.02, rely=0.21, relheight=0.18
                , relwidth=0.97)
        self.Scrolledtext_params.configure(background="white")
        self.Scrolledtext_params.configure(font="TkTextFont")
        self.Scrolledtext_params.configure(foreground="black")
        self.Scrolledtext_params.configure(highlightbackground="wheat")
        self.Scrolledtext_params.configure(highlightcolor="black")
        self.Scrolledtext_params.configure(insertbackground="black")
        self.Scrolledtext_params.configure(insertborderwidth="3")
        self.Scrolledtext_params.configure(selectbackground="#c4c4c4")
        self.Scrolledtext_params.configure(selectforeground="black")
        self.Scrolledtext_params.configure(width=10)
        self.Scrolledtext_params.configure(wrap=NONE)

        self.Labelframe1 = LabelFrame(top)
        self.Labelframe1.place(relx=0.01, rely=0.45, relheight=0.33
                , relwidth=0.98)
        self.Labelframe1.configure(relief=GROOVE)
        self.Labelframe1.configure(foreground="black")
        self.Labelframe1.configure(text='''Results''')
        self.Labelframe1.configure(background="#dadada")
        self.Labelframe1.configure(highlightbackground="#d9d9d9")
        self.Labelframe1.configure(highlightcolor="black")
        self.Labelframe1.configure(width=1180)

        self.Scrolledtext_Results = ScrolledText(self.Labelframe1)
        self.Scrolledtext_Results.place(relx=0.01, rely=0.11, relheight=0.85
                , relwidth=0.98)
        self.Scrolledtext_Results.configure(background="white")
        self.Scrolledtext_Results.configure(font="TkTextFont")
        self.Scrolledtext_Results.configure(foreground="black")
        self.Scrolledtext_Results.configure(highlightbackground="wheat")
        self.Scrolledtext_Results.configure(highlightcolor="black")
        self.Scrolledtext_Results.configure(insertbackground="black")
        self.Scrolledtext_Results.configure(insertborderwidth="3")
        self.Scrolledtext_Results.configure(selectbackground="#c4c4c4")
        self.Scrolledtext_Results.configure(selectforeground="black")
        self.Scrolledtext_Results.configure(width=10)
        self.Scrolledtext_Results.configure(wrap=NONE)

        self.Labelframe2 = LabelFrame(top)
        self.Labelframe2.place(relx=0.01, rely=0.89, relheight=0.12
                , relwidth=0.98)
        self.Labelframe2.configure(relief=GROOVE)
        self.Labelframe2.configure(foreground="black")
        self.Labelframe2.configure(text='''Logging''')
        self.Labelframe2.configure(background="wheat")
        self.Labelframe2.configure(highlightbackground="#d9d9d9")
        self.Labelframe2.configure(highlightcolor="black")
        self.Labelframe2.configure(width=1180)

        self.Scrolledtext_log = ScrolledText(self.Labelframe2)
        self.Scrolledtext_log.place(relx=0.01, rely=0.19, relheight=0.68
                , relwidth=0.98)
        self.Scrolledtext_log.configure(background="white")
        self.Scrolledtext_log.configure(font="TkTextFont")
        self.Scrolledtext_log.configure(foreground="black")
        self.Scrolledtext_log.configure(highlightbackground="wheat")
        self.Scrolledtext_log.configure(highlightcolor="black")
        self.Scrolledtext_log.configure(insertbackground="black")
        self.Scrolledtext_log.configure(insertborderwidth="3")
        self.Scrolledtext_log.configure(selectbackground="#c4c4c4")
        self.Scrolledtext_log.configure(selectforeground="black")
        self.Scrolledtext_log.configure(width=10)
        self.Scrolledtext_log.configure(wrap=NONE)





# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        #self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = Pack.__dict__.keys() | Grid.__dict__.keys() \
                  | Place.__dict__.keys()
        else:
            methods = Pack.__dict__.keys() + Grid.__dict__.keys() \
                  + Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        return func(cls, container, **kw)
    return wrapped

class ScrolledText(AutoScroll, Text):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

class ScrolledListBox(AutoScroll, Listbox):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

if __name__ == '__main__':
    vp_start_gui()



