from tkinter import *

class TagLabel(Frame):
    '''Creates a label with partial borders'''
    def __init__(self, parent, bordercolor, size, *args, **kwargs):
        Frame.__init__(self, parent, bg=bordercolor)
        color = bordercolor
        self.size = size
        self.label = Label(self, *args, **kwargs) #make the label
        self.label.grid(row=0,column=1,sticky='nsew', pady=(0,0), padx=(size,0))
        self.grid_columnconfigure(1,weight=1)

    def update_text(self, text):
        self.label.configure(text=text)
        
##root = Tk()
##tl = TagLabel(root, bordercolor='#666666', size=12,
##               font=('roboto',16,'bold'), text='Test',
##               bg='#444444', fg='#f0f0f0', borderwidth=4,
##               relief='flat')
##tl.pack()
##tl.config(bg='green')
##root.mainloop
