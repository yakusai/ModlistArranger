from tkinter import *
import webbrowser
from ToolTips import CreateToolTip
from LinkGrabber import LinkGrabber

class IncompatibilityManager(Toplevel):
    def __init__(self, parent, incompatibilities, font='roboto', fg='#f0f0f0', bg='#444444', bg2='#2d2d2d', *args, **kwargs):
        Toplevel.__init__(self, bg=bg2, takefocus=True, *args, **kwargs)
        self.grab_set()
        self.geometry('500x300')
        self.title('Incompatibility Manager')
        self.listbox = IncompatibilityListbox(self, bg=bg)
        for i in incompatibilities:
            self.listbox.insert(END, i)
        self.b0 = Button(self,  font=font, bg=bg, fg=fg, text='Add',
                         command=self.add)
        self.b1 = Button(self, font=font, bg=bg, fg=fg, text='Save',
                         command=lambda:self.save(incompatibilities))
        self.b2 = Button(self, font=font, bg=bg, fg=fg, text='Cancel',
                         command=self.destroy)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.listbox.grid(columnspan=3, sticky='nsew', padx=20,pady=(10,0))
        self.b0.grid(row=1, sticky='e', padx=5, ipadx=20, pady=5)
        self.b1.grid(row=1,column=1, padx=5, ipadx=20, pady=5)
        self.b2.grid(row=1,column=2, sticky='w', padx=5, ipadx=20, pady=5)
        #Center the window
        self.update_idletasks()
        x = (self.master.winfo_width()/2) + self.master.winfo_x() - (self.winfo_width()/2)
        y = (self.master.winfo_height()/2) + self.master.winfo_y() - (self.winfo_height()/2)
        self.geometry('+{}+{}'.format(int(x),int(y)))
        #Prevent code execution from parent until this window closes
        self.wait_window()

    def add(self):
        l = []
        LinkGrabber(self, l)
        current = []
        for label in self.listbox.label_list:
            current.append(label.url.cget('text'))
        for i in l:
            if i not in current:
                self.listbox.insert(END, i)
        
    def save(self, incompatibilities):
        new = []
        for label in self.listbox.label_list:
            new.append(label.url.cget('text'))
        incompatibilities[:] = new
        self.destroy()

class IncompatibilityListbox(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.label_list = []
        self.grid_columnconfigure(0, weight=1)        

    def insert(self, index, url):
        if index == END or index > len(self.label_list):
            index = len(self.label_list)
        url_label = IncompatibilityLabel(self, url)
        self.label_list.insert(index, url_label)
        if len(self.label_list) > index:
            for x in range(index,len(self.label_list)):
                self.label_list[x].grid(row=x, column=0, sticky='nsew')
        else:
            url_label.grid(row=len(self.mod_list), column=0, sticky='nsew')

    def delete(self, index):
        if index == END:
            index = len(self.label_list) - 1
        if index < len(self.label_list) - 1:
            for x in range(index,len(self.label_list)-1):
                self.label_list[x+1].grid(row=x, column=0, sticky='nsew')
        self.label_list[index].grid_forget()
        self.label_list[index].destroy()
        del self.label_list[index]
        if len(self.label_list) == 0:
            self.configure(height=1)

class IncompatibilityLabel(Frame):
    def __init__(self, parent, url):
        Frame.__init__(self, parent, bg='#444444')
        self.is_entered = False
        self.url = Label(self, text=url, font=('roboto',12), bg='#444444',
                         fg='#f0f0f0', anchor='w', cursor='hand2')
        self.url.pack(fill='x')
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.url.bind('<ButtonRelease-1>', self.callback)
        self.url.bind('<ButtonRelease-3>', self.delete)
        tiptext = 'Left click a URL to open it in your browser. Right click ' \
                  'one to remove it.'
        CreateToolTip(self.url, tiptext, waittime = 0)

    def on_enter(self, event):
        self.url.configure(font=('roboto',12,'underline'))
        self.is_entered = True

    def on_leave(self, event):
        self.url.configure(font=('roboto',12))
        self.is_entered = False

    def callback(self, event):
        if self.is_entered:
            webbrowser.open_new(self.url.cget('text'))

    def delete(self, event):
        if self.is_entered:
            self.master.delete(self.master.label_list.index(self))

class ConflictListbox(Toplevel):
    def __init__(self, parent, conflicts, font='roboto', fg='#f0f0f0', bg='#444444', bg2='#2d2d2d', *args, **kwargs):
        Toplevel.__init__(self, bg=bg2, takefocus=True, *args, **kwargs)
        '''Display's a conflict list'''
        self.grab_set()
        self.geometry('400x300')
        self.title('Conflicts')
        self.listbox = Listbox(self, bg=bg, font=font, fg=fg)
        for conflict in conflicts:
            self.listbox.insert(END, conflict)
        self.listbox.pack(fill='both', expand = True, padx=20,pady=20)
        #Center the window
        self.update_idletasks()
        x = (self.master.winfo_width()/2) + self.master.winfo_x() - (self.winfo_width()/2)
        y = (self.master.winfo_height()/2) + self.master.winfo_y() - (self.winfo_height()/2)
        self.geometry('+{}+{}'.format(int(x),int(y)))
        #Prevent code execution from parent until this window closes
        self.wait_window()
    
    
#testing  
if __name__ == '__main__':
    root = Tk()
    l = ['https://www.twitch.tv/videos/870424157',2,3,4]
    b = Button(root, text='E', command = lambda : IncompatibilityManager(root, l))
    b.pack()
    root.mainloop()
