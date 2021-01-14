from tkinter import *
from tkinter import messagebox

class OptionDialog(Toplevel):
    """
        This dialog accepts a list of options.
        If an option is selected, the results property is to that option value
        If the box is closed, the results property is set to zero
    """
    def __init__(self,parent,title,question,options):
        Toplevel.__init__(self,parent,bg='#444444')
        self.bg='#444444'
        self.fg='#f0f0f0'
        self.font=('roboto',12)
        self.title(title)
        self.question = question
        self.transient(parent)
        self.protocol("WM_DELETE_WINDOW",self.cancel)
        self.options = options
        self.result = '_'
        self.createWidgets()
        self.grab_set()
        self.update_idletasks()
        x = (self.master.master.winfo_width()/2) + self.master.master.winfo_x() - (self.winfo_width()/2)
        y = (self.master.master.winfo_height()/2) + self.master.master.winfo_y() - (self.winfo_height()/2)
        self.geometry('+{}+{}'.format(int(x),int(y)))
        self.resizable(width=False,height=False)
        ## wait.window ensures that calling function waits for the window to
        ## close before the result is returned.
        self.wait_window()
        
    def createWidgets(self):
        frmQuestion = Frame(self,bg=self.bg)
        Label(frmQuestion,text=self.question,font=self.font,height=2,width=40,
              anchor='w', bg=self.bg, fg=self.fg).grid(sticky='w',padx=5)
        frmQuestion.grid(row=1)
        frmButtons = Frame(self, bg=self.bg)
        frmButtons.grid(row=2,sticky='e')
        column = 0
        for option in self.options:
            btn = Button(frmButtons,text=option,font=self.font,bg=self.bg,
                         fg=self.fg,command=lambda x=option:self.setOption(x))
            btn.grid(column=column,row=0,sticky='e',padx=2.5,pady=5,ipadx=15)
            column += 1
    def setOption(self,optionSelected):
        self.result = optionSelected
        self.destroy()
    def cancel(self):
        self.result = None
        self.destroy()



##if __name__ == '__main__':
##    #test the dialog
##    root=Tk()
##    def run():
##        values = ['Save',"Don't Save",'Cancel']
##        dlg = OptionDialog(root,'Unsaved Changes Found',"Do you want to save changes?",values)
##        print(dlg.result)
##    Button(root,text='Dialog',command=run).pack()
##    root.mainloop()
