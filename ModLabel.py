from tkinter import *
import webbrowser


class ModLabel(Frame):
    def __init__(self, parent, info, index, listview = False):
        '''displays mod information obtained from the info list'''
        Frame.__init__(self, parent, bg='#2d2d2d')
        self.info = info
        self.listview = listview
        #set the index variable to the input index
        self.true_index = index
        #set default color
        self.color = '#383838'
        #set default boolean variables
        self.is_focused = False
        self.is_title_focused = False
        self.is_selected = False
        self.is_index_focused = False
        #set incompatibility list and conflicts set
        self.incompatibilities = []
        self.conflicts = set()
        #configure widget to resize properly
        self.grid_columnconfigure(1, weight=1)
        #create all widgets
        self.index = Label(self, font=('roboto',40), text=index+1, bg='#444444', fg='#f0f0f0', bd=2, relief='ridge', anchor='center')
        self.title = Entry(self, font=('roboto',15,'bold'), readonlybackground='#383838', fg='#f0f0f0', cursor='hand2')
        self.game = Entry(self, font=('roboto',12), readonlybackground='#383838', fg='#f0f0f0', width=14)
        self.version = Entry(self, font=('roboto',12), readonlybackground='#383838', fg='#f0f0f0', width=7)
        self.description = Text(self, font=('roboto',12), bg='#2d2d2d',
                                fg='#f0f0f0', height=2, undo=True,
                                insertbackground='white')
        #insert text into Entry and Text widgets
        self.title.insert(END, info[1])
        self.game.insert(END, info[2])
        self.version.insert(END, info[5])
        self.description.insert(END, info[3])
        #layout all widgets
        self.index.grid(row=0, rowspan=2, column=0, sticky='nsew', ipadx=16)
        self.title.grid(row=0, column=1, sticky='nsew', ipadx=16)
        self.game.grid(row=0, column=2, sticky='nsew', ipadx=16)
        self.version.grid(row=0, column=3, sticky='nsew')
        self.description.grid(row=1, column=1, columnspan=3, sticky='nsew')
        self.description.grid_propagate(False)
        #change layout depending on display state
        if self.listview:
            self.display_listview()
        else:
            self.display_default()
        #configure the states of each widget
        self.title.configure(state='readonly')
        self.game.configure(state='readonly')
        self.version.configure(state='readonly')
        self.description.configure(state='disabled',inactiveselectbackground=self.description.cget("selectbackground"))
        #bind functionality commands to their appropriate events
        self.title.bind('<ButtonRelease-1>', lambda e: self.callback(info[0]))
        self.title.bind('<ButtonRelease-2>', lambda e: self.callback(info[0]))
        self.title.bind('<Enter>', self.on_enter)
        self.title.bind('<Leave>', self.on_leave)
        self.index.bind('<Enter>', self.on_enter_index)
        self.index.bind('<Leave>', self.on_leave_index)
        self.bind('<Enter>', self.on_enter_all)
        self.bind('<Leave>', self.on_leave_all)
        self.description.bind('<Return>', self.disable_newline)

    def disable_newline(self, event):
        return 'break'
        
    def toggle_view(self):
        '''toggles the display between the default and the smaller listview'''
        if self.listview:
            self.display_default()
        else:
            self.display_listview()

    def display_default(self):
        self.index.grid(row=0, rowspan=2, column=0, sticky='nsew',ipadx=16)
        self.title.configure(font=('roboto',15,'bold'))
        self.index.configure(font=('roboto',40))
        self.description.grid()
        self.listview = False

    def display_listview(self):
        self.index.grid(row=0, rowspan=1, column=0, sticky='nsew',ipadx=16)
        self.title.configure(font=('roboto',12))
        self.index.configure(font=('roboto',15))
        self.description.grid_remove()
        self.listview = True

    def enable_desc_edit(self, event=None):
        self.description.configure(state='normal')

    def disable_desc_edit(self, event=None):
        self.description.configure(state='disabled')

    def get_info(self):
        '''info indices: 0=url,1=title,2=game,3=desc,
        4=version,5=site,6=color,7=incompatibilities'''
        info = []
        info.append(self.info[0])
        info.append(self.title.get())
        info.append(self.game.get())
        info.append(self.description.get('1.0', END).rstrip())
        info.append(self.info[4])
        info.append(self.version.get())
        info.append(self.color)
        info.append(self.incompatibilities)
        return info
        
    def update_index(self, index):
        self.index.configure(text=index+1)
        self.true_index = index

    def update_color(self, bg='#383838', state='normal'):
        '''Changes the color of the title label based on the state'''
        if state.lower() == 'normal':
            self.color = bg
            self.title.config(readonlybackground=self.color)
            self.game.config(readonlybackground=self.color)
            self.version.config(readonlybackground=self.color)
        elif state.lower() == 'revert':
            self.title.config(readonlybackground=self.color)
            self.game.config(readonlybackground=self.color)
            self.version.config(readonlybackground=self.color)
            self.description.config(bg='#2d2d2d', fg='#f0f0f0')
        elif state.lower() == 'alert':
            self.title.config(readonlybackground=bg)
            self.game.config(readonlybackground=bg)
            self.version.config(readonlybackground=bg)
            self.description.config(bg=bg)
        if self.title.cget('readonlybackground') in ['yellow', 'white', 'grey']:
            fg = '#2d2d2d'
        else:
            fg = '#f0f0f0'
        self.title.config(fg=fg)
        self.game.config(fg=fg)
        self.version.config(fg=fg)
        if state.lower() == 'alert':
            self.description.config(fg=fg)
        
    def get_index(self):
        return self.true_index

    def select(self):
        if self.is_index_focused:
            self.is_selected = True
            self.index.configure(bg='#f0f0f0', fg='#444444')
        else:
            self.is_selected = False
            self.index.configure(bg='#444444', fg='#f0f0f0')

    def force_select(self):
        self.is_selected = True
        self.index.configure(bg='#f0f0f0', fg='#444444')

    def force_deselect(self):
        self.is_selected = False
        self.index.configure(bg='#444444', fg='#f0f0f0')

    def is_selected(self):
        '''Returns mouse selection state'''
        return self.is_selected

    def callback(self, url):
        '''opens the target url on click'''
        if self.is_title_focused:
            webbrowser.open_new(url)

    def on_enter(self, event):
        '''underlines the mod's title when the mouse hovers over it and sets is_title_focused to True'''
        if self.listview:
            self.title.configure(font=('roboto',12,'underline'))
        else:
            self.title.configure(font=('roboto',15,'bold','underline'))
        self.is_title_focused = True

    def on_leave(self, event):
        '''stops underlining the mod's title when the mouse stops hovering over it and sets is_title_focused to False'''
        if self.listview:
            self.title.configure(font=('roboto',12))
        else:
            self.title.configure(font=('roboto',15,'bold'))
        self.is_title_focused = False

    def on_enter_index(self, event):
        self.is_index_focused = True

    def on_leave_index(self, event):
        self.is_index_focused = False

    def on_enter_all(self, event):
        self.is_focused = True

    def on_leave_all(self, event):
        self.is_focused = False
