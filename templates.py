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
from subprocess import run, PIPE


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

    def load(self):
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

    def save(self):
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

    def save_as(self):
        '''save as a file'''
        with tkinter.filedialog.asksaveasfile(title='另存为') as f:
            top.title('NotePad+ : {}'.format(f.name))
            f.write(contents.get('1.0', END))
            logging.info('saved as a file,call:"{}"'.format(self.filename))

    def new(self):
        '''create a file'''
        contents.delete('1.0', END)
        logging.info('create a file')
        top.title('Unknown')

    def import_file(self):
        '''import a python file'''
        choose = tkinter.messagebox.askyesno(title='选择', message='是否导入文件')
        if choose:
            self.filename_name = tkinter.filedialog.askopenfilename()
            cmd = r'C:\Users\Public\python\py\python.exe', r'C:\Users\Public\python\change.py', self.filename_name, self.filename
            changes = run(cmd)
        else:
            cmd = r'C:\Users\Public\python\py\python.exe', r'C:\Users\Public\python\change.py', self.filename
            changes = run(cmd)
        data = open(r'D:\a.txt', 'r').read()
        open(self.filename, 'w', encoding='utf-8').write(data.strip())
        with open(self.filename, encoding='utf-8') as file:
            contents.delete('1.0', END)
            contents.insert(INSERT, file.read())
            top.title('NotePad+ : %s' % self.filename)
        logging.info('import a python file')


events = Events()
logging.info('open app')
Button(text='new', command=events.new).pack(side=LEFT)
Button(text='open', command=events.load).pack(side=LEFT)
Button(text='save', command=events.save).pack(side=LEFT)
Button(text='save as', command=events.save_as).pack(side=LEFT)
Button(text='import', command=events.import_file).pack(side=LEFT)
tkinter.mainloop()
logging.info('close app')
