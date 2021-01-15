from tkinter import *

class ExpandToText(Text):
    def __init__(self, master=None, **kwargs):
        '''Resizes the widget to always fit its contents'''
        Text.__init__(self, master, **kwargs)
        self.bind('<Configure>', self.update_height)
        self.bind('<Key>', self.update_height)
        
    def update_height(self, event):
        '''Updates the height of the widget to be the number of lines of text'''
        height=self.count('1.0', 'end', 'displaylines')[0]
        self.configure(height=height)

class TextResizer(Text):
    def __init__(self, master=None, **kwargs):
        '''Resizes the text in the widget to fit the widget size, up to a limit'''
        Text.__init__(self, master, **kwargs)
        self.bind('<Configure>', self.update_size)
        self.bind('<Key>', self.update_size)

    def update_size(self, event):
        new_size = int(round(self.winfo_width()/4))
        if new_size > 12:
            new_size = 12
        self.configure(font=('roboto',new_size))
