'a template'
from tkinter import *
from tkinter.constants import BOTH, BOTTOM, END, INSERT, LEFT
from tkinter.scrolledtext import ScrolledText
import tkinter.messagebox
import tkinter.filedialog
from tkinter.ttk import *
import logging
import sys
from urllib.request import urlretrieve, urlopen
from zipfile import ZipFile
from subprocess import run


top = Tk()
top.title('NotePad+')
contents = ScrolledText()
contents.pack(side=BOTTOM, expand=True, fill=BOTH)

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

field_pat = re.compile(r'\[(.*?)\]')
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

    def load(self, events = None):
        '''open a file'''
        try:
            self.filename = tkinter.filedialog.askopenfilename()
            with open(self.filename, encoding='utf-8') as file:
                contents.delete('1.0', END)
                contents.insert(INSERT, file.read())
                logging.info('opened a file,call:"%s"' % self.filename)
                top.title('NotePad+ : %s' % self.filename)
        except FileNotFoundError:
            pass

    def save(self, events = None):
        '''save a file'''
        try:
            if self.filename != self.init_path:
                with open(self.filename, 'w', encoding='utf-8') as f:
                    f.write(contents.get('1.0', END))
                    logging.info(
                        'saved a file,call:"{}"'.format(self.filename))
            else:
                self.save_as()
        except FileNotFoundError:
            pass

    def save_as(self, events = None):
        '''save as a file'''
        with tkinter.filedialog.asksaveasfile(title='另存为') as f:
            top.title('NotePad+ : {}'.format(f.name))
            f.write(contents.get('1.0', END))
            logging.info('saved as a file,call:"{}"'.format(self.filename))

    def new(self, events = None):
        '''create a file'''
        contents.delete('1.0', END)
        logging.info('create a file')
        top.title('Unknown')

    def import_file(self, events = None):
        '''import a python file'''
        self.filename_name = tkinter.filedialog.askopenfilename()
        cmd = r'C:\Users\Public\python\py\python.exe', r'C:\Users\Public\python\change.py', self.filename_name, self.filename
        changes = run(cmd)
        self._after_change()

    def change(self, events = None):
        """change a file"""
        cmd = r'C:\Users\Public\python\py\python.exe', r'C:\Users\Public\python\change.py', self.filename
        changes = run(cmd)
        self._after_change()

    def _after_change(self, events = None):
        """after change a file"""
        data = open(r'D:\a.txt', 'r').read()
        open(self.filename, 'w', encoding='utf-8').write(data.strip())
        with open(self.filename, encoding='utf-8') as file:
            contents.delete('1.0', END)
            contents.insert(INSERT, file.read())
            top.title('NotePad+ : %s' % self.filename)
        logging.info('change a file')


events = Events()
logging.info('open app')
menubar = Menu(top)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='新建', command=events.new, accelerator='Ctrl+N')
filemenu.add_command(label='打开', command=events.load, accelerator='Ctrl+O')
filemenu.add_command(label='保存', command=events.save, accelerator='Ctrl+S')
filemenu.add_command(label='另存为', command=events.save_as,
                     accelerator='Ctrl+Shift+S')
filemenu.add_separator()
filemenu.add_command(label='退出', command=top.quit)
menubar.add_cascade(label='文件', menu=filemenu)
top.bind("<Control-n>", events.new)
top.bind("<Control-o>", events.load)
top.bind("<Control-s>", events.save)
top.bind("<Control-Shift-s>", events.save_as)

importmenu = Menu(menubar, tearoff=0)
importmenu.add_command(label='导入文件', command=events.import_file)
importmenu.add_command(label='运行', command=events.change)
menubar.add_cascade(label='导入', menu=importmenu)
top.bind("<Control-i>", events.import_file)
top.bind("<Control-r>", events.change)

top.config(menu=menubar)
tkinter.mainloop()
logging.info('close app')
