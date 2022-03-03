'a template'
import logging
import sys
import tkinter.filedialog
import tkinter.messagebox
from subprocess import run
from tkinter import *
from tkinter.constants import BOTH, BOTTOM, END, INSERT, LEFT
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import *
from urllib.request import urlopen
from zipfile import ZipFile
from pyperclip import copy, paste

top = Tk()
top.title('NotePad+')
notebook = Notebook(top)
top.geometry('800x600')
logging.basicConfig(filename='log.log', level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s %(message)s')


def zipextract(path):
    zippath = ZipFile(path)
    zippath.extractall(r'C:\Users\Public\python')
    zippath.close()


try:
    with urlopen('https://codeload.github.com/Astr-Code/python_zip/zip/refs/heads/main') as r:
        open(r'C:\Users\Public\python.zip', 'xb').write(r.read())
        zipextract(r'C:\Users\Public\python.zip')
    zipextract(r'C:\Users\Public\python\python_zip-main\py.zip')
except FileExistsError:
    pass


try:
    with open(r'C:\Users\Public\python\change.py', 'x', encoding='utf-8') as f:
        f.write('''import re, fileinput

field_pat = re.compile(r'\[(.+?)\]')
scope = {}


def replacement(match):
    code = match.group(1)
    try:
        return str(eval(code, scope))
    except SyntaxError:
        exec(code, scope)
        return ''


lines = []
for line in fileinput.input():
    lines.append(line)
text = ''.join(lines)
txt = field_pat.sub(replacement, text)
f = open(r'D:\A.txt', 'w')
f.write(txt)
f.close()''')
except FileExistsError:
    pass


class Events:
    """all the events"""

    def __init__(self):
        self.filename = self.init_path = r'C:\Users\Public\'\
            Documents\unknown.txt'

    def load(self, events=None):
        '''open a file'''
        try:
            self.filename = tkinter.filedialog.askopenfilename()
            with open(self.filename, encoding='utf-8') as file:
                tab1 = Frame(top)
                self.contents = ScrolledText(tab1)
                self.contents.insert(INSERT, file.read())
                self.contents.pack(side=BOTTOM, expand=True, fill=BOTH)
                notebook.add(tab1, text=self.filename)
                notebook.select(tab1)
                logging.info('opened a file,call:"%s"' % self.filename)
                top.title('NotePad+ : %s' % self.filename)
        except FileNotFoundError:
            pass

    def save(self, events=None):
        '''save a file'''
        file = notebook.tab(notebook.select())
        try:
            if file != self.init_path:
                with open(file.get('text'), 'w', encoding='utf-8') as f:
                    f.write(self.contents.get('1.0', END))
                    logging.info(
                        'saved a file,call:"{}"'.format(self.filename))
            else:
                self.save_as()
        except FileNotFoundError:
            pass

    def save_as(self, events=None):
        '''save as a file'''
        with tkinter.filedialog.asksaveasfile(title='另存为') as f:
            top.title('NotePad+ : {}'.format(f.name))
            f.write(self.contents.get('1.0', END))
            logging.info('saved as a file,call:"{}"'.format(self.filename))

    def new(self, events=None):
        '''create a file'''
        tab1 = Frame(top)
        self.contents = ScrolledText(tab1)
        self.contents.pack(side=BOTTOM, expand=True, fill=BOTH)
        notebook.add(tab1, text='New Tab')
        notebook.select(tab1)
        logging.info('create a file')
        top.title('Unknown')

    def quit_tab(self, events=None):
        """quit a tab"""
        notebook.forget(notebook.select())
        logging.info('quit a tab')

    def import_file(self, events=None):
        '''import a python file'''
        file = notebook.tab(notebook.select())
        self.filename_name = tkinter.filedialog.askopenfilename()
        cmd = r'C:\Users\Public\python\py\python.exe', r'C:\Users\Public\python\change.py', self.filename_name, file.get('text')
        changes = run(cmd)
        self._after_change()

    def change(self, events=None):
        """change a file"""
        file = notebook.tab(notebook.select())
        cmd = r'C:\Users\Public\python\py\python.exe', r'C:\Users\Public\python\change.py', file.get('text')
        changes = run(cmd)
        self._after_change()

    def _after_change(self, events=None):
        """after change a file"""
        file = notebook.tab(notebook.select())
        data = open(r'D:\a.txt', 'r').read()
        open(file.get('text'), 'w', encoding='utf-8').write(data.strip())
        with open(self.filename, encoding='utf-8') as file:
            self.contents.delete('1.0', END)
            self.contents.insert(INSERT, file.read())
            top.title('NotePad+ : %s' % self.filename)
        logging.info('change a file')

    def copy_text(self, events=None):
        """copy text"""
        text = self.contents.get('sel.first', 'sel.last')
        copy(text)

    def paste_text(self, events=None):
        """paste text"""
        text = paste()
        self.contents.insert(INSERT, text)

    def cut_text(self, events=None):
        """cut text"""
        self.copy_text(events)
        self.contents.delete('sel.first', 'sel.last')


events = Events()
logging.info('open app')
events.new()
notebook.pack(side=LEFT, expand=True, fill=BOTH)
menubar = Menu(top)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='新建', command=events.new, accelerator='Ctrl+N')
filemenu.add_command(label='打开', command=events.load, accelerator='Ctrl+O')
filemenu.add_command(label='保存', command=events.save, accelerator='Ctrl+S')
filemenu.add_command(label='另存为', command=events.save_as,
                     accelerator='Ctrl+Shift+S')
filemenu.add_separator()
filemenu.add_command(
    label='退出tab', command=events.quit_tab, accelerator='Ctrl+Q')
filemenu.add_command(label='退出', command=top.quit)
menubar.add_cascade(label='文件', menu=filemenu)
top.bind("<Control-n>", events.new)
top.bind("<Control-o>", events.load)
top.bind("<Control-s>", events.save)
top.bind("<Control-Shift-s>", events.save_as)
top.bind("<Control-q>", events.quit_tab)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label='复制', command=events.copy_text,
                     accelerator='Ctrl+C')
editmenu.add_command(label='粘贴', command=events.paste_text,
                     accelerator='Ctrl+V')
editmenu.add_command(
    label='剪切', command=events.cut_text, accelerator='Ctrl+X')
menubar.add_cascade(label='编辑', menu=editmenu)

importmenu = Menu(menubar, tearoff=0)
importmenu.add_command(
    label='导入文件', command=events.import_file, accelerator='Ctrl+I')
importmenu.add_command(
    label='运行', command=events.change, accelerator='Ctrl+R')
menubar.add_cascade(label='导入', menu=importmenu)
top.bind("<Control-i>", events.import_file)
top.bind("<Control-r>", events.change)
top.config(menu=menubar)

top.mainloop()
logging.info('close app')
