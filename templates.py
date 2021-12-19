import re
from tkinter import *
from tkinter.constants import BOTH, BOTTOM, END, INSERT, LEFT
from tkinter.scrolledtext import ScrolledText
import tkinter.messagebox
import tkinter.filedialog
from tkinter.ttk import *
import logging
import sys

field_pat = re.compile(r'-(.+?)-')
scope = {}

top = Tk()
top.title('NotePad+')
contents = ScrolledText()
contents.pack(side=BOTTOM, expand=True, fill=BOTH)

# filenames = tkinter.Entry()
# filenames.pack(side=LEFT, expand=True, fill=X)

logging.basicConfig(filename='log.log', level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s %(message)s')


def _re_placement(match):
    code = match.group(1)
    try:
        return str(eval(code, scope))
    except SyntaxError:
        exec(code, scope)
        return ''


class Events:
    def __init__(self):
        self.filename = self.init_path = r'C:\Users\Public\Documents\un-know.txt'

    def load(self):
        try:
            self.filename = tkinter.filedialog.askopenfilename()
            with open(self.filename) as file:
                contents.delete('1.0', END)
                contents.insert(INSERT, file.read())
                logging.info('opened a file,call:"{}"'.format(self.filename))
                top.title('NotePad+ : {}'.format(self.filename))
        except FileNotFoundError:
            pass

    def change(self):
        try:
            with tkinter.filedialog.asksaveasfile() as f:
                lines = []
                for line in open(self.filename, 'r').read():
                    lines.append(line)
                text = ''.join(lines)
                f.write(field_pat.sub(_re_placement, text))
                logging.info('changed a file,call:"{}"'.format(self.filename))
        except Exception as e:
            tkinter.messagebox.showerror(title='Error', message='Error: ' + str(e))
            logging.error(e)

    def save(self):
        try:
            if self.filename != self.init_path:
                with open(self.filename, 'w') as f:
                    f.write(contents.get('1.0', END))
                    logging.info('saved a file,call:"{}"'.format(self.filename))
            else:
                self.save_as()
        except FileNotFoundError:
            pass

    def save_as(self):
        with tkinter.filedialog.asksaveasfile(title='另存为') as f:
            top.title('NotePad+ : {}'.format(f.filename))
            f.write(contents.get('1.0', END))
            logging.info('saved as a file,call:"{}"'.format(self.filename))

    def new(self):
        contents.delete('1.0', END)
        logging.info('create a file')
        top.title('Un know')
        
    def import_file(self):
        self.filename = tkinter.filedialog.askopenfilename()
        self.file = re.findall(r'[A-Z0-9a-z]*\.py', self.filename)
        self.file = self.file[0]
        sys.path.append(self.filename[0:-len(self.file)])
        exec('from {} import *'.format(self.file[0:-3]), scope)


events = Events()
logging.info('open app')
Button(text='new', command=events.new).pack(side=LEFT)
Button(text='open', command=events.load).pack(side=LEFT)
Button(text='change as', command=events.change).pack(side=LEFT)
Button(text='save', command=events.save).pack(side=LEFT)
Button(text='save as', command=events.save_as).pack(side=LEFT)
Button(text='import', command=events.import_file).pack(side=LEFT)
tkinter.mainloop()
logging.info('close app')
