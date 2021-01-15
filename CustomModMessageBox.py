from tkinter import *
from tkinter import messagebox
import validators


class CustomModMessageBox(Toplevel):
    def __init__(self, parent, title, info_list, font='roboto', fg='#f0f0f0', bg='#444444',*args,**kwargs):
        Toplevel.__init__(self, takefocus=True, *args,**kwargs)
        self.grab_set()
        self.title(title)
        self.configure(bg=bg)
        #url
        self.i0_label = Label(self,text="Enter the mod's url (required):",bg=bg,font=font,fg=fg,anchor='w')
        self.i0_entry = Entry(self,bg=bg,fg='#f0f0f0',font=font,insertbackground='white')
        self.i0_label.pack(fill='x',padx=20,pady=(10,0))
        self.i0_entry.pack(fill='x',padx=20)
        #name
        self.i1_label = Label(self,text="Enter the mod's displayed name (required):",bg=bg,font=font,fg=fg,anchor='w')
        self.i1_entry = Entry(self,bg=bg,fg='#f0f0f0',font=font,insertbackground='white')
        self.i1_label.pack(fill='x',padx=20)
        self.i1_entry.pack(fill='x',padx=20)
        #game
        self.i2_label = Label(self,text="Enter the name of the game the mod is for:",bg=bg,font=font,fg=fg,anchor='w')
        self.i2_entry = Entry(self,bg=bg,fg='#f0f0f0',font=font,insertbackground='white')
        self.i2_label.pack(fill='x',padx=20)
        self.i2_entry.pack(fill='x',padx=20)
        #site or location
        self.i5_label = Label(self,text="Enter the site or place this mod is from:",bg=bg,font=font,fg=fg,anchor='w')
        self.i5_entry = Entry(self,bg=bg,fg='#f0f0f0',font=font,insertbackground='white')
        self.i5_label.pack(fill='x',padx=20)
        self.i5_entry.pack(fill='x',padx=20,pady=(0,5))
        #buttons
        self.b_ok = Button(self, text='OK',bg=bg,font=font,fg=fg,command=lambda:self.on_confirm(info_list))
        self.b_ok.pack(side='left',fill='x',expand=True,padx=5,pady=5)
        self.b_cancel = Button(self, text='Cancel',bg=bg,font=font,fg=fg,command=self.destroy)
        self.b_cancel.pack(side='right',fill='x',expand=True,padx=5,pady=5)
        #geometry
        self.resizable(width=False,height=False)
        x = (self.master.winfo_width()/2) + self.master.winfo_x() - (350/2)
        y = (self.master.winfo_height()/2) + self.master.winfo_y() - (240/2)
        self.geometry('350x240+{}+{}'.format(int(x),int(y)))
        ## wait.window ensures that calling function waits for the window to
        ## close before the result is returned.
        self.wait_window()

    def on_confirm(self, info_list):
        i0 = self.i0_entry.get()
        i1 = self.i1_entry.get()
        i2 = self.i2_entry.get()
        i5 = self.i5_entry.get()
        if validators.url(i0) == True and i1 != '':
            info_list.append(i0)
            info_list.append(i1)
            info_list.append(i2)
            info_list.append('')
            info_list.append('')
            info_list.append(i5)
            self.destroy()
        elif validators.url(i0) != True:
            messagebox.showinfo('Invalid URL', 'A valid URL (including "https://" or "http://") MUST be associated with the mod.')
        else:
            messagebox.showinfo('No Name Input', 'The mod must have a name.')


##class MBox()

''' test code
##D = {'
root = Tk()
l = []
b = Button(root, text='E', command = lambda : CustomModMessageBox(root,'E',l))
b.pack()
##c = CustomModMessageBox('E')
##print(c.winfo_reqheight())
root.mainloop()
'''
