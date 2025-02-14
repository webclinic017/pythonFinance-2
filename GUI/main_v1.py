#! /usr/bin/env python
#
# GUI module generated by PAGE version 4.9
# In conjunction with Tcl version 8.6
#    Aug 18, 2018 08:33:05 PM
import sys

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

import MvcController

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    top = ASTA_Framework(root)
    MvcController.init(root, top)
    root.mainloop()

w = None
def create_ASTA_Framework(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel(root)
    top = ASTA_Framework(w)
    MvcController.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_ASTA_Framework():
    global w
    w.destroy()
    w = None


class ASTA_Framework:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#effbff'  # Closest X11 color: '{alice blue}'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#d9d9d9'  # X11 color: 'gray85'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=
        [('selected', _compcolor), ('active', _ana2color)])

        top.geometry("1500x849+326+30")
        top.title("ASTA_Framework")
        top.configure(background="#eaeaea")
        top.configure(highlightbackground="#d5eaff")
        top.configure(highlightcolor="black")

        self.menubar = Menu(top, font="TkMenuFont", bg='#ff0000', fg=_fgcolor)
        top.configure(menu=self.menubar)

        self.file = Menu(top, tearoff=0)
        self.menubar.add_cascade(menu=self.file,
                                 background="#00ffff",
                                 compound="left",
                                 font=('Purisa', 12, 'normal', 'roman',),
                                 foreground="#000000",
                                 label="File")
        self.file.add_command(
            activebackground="#f4bcb2",
            activeforeground="#000000",
            background="#effbff",
            command=MvcController.save_analysis_parameters,
            font="TkMenuFont",
            foreground="#000000",
            label="Save Analysis Params")
        self.file.add_command(
            activebackground="#f4bcb2",
            activeforeground="#000000",
            background="#effbff",
            command=MvcController.load_analysis_parameters,
            font="TkMenuFont",
            foreground="#000000",
            label="Load Analysis Parameters")
        self.file.add_separator(
            background="#ffff00")
        self.file.add_command(
            activebackground="#f4bcb2",
            activeforeground="#000000",
            background="#effbff",
            command=MvcController.load_backtesting_stocks,
            font="TkMenuFont",
            foreground="#000000",
            label="Load Backtesting Stocks")
        self.file.add_separator(
            background="#effbff")
        self.file.add_command(
            activebackground="#d9d9d9",
            activeforeground="#000000",
            background="#ebebeb",
            command=MvcController.quit,
            font="TkMenuFont",
            foreground="#000000",
            label="Quit")
        self.edit = Menu(top, tearoff=0)
        self.menubar.add_cascade(menu=self.edit,
                                 background="#990000",
                                 font=('Purisa', 12, 'normal', 'roman',),
                                 foreground="#ffff00",
                                 label="Edit")


        self.style.configure('TNotebook.Tab', background=_bgcolor)
        self.style.configure('TNotebook.Tab', foreground=_fgcolor)
        self.style.map('TNotebook.Tab', background=
        [('selected', _compcolor), ('active', _ana2color)])
        self.TNotebook2 = ttk.Notebook(top)
        self.TNotebook2.place(relx=0.0, rely=0.0, relheight=0.75, relwidth=0.99)
        self.TNotebook2.configure(width=1281)
        self.TNotebook2.configure(takefocus="")
        self.TNotebook2_t1_page_res = ttk.Frame(self.TNotebook2)
        self.TNotebook2.add(self.TNotebook2_t1_page_res, padding=3)
        self.TNotebook2.tab(0, text="Run", underline="-1", )
        self.TNotebook2_t2_page_config = ttk.Frame(self.TNotebook2)
        self.TNotebook2.add(self.TNotebook2_t2_page_config, padding=3)
        self.TNotebook2.tab(1, text="Configuration", underline="-1", )
        self.TNotebook2_t2 = ttk.Frame(self.TNotebook2)
        self.TNotebook2.add(self.TNotebook2_t2, padding=3)
        self.TNotebook2.tab(2, text="Backtesting", underline="-1", )

        self.style.configure('Treeview.Heading', font="TkDefaultFont")
        self.Scrolledtreeview1 = ScrolledTreeView(self.TNotebook2_t1_page_res)
        self.Scrolledtreeview1.place(relx=0.01, rely=0.02, relheight=0.85
                                     , relwidth=0.97)
        self.Scrolledtreeview1.heading("#0", text="Tree")
        self.Scrolledtreeview1.heading("#0", anchor="center")
        self.Scrolledtreeview1.column("#0", width="616")
        self.Scrolledtreeview1.column("#0", minwidth="20")
        self.Scrolledtreeview1.column("#0", stretch="1")
        self.Scrolledtreeview1.column("#0", anchor="w")

        self.ButtonRunStrategy = Button(self.TNotebook2_t1_page_res)
        self.ButtonRunStrategy.place(relx=0.1, rely=0.9, height=44, width=142)
        self.ButtonRunStrategy.configure(activebackground="#f4bcb2")
        self.ButtonRunStrategy.configure(activeforeground="#000000")
        self.ButtonRunStrategy.configure(background="#d5eaff")
        self.ButtonRunStrategy.configure(disabledforeground="#a3a3a3")
        self.ButtonRunStrategy.configure(foreground="#000000")
        self.ButtonRunStrategy.configure(highlightbackground="#effbff")
        self.ButtonRunStrategy.configure(highlightcolor="black")
        self.ButtonRunStrategy.configure(pady="0")
        self.ButtonRunStrategy.configure(text='''Run Screening Once''')

        self.ButtonRunStrategyRepetitive = Button(self.TNotebook2_t1_page_res)
        self.ButtonRunStrategyRepetitive.place(relx=0.25, rely=0.9, height=44
                                               , width=160)
        self.ButtonRunStrategyRepetitive.configure(activebackground="#f4bcb2")
        self.ButtonRunStrategyRepetitive.configure(activeforeground="#000000")
        self.ButtonRunStrategyRepetitive.configure(background="greenyellow")
        self.ButtonRunStrategyRepetitive.configure(disabledforeground="#a3a3a3")
        self.ButtonRunStrategyRepetitive.configure(foreground="#000000")
        self.ButtonRunStrategyRepetitive.configure(highlightbackground="#effbff")
        self.ButtonRunStrategyRepetitive.configure(highlightcolor="black")
        self.ButtonRunStrategyRepetitive.configure(pady="0")
        # Text is set in the controller

        self.ButtonStartAutoTrading = Button(self.TNotebook2_t1_page_res)
        self.ButtonStartAutoTrading.place(relx=0.40, rely=0.9, height=44
                                          , width=142)
        self.ButtonStartAutoTrading.configure(activebackground="#f4bcb2")
        self.ButtonStartAutoTrading.configure(activeforeground="#000000")
        self.ButtonStartAutoTrading.configure(background="greenyellow")
        self.ButtonStartAutoTrading.configure(disabledforeground="#a3a3a3")
        self.ButtonStartAutoTrading.configure(foreground="#000000")
        self.ButtonStartAutoTrading.configure(highlightbackground="#effbff")
        self.ButtonStartAutoTrading.configure(highlightcolor="black")
        self.ButtonStartAutoTrading.configure(pady="0")
        # Text is set in the controller

        self.TPanedwindow2 = ttk.Panedwindow(self.TNotebook2_t2_page_config
                                             , orient="horizontal")
        self.TPanedwindow2.place(relx=0.0, rely=0.0, relheight=0.99
                                 , relwidth=0.99)
        self.TPanedwindow2.configure(width=200)
        self.TPanedwindow2_p1_strat_selection = ttk.Labelframe(width=-818
                                                               , text='Strategy Selection')
        self.TPanedwindow2.add(self.TPanedwindow2_p1_strat_selection)
        self.TPanedwindow2_p2_parameters = ttk.Labelframe(text='Parameters')
        self.TPanedwindow2.add(self.TPanedwindow2_p2_parameters)
        self.__funcid0 = self.TPanedwindow2.bind('<Map>', self.__adjust_sash0)

        self.Scrolledlistbox_selectStrategy = ScrolledListBox(self.TPanedwindow2_p1_strat_selection,
                                                              selectmode=MULTIPLE, exportselection=0)
        self.Scrolledlistbox_selectStrategy.place(relx=0.0, rely=0.03
                                                  , relheight=0.95, relwidth=0.96)
        self.Scrolledlistbox_selectStrategy.configure(background="white")
        self.Scrolledlistbox_selectStrategy.configure(disabledforeground="#a3a3a3")
        self.Scrolledlistbox_selectStrategy.configure(font="TkFixedFont")
        self.Scrolledlistbox_selectStrategy.configure(foreground="black")
        self.Scrolledlistbox_selectStrategy.configure(highlightbackground="#d9d9d9")
        self.Scrolledlistbox_selectStrategy.configure(highlightcolor="#effbff")
        self.Scrolledlistbox_selectStrategy.configure(selectbackground="#c4c4c4")
        self.Scrolledlistbox_selectStrategy.configure(selectforeground="black")
        self.Scrolledlistbox_selectStrategy.configure(width=10)

        self.b_open_results_new_wd = Button(self.TNotebook2_t2)
        self.b_open_results_new_wd.place(relx=0.25, rely=0.9, height=44
                                         , width=170)
        self.b_open_results_new_wd.configure(activebackground="#f4bcb2")
        self.b_open_results_new_wd.configure(activeforeground="#000000")
        self.b_open_results_new_wd.configure(background="#d5eaff")
        self.b_open_results_new_wd.configure(disabledforeground="#a3a3a3")
        self.b_open_results_new_wd.configure(foreground="#000000")
        self.b_open_results_new_wd.configure(highlightbackground="#effbff")
        self.b_open_results_new_wd.configure(highlightcolor="black")
        self.b_open_results_new_wd.configure(pady="0")
        self.b_open_results_new_wd.configure(text='''Open Results in new window''')

        self.b_run_backtest = Button(self.TNotebook2_t2)
        self.b_run_backtest.place(relx=0.1, rely=0.9, height=44, width=130)
        self.b_run_backtest.configure(activebackground="#f4bcb2")
        self.b_run_backtest.configure(activeforeground="#000000")
        self.b_run_backtest.configure(background="#d5eaff")
        self.b_run_backtest.configure(disabledforeground="#a3a3a3")
        self.b_run_backtest.configure(foreground="#000000")
        self.b_run_backtest.configure(highlightbackground="#effbff")
        self.b_run_backtest.configure(highlightcolor="black")
        self.b_run_backtest.configure(pady="0")
        self.b_run_backtest.configure(text='''Run backtest''')

        self.TPanedwindow1 = ttk.Panedwindow(self.TNotebook2_t2
                                             , orient="horizontal")
        self.TPanedwindow1.place(relx=0.0, rely=0.0, relheight=0.85
                                 , relwidth=0.98)
        self.TPanedwindow1.configure(width=200)
        self.TPanedwindow1_p1_bt_stocks = ttk.Labelframe(width=-655
                                                         , text='Backtest Configuration')
        self.TPanedwindow1.add(self.TPanedwindow1_p1_bt_stocks)
        self.TPanedwindow1_p2_analysis = ttk.Labelframe(text='Backtrading Result')

        self.TPanedwindow1.add(self.TPanedwindow1_p2_analysis)
        self.__funcid1 = self.TPanedwindow1.bind('<Map>', self.__adjust_sash1)

        self.sl_bt_select_stocks = ScrolledListBox(self.TPanedwindow1_p1_bt_stocks,
                                                   selectmode=MULTIPLE, exportselection=0)
        self.sl_bt_select_stocks.place(relx=0.03, rely=0.08, relheight=0.53
                                       , relwidth=0.95)
        self.sl_bt_select_stocks.configure(background="white")
        self.sl_bt_select_stocks.configure(disabledforeground="#a3a3a3")
        self.sl_bt_select_stocks.configure(font="TkFixedFont")
        self.sl_bt_select_stocks.configure(foreground="black")
        self.sl_bt_select_stocks.configure(highlightbackground="#d9d9d9")
        self.sl_bt_select_stocks.configure(highlightcolor="#effbff")
        self.sl_bt_select_stocks.configure(selectbackground="#c4c4c4")
        self.sl_bt_select_stocks.configure(selectforeground="black")
        self.sl_bt_select_stocks.configure(width=10)

        self.sb_select_analyzers = ScrolledListBox(self.TPanedwindow1_p1_bt_stocks, selectmode=MULTIPLE,
                                                   exportselection=0)
        self.sb_select_analyzers.place(relx=0.03, rely=0.66, relheight=0.32
                                       , relwidth=0.95)
        self.sb_select_analyzers.configure(background="white")
        self.sb_select_analyzers.configure(disabledforeground="#a3a3a3")
        self.sb_select_analyzers.configure(font="TkFixedFont")
        self.sb_select_analyzers.configure(foreground="black")
        self.sb_select_analyzers.configure(highlightbackground="#d9d9d9")
        self.sb_select_analyzers.configure(highlightcolor="#effbff")
        self.sb_select_analyzers.configure(selectbackground="#c4c4c4")
        self.sb_select_analyzers.configure(selectforeground="black")
        self.sb_select_analyzers.configure(width=10)

        self.Label1 = Label(self.TPanedwindow1_p1_bt_stocks)
        self.Label1.place(relx=0.03, rely=0.62, height=21, width=102)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#effbff")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Analyzer Selection''')

        self.Label2 = Label(self.TPanedwindow1_p1_bt_stocks)
        self.Label2.place(relx=0.03, rely=0.03, height=21, width=113)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background="#effbff")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''Stock Data Selection''')

        self.Scrolledtext_analyzer_results = ScrolledText(self.TPanedwindow1_p2_analysis)
        self.Scrolledtext_analyzer_results.place(relx=0.01, rely=0.04
                                                 , relheight=0.93, relwidth=0.97)
        self.Scrolledtext_analyzer_results.configure(background="white")
        self.Scrolledtext_analyzer_results.configure(font="TkTextFont")
        self.Scrolledtext_analyzer_results.configure(foreground="black")
        self.Scrolledtext_analyzer_results.configure(highlightbackground="#effbff")
        self.Scrolledtext_analyzer_results.configure(highlightcolor="black")
        self.Scrolledtext_analyzer_results.configure(insertbackground="black")
        self.Scrolledtext_analyzer_results.configure(insertborderwidth="3")
        self.Scrolledtext_analyzer_results.configure(selectbackground="#c4c4c4")
        self.Scrolledtext_analyzer_results.configure(selectforeground="black")
        self.Scrolledtext_analyzer_results.configure(width=10)
        self.Scrolledtext_analyzer_results.configure(wrap=NONE)

        self.Labelframe2 = LabelFrame(top)
        self.Labelframe2.place(relx=0.01, rely=0.76, relheight=0.22
                               , relwidth=0.98)
        self.Labelframe2.configure(relief=GROOVE)
        self.Labelframe2.configure(foreground="black")
        self.Labelframe2.configure(text='''Logging''')
        self.Labelframe2.configure(background="#effbff")
        self.Labelframe2.configure(highlightbackground="#d9d9d9")
        self.Labelframe2.configure(highlightcolor="black")
        self.Labelframe2.configure(width=150)

    def __adjust_sash0(self, event):
        paned = event.widget
        pos = [246, ]
        i = 0
        for sash in pos:
            paned.sashpos(i, sash)
            i += 1
        paned.unbind('<map>', self.__funcid0)
        del self.__funcid0

    def __adjust_sash1(self, event):
        paned = event.widget
        pos = [396, ]
        i = 0
        for sash in pos:
            paned.sashpos(i, sash)
            i += 1
        paned.unbind('<map>', self.__funcid1)
        del self.__funcid1


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

        # self.configure(yscrollcommand=_autoscroll(vsb),
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

class ScrolledTreeView(AutoScroll, ttk.Treeview):
    '''A standard ttk Treeview widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)


if __name__ == '__main__':
    vp_start_gui()
