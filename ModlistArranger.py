from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import sys
import os
import ast
import webbrowser
import requests
from contextlib import redirect_stderr
from ParseURL import ParseURL
from CategorizedListbox import CategorizedListbox
from OptionDialog import OptionDialog

#Determine current version number
version = 1.4
latest_url = 'https://github.com/yakusai/ModlistArranger/releases/latest/'
download_url = 'https://www.nexusmods.com/skyrimspecialedition/mods/44323?tab=files'

class Main(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        #initialize globals and setup root window
        self.geom = '600x650+{}+{}'.format(str(self._get_default_center()[0]),str(self._get_default_center()[1]))
        self.path = os.getcwd()
        self.name = 'Modlist Arranger - '
        self.basename = 'Untitled'
        self.filter_text = ''
        self.start_collapsed = BooleanVar(value=True)
        self.def_flagged = BooleanVar(value=False)
        self.red_flagged = BooleanVar(value=False)
        self.blu_flagged = BooleanVar(value=False)
        self.gre_flagged = BooleanVar(value=False)
        self.yel_flagged = BooleanVar(value=False)
        self.is_entered = False
        self.is_text_entered = False
        self.can_open_all = False
        self.clicked_widget = None
        self.is_listview = False
        self.notebox = None
        self.notes = ''
        self._settings()
        self._root(parent)
        self.root = parent
        self._configure_menu()
        #setup main frames
        top_frame = Frame(root, bg='#444444', width=450, height=50, pady=3)
        center_frame = Frame(parent, bg='#2d2d2d', width=50,
                             height=50, padx=3, pady=3)
        bottom_frame = Frame (parent, bg='#444444', width=50,
                              height=40, padx=3, pady=3)
        top_frame.grid(row=0, sticky="ew")
        center_frame.grid(row=1, sticky="nsew")
        bottom_frame.grid(row=2, sticky="ew")
        #configure all widgets
        self._configure(top_frame,center_frame,bottom_frame)
        self._configure_top(top_frame)
        self._configure_center(center_frame)
        self._configure_bottom(bottom_frame)
        #set bindings
        self._bind_events(parent)
        #Sets the data for a new modlist
        self.original_data = self._get_data()
        #Loads .malists dropped onto the program
        self.load_dropped_file()


    #====Initial Configuration Methods====
        

    def _settings(self):
        #get or initialize saved settings
        try:
            with open('config.cfg','r') as f:
                data = f.readlines()
            if data[0].lower() == 'listview=true\n':
                self.is_listview = True
            else:
                self.is_listview = False
            self.path = data[1][5:].rstrip()
            self.geom = '{}x{}+{}+{}'.format(data[2][6:].rstrip(),data[3][7:].rstrip(),data[4][2:].rstrip(),data[5][2:].rstrip())
            if data[6].lower() == 'start_collapsed=true\n':
                self.start_collapsed.set(True)
            else:
                self.start_collapsed.set(False)
        except:
            with open('config.cfg','w') as f:
                f.write('listview=false\n')
                f.write('path='+os.getcwd()+'\n')
                f.write('width=600\n')
                f.write('height=650\n')
                f.write('x='+str(self._get_default_center()[0])+'\n')
                f.write('y='+str(self._get_default_center()[1])+'\n')
                f.write('start_collapsed=true\n')
            
    def _root(self, parent):
        parent.title(self.name+self.basename)
        parent.minsize(width=300, height=250)
        parent.geometry(self.geom)
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        parent.option_add('*background', '#444444')
        parent.option_add('*font', 'roboto')
        parent.option_add('*foreground', '#f0f0f0')
        parent.protocol("WM_DELETE_WINDOW",self.exit_command)
        parent.update_idletasks()

    def _configure_menu(self):
        root_menu = Menu(self.root)
        self.root.config(menu=root_menu)
        self.file_menu = Menu(root_menu, tearoff=0)
        self.edit_menu = Menu(root_menu, tearoff=0, postcommand=self._has_mods_command)
        self.color_flag_menu = Menu(root_menu, tearoff=0)
        #create menu items
        root_menu.add_cascade(label='File', menu=self.file_menu)
        root_menu.add_cascade(label='Edit', menu=self.edit_menu)
        #file menu items
        self.file_menu.add_command(label='New File', command=self.new_command,
                                   accelerator='Ctrl+N')
        self.file_menu.add_command(label='Open...', command=self.open_command,
                                   accelerator='Ctrl+O')
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Save', command=self.save_command,
                                   accelerator='Ctrl+S')
        self.file_menu.add_command(label='Save As...',
                                   command=self.saveas_command,
                                   accelerator='Ctrl+Shift+S')
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.exit_command,
                                   accelerator='Ctrl+Q')
        #edit menu items
        self.edit_menu.add_command(label='Open Modlist Notes',
                                   command=self.open_modlist_notes)
        self.edit_menu.add_command(label='Open All Mod Links',
                                   command=self.open_all_mods_command)
        self.edit_menu.add_cascade(label='Flag Color as Non-Mod...',
                                    menu=self.color_flag_menu)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label='Check For All Incompatibilities',
                                   command=self.check_conflicts,
                                   accelerator='Ctrl+E')
        self.edit_menu.add_command(label='Clear All Conflict Highlights',
                                   command=self.clear_conflicts,
                                   accelerator='Ctrl+R')
        self.edit_menu.add_separator()
        self.edit_menu.add_checkbutton(label='Collapse All Mod Categories '
                                       'on Open', onvalue=1, offvalue=0,
                                       variable=self.start_collapsed,
                                       selectcolor='white')
        #flag color submenu items
        self.color_flag_menu.add_checkbutton(label='Default', onvalue=1,
                                             offvalue=0,
                                             variable=self.def_flagged,
                                             selectcolor='white')
        self.color_flag_menu.add_checkbutton(label='Red', onvalue=1,
                                             offvalue=0,
                                             variable=self.red_flagged,
                                             selectcolor='white')
        self.color_flag_menu.add_checkbutton(label='Blue', onvalue=1,
                                             offvalue=0,
                                             variable=self.blu_flagged,
                                             selectcolor='white')
        self.color_flag_menu.add_checkbutton(label='Green', onvalue=1,
                                             offvalue=0,
                                             variable=self.gre_flagged,
                                             selectcolor='white')
        self.color_flag_menu.add_checkbutton(label='Yellow', onvalue=1,
                                             offvalue=0,
                                             variable=self.yel_flagged,
                                             selectcolor='white')

    def _configure(self, t, c, b):
        '''Configure and place the base frames'''
        t.grid(row=0, sticky='ew')
        c.grid(row=1, sticky='nsew')
        b.grid(row=2, sticky="ew")
        #configure weights to ensure proper resizing of housed widgets
        t.grid_columnconfigure(1, weight=1)
        c.grid_columnconfigure(0, weight=1)
        b.grid_columnconfigure(0, weight=1)
        b.grid_columnconfigure(1, weight=1)

    def _configure_top(self, t):
        '''Create and place the top frame widgets'''
        url_input_label = Label(t, text='Quick Add:',
                               bg='#444444', fg='#f0f0f0')
        self.url_entry = Entry(t, bg='white', fg='grey')
        self.url_entry.insert(0, 'Enter Nexus Mod Link Here...')
        self.listview_img = PhotoImage(file = os.path.realpath('listviewbig.png'))
        toggle_view_button = Button(t, image=self.listview_img, bg='#444444',
                                height=2, command=self.toggle_view)
        add_button = Button(t, font=('roboto',12,'bold'), text="Add to End",
                            activebackground='#777777', bg='#444444',
                            fg='#f0f0f0', width=20, height=2, command=self.add_entry)
        #layout widgets
        url_input_label.grid(row=0, column=0)
        self.url_entry.grid(row=0, column=1, sticky="nsew")
        toggle_view_button.grid(row=1, column=0, sticky='nsew')
        add_button.grid(row=1, column=1, columnspan=1, sticky='ew')
                
    def _configure_center(self, c):
        '''Create and place the center widgets'''
        #canvas
        self.canvas = Canvas(c, bg='#2d2d2d')
        self.canvas.pack(side='left',fill='both',expand=True)
        #scrollbar
        y_scrollbar = Scrollbar(c, orient='vertical',
                                command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=y_scrollbar.set) #scroll mapping
        y_scrollbar.pack(side='right',fill='y')
        #modlist
        self.modlistbox = CategorizedListbox(self.canvas, self.is_listview)
        #window (necessary for scrolling)
        self.window = self.canvas.create_window((4,4), window=self.modlistbox,
                                      anchor='nw')

    def _configure_bottom(self, b):
        self.filter = Entry(b, bg='white', fg='grey')
        self.filter.grid(columnspan=2,sticky='nsew')
        self.filter.insert(0, 'Filter')
        self.up_arrow_img = PhotoImage(file = os.path.realpath('arrow-up.png'))
        up_button = Button(b, font='roboto', image=self.up_arrow_img,
                           activebackground='#777777', bg='#444444', fg='#f0f0f0',
                           command=self.modlistbox.moveSelectionUp)
        up_button.grid(row=1, column=1, sticky='nsew')
        self.down_arrow_img = PhotoImage(file = os.path.realpath('arrow-down.png'))
        down_button = Button(b, font='roboto', image=self.down_arrow_img,
                             activebackground='#777777', bg='#444444', fg='#f0f0f0',
                             command=self.modlistbox.moveSelectionDown)
        down_button.grid(row=1, column=0, sticky='nsew')
        self.mod_count_label = Label(b, text='Total Modcount: 0',
                                     font=('arial',12), bg='#444444', fg='#f0f0f0',
                                     anchor='e')
        self.mod_count_label.grid(row=2, columnspan=2, sticky='nsew')
        
    def _bind_events(self, parent):
        '''Binds various commands to keys'''
        #modlist resizing bind
        self.modlistbox.bind('<Configure>', self.set_scroll)
        #middle mouse scroll bind
        self.canvas.bind_all('<MouseWheel>', self.on_mousewheel)
        #canvas window resizing bind
        self.canvas.bind('<Configure>', self.resize_canvas_width)
        #enter events bind
        self.url_entry.bind('<FocusIn>', self.on_text_focus)
        self.url_entry.bind('<FocusOut>', self.on_text_focusout)
        self.canvas.bind('<Enter>', self.on_enter)
        self.canvas.bind('<Leave>', self.on_leave)
        self.modlistbox.bind('<Enter>', self.on_enter)
        #mouse binds
        self.canvas.bind_all('<Button-1>', self.on_click)
        self.canvas.bind_all('<Shift-Button-1>', self.modlistbox.onShiftClickEvent)
        self.canvas.bind_all('<Button-3>', self.on_right_click)
        self.canvas.bind_all('<B1-Motion>', self.on_mouse_motion)
        self.canvas.bind_all('<Double-Button-1>', self.on_double_click)
        #select all mods bind
        parent.bind_all('<Control-a>', self.select_all)
        #file io binds
        parent.bind_all('<Control-n>', self.new_command)
        parent.bind_all('<Control-s>', self.save_command)
        parent.bind_all('<Shift-Control-S>', self.saveas_command)
        parent.bind_all('<Control-o>', self.open_command)
        #filter binds
        self.filter.bind('<FocusIn>', self.on_filter_focus)
        self.filter.bind('<FocusOut>', self.on_filter_focusout)
        self.filter.bind('<KeyRelease>', self.filter_command)
        #key binds
        parent.bind_all('<Control-q>', self.exit_command)
        parent.bind_all('<Control-e>', self.check_conflicts)
        parent.bind_all('<Control-r>', self.clear_conflicts)
        parent.bind_all('<Control-f>', self.focus_filter)
        self.canvas.bind_all('<Up>', self.modlistbox.moveSelectionUp)
        self.canvas.bind_all('<Down>', self.modlistbox.moveSelectionDown)
        self.canvas.bind_all('<Delete>', self.context_delete)
        #update mod count binds
        self.after(100, self.update_count)

    def load_dropped_file(self):
        if len(sys.argv) == 1:
            return
        dropped_file = sys.argv[1]
        if os.path.splitext(dropped_file)[1] == '.malist':
            self._load(dropped_file)
    

    #====Command Methods====

    def toggle_view(self):
        self.modlistbox.toggle_view()
        with open('config.cfg', 'r') as f:
            data = f.readlines()
        if self.modlistbox.modlists[0].listview:
            data[0] = 'listview=true\n'
        else:
            data[0] = 'listview=false\n'
        with open('config.cfg', 'w') as f:
                f.writelines(data)

    def add_entry(self):
        '''adds a valid Nexus URL's mod data into the list'''
        url = self.url_entry.get()
        info = ParseURL.parse_nexus_url(url)
        #insert mod if parsed properly
        if info is not None:
            self.modlistbox.modlists[len(self.modlistbox.modlists)-1].insert(END, info)
            #clear text after completion
            self.url_entry.delete(0, 'end')

    #Text Commands

    def cut(self, entry):
        self.root.clipboard_clear()
        self.root.clipboard_append(entry.selection_get())
        entry.delete('sel.first','sel.last')

    def copy(self, entry):
        self.root.clipboard_clear()
        self.root.clipboard_append(entry.selection_get())
            
    def paste(self, entry):
        try:
            txt = self.root.clipboard_get()
            try:
                index = entry.index('sel.first')
                entry.delete('sel.first','sel.last')
                entry.insert(index, txt)
            except:
                entry.insert('insert', txt)
        except:
            pass

    #====Event Methods====


    #Resize Methods
    def set_scroll(self, event):
        '''reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def resize_canvas_width(self, event):
        '''resizes the canvas windows' width properly'''
        self.canvas.itemconfig(self.window, width = event.width-5)

    #Mouse Methods
    def on_mousewheel(self, event):
        '''scrolls the vertical view by a number of units'''
        x,y = self.root.winfo_pointerxy()
        widget = self.root.winfo_containing(x,y)
        if widget is self.canvas or widget in self._get_all_children(self.canvas):
            self.canvas.yview_scroll(int(2*(-1*(event.delta/120))), "units")

    def on_click(self, event):
        #Get widget type under mouse
        x,y = self.root.winfo_pointerxy()
        self.clicked_widget = self.root.winfo_containing(x,y)
        if self.clicked_widget is not None:
            self.clicked_widget.focus_set()
        if self.is_entered:
            self.modlistbox.onClickEvent(event)

    def on_mouse_motion(self, event):
        #Ensures you can't drag selections when clicking the wrong things
        if type(self.clicked_widget) == Label:
            #triggers selection drags
            self.modlistbox.dragSelection(event)

    def on_right_click(self, event):
        #description editing functionality
        for modlist in self.modlistbox.modlists:
            modlist._check_descs()
        #create the contextual popup menu
        rc_menu = Menu(self.root, tearoff=0)
        #Get widget type under mouse
        x,y = self.root.winfo_pointerxy()
        widget = self.root.winfo_containing(x,y)
        #too lazy to rename every widget to self.clicked_widget
        self.clicked_widget = widget
        self.clicked_widget.focus_set()
        if self.clicked_widget is event.widget:
            if type(widget) in [Entry,Text] and widget.cget('state') == 'normal':
                rc_menu.add_command(label='Paste', command=lambda:self.paste(widget))
                rc_menu.add_command(label='Cut', command=lambda:self.cut(widget))
                rc_menu.add_command(label='Copy', command=lambda:self.copy(widget))
                try:
                    widget_len = len(widget.selection_get())
                except:
                    widget_len = 0
                if widget_len == 0:
                    rc_menu.entryconfig('Cut', state='disabled')
                    rc_menu.entryconfig('Copy', state='disabled')
                    rc_menu.config(disabledforeground='gray')
            elif widget is self.canvas or widget in self._get_all_children(self.canvas):
                    self.modlistbox.rightClickMenu(event, rc_menu)
                    rc_menu.add_separator()
                    rc_menu.add_command(label='Collapse All Categories',
                                        command=self.modlistbox.collapse_all)
                    rc_menu.add_command(label='Expand All Categories',
                                        command=self.modlistbox.expand_all)
        try:
            rc_menu.tk_popup(event.x_root, event.y_root)
        finally:
            rc_menu.grab_release()

    def on_double_click(self, event):
        self.modlistbox.onDoubleClickEvent(event)

    #Entry and Exit Methods
    def on_enter(self, event):
        self.is_entered = True

    def on_leave(self, event):
        self.is_entered = False

    def on_text_focus(self, event):
        """function that gets called whenever entry is clicked"""
        if self.url_entry.get() == 'Enter Nexus Mod Link Here...' and self.filter.cget('fg') == 'grey':
           self.url_entry.delete(0, "end") # delete all the text in the entry
           self.url_entry.insert(0, '') #Insert blank for user input
           self.url_entry.config(fg = 'black')


    def on_text_focusout(self, event):
        if self.url_entry.get() == '':
            self.url_entry.insert(0, 'Enter Nexus Mod Link Here...')
            self.url_entry.config(fg = 'grey')
        
    #Key-Binded Methods
    def select_all(self, event):
        focused_widget = self.root.focus_get()
        if type(focused_widget) is Entry and focused_widget.cget('state') == 'normal' or type(focused_widget) is Text and focused_widget.cget('state') == 'normal':
            pass
        else:
            for modlist in self.modlistbox.modlists:
                modlist.selectAll()

    def context_delete(self, event=None):
        if len(self.modlistbox.selected_modlists) > 0:
            self.modlistbox.delete_selected()
        else:
            self.modlistbox.delete_selected_mod()

    #Automated Methods
    def update_count(self, event=None):
        '''Updates the mod count, and also the unsaved changes indicator'''
        #Gets the colors flagged as non-mods
        colors = []
        if self.def_flagged.get():
            colors.append('#383838')
        if self.red_flagged.get():
            colors.append('red')
        if self.blu_flagged.get():
            colors.append('blue')
        if self.gre_flagged.get():
            colors.append('green')
        if self.yel_flagged.get():
            colors.append('yellow')
        self.mod_count_label.config(text=self.modlistbox.get_mod_count(colors))
        self.update_unsaved_indicator()
        self.after(100, self.update_count)

    def check_conflicts(self, event=None):
        '''Checks each mod's list of incompatibilities with every other mod'''
        infos = []
        mods = []
        conflict_count = 0
        #clear all conflicts first
        for modlist in self.modlistbox.modlists:
            for mod in modlist.modlabel_list:
                mod.conflicts.clear()
        #populate list of all mod data and list of all mods
        for modlist in self.modlistbox.modlists:
            for mod in modlist.modlabel_list:
                mod.update_color(state='revert')
                infos.append(mod.get_info())
                mods.append(mod)
        #for any mod's url found inside the incompatibility list of a mod
        #currently being checked, put both mod's names into eachother's
        #set of conflicts
        for base_mod in mods:
            for conflicting_mod_url in base_mod.get_info()[7]:
                for mod in mods:
                    mod_url = mod.get_info()[0]
                    mod_name = mod.get_info()[1]
                    if base_mod is not mod and conflicting_mod_url == mod_url \
                       and base_mod.get_info()[1] not in mod.conflicts:
                        mod.conflicts.add(base_mod.get_info()[1])
                        base_mod.conflicts.add(mod.get_info()[1])
                        base_mod.update_color('grey', state='alert')
                        mod.update_color('grey', state='alert')
                        conflict_count += 1
        messagebox.showinfo('Conflict Scan Complete', str(conflict_count)+' con'
                            'flict(s) found. Conflicts will be highlighted in '
                            "grey within the list. You may view a mod's con"
                            'flicts by selecting "View Conflicts" when right-.'
                            'clicking that mod.')

    def clear_conflicts(self, event=None):
        '''Reverts all mod colors to their normal state'''
        for modlist in self.modlistbox.modlists:
            for mod in modlist.modlabel_list:
                mod.update_color(state='revert')
                
    #Filter Methods
    def filter_command(self, event):
        '''Updates the display to only show filtered mods'''
        if self.filter_text != self.filter.get():
            self.filter_text = self.filter.get()
            for modlist in self.modlistbox.modlists:
                if len(self.filter_text) > 0:
                    l = []
                    for i in range(len(modlist.modlabel_list)):
                        mod = modlist.modlabel_list[i]
                        if self.filter_text.lower() in mod.get_info()[1].lower():
                            #Adds all filtered mod indices to l
                            l.append(i)
                        else:
                            #Removes the mod from view if not in filter
                            mod.grid_remove()
                    if len(l) == 0:
                        modlist.grid_remove()
                        if modlist.is_collapsed:
                            modlist.force_collapse()
                        self.modlistbox.config(height=1)
                    else:
                        modlist.grid()
                        if modlist.is_collapsed:
                            modlist.force_collapse()
                        #Display all filtered mods
                        for i in l:
                            modlist.modlabel_list[i].grid()
                else:
                    #if filter empty, display modlists normally
                    for modlist in self.modlistbox.modlists:
                        modlist.grid()
                        if modlist.is_collapsed:
                            modlist.force_collapse()
                        else:
                            modlist.force_expand()

    def on_filter_focus(self, event):
        """function that gets called whenever entry is clicked"""
        if self.filter.get() == 'Filter' and self.filter.cget('fg') == 'grey':
           self.filter.delete(0, "end") # delete all the text in the entry
           self.filter.insert(0, '') #Insert blank for user input
           self.filter.config(fg = 'black')
           
    def on_filter_focusout(self, event):
        if self.filter.get() == '':
            self.filter.insert(0, 'Filter')
            self.filter.config(fg = 'grey')

    #====Database Control and Menu Methods====

    def new_command(self,event=None):
        will_continue = self._save_changes()
        self.original_data
        if will_continue:
            d = [['Mods',[]]]
            self.modlistbox.load(d)
            self.original_data = self._get_data()
            self.basename = 'Untitled'
            self.root.title(self.name+self.basename)
        

    def open_command(self,event=None):
        if self.notebox is not None:
            self._close_notes(self.notebox.master)
        will_continue = self._save_changes()
        if will_continue == False:
            return
        file = filedialog.askopenfilename(initialdir = self.path, title='Open',
                                          filetypes=(('Modlist Arranger List Files','*.malist'),
                                                     ('all files','*.*')))
        self._load(file)

    def _load(self, file):
        if file:
            self.path = os.path.dirname(file)
            self._save_path()
            self.basename = os.path.basename(file)
            d = []
            with open(file, 'r', encoding='utf-8') as f:
                data = f.read().splitlines()
            get_notes = False
            self.notes = ''
            for i in range(0,len(data),2):
                if data[i] not in ['','>?<'] and get_notes == False:
                    d.append([data[i],ast.literal_eval(data[i+1])])
                elif data[i] == '>?<':
                    for n in range(i+1,len(data)):
                        self.notes += data[n]+'\n'
                    break
            self.canvas.pack_forget()
            self.modlistbox.load(d)
            if self.start_collapsed.get():
                self.modlistbox.collapse_all()
            self.canvas.pack(side='left',fill='both',expand=True)
            self.original_data = self._get_data()
            self.root.title(self.name+self.basename)

    def save_command(self,event=None):
        if self.basename == 'Untitled':
            file = self.saveas_command()
            if file:
                return True
            else:
                return False
        else:
            if self.notebox is not None:
                self.notes = self.notebox.get('1.0', END).rstrip()+'\n'
            file = '{}\{}'.format(self.path, self.basename)
            self._save(file)
            return True
            
    def _save(self,file):
        if file:
            with open(file, 'w', encoding="utf-8") as f:
                f.write(self._get_data())
            self.path = os.path.dirname(file)
            self._save_path()
            self.basename = os.path.basename(file)
            self.root.title(self.name+self.basename)
            self.original_data = self._get_data()
                        
    def saveas_command(self,event=None):
        if self.notebox is not None:
            self._close_notes(self.notebox.master)
        file = filedialog.asksaveasfilename(initialdir = self.path,title ='Save As', filetypes = (('Modlist Arranger List Files','*.malist'),('all files','*.*')), defaultextension='.malist')
        if file:
            self._save(file)
        return file

    def _get_data(self):
        '''Returns a string with the data of the current modlist for file writing'''
        d = ''
        for modlist in self.modlistbox.modlists:
            d += modlist.name+'\n'
            d += str(modlist.get_all_info())+'\n'
        d += '>?<\n'+self.notes
        return d
    
    def _save_changes(self):
        '''Checks whether changes should be saved, then returns True to continue'''
        data = self._get_data()
        if data != self.original_data:
            values = ['Save',"Don't Save",'Cancel']
            msgBox = OptionDialog(self,'Unsaved Changes Found',
                                  'Do you want to save changes to {}?'.format(self.basename),
                                  values)
            if msgBox.result == 'Save':
                will_continue = self.save_command()
                if will_continue:
                    return True
                else:
                    return False
            elif msgBox.result == 'Cancel':
                return False
            elif msgBox.result == "Don't Save":
                return True
            else:
                return False
        else:
            return True

    def _save_path(self):
        '''Saves the current path to the config file'''
        with open('config.cfg', 'r') as f:
            data = f.readlines()
        data[1] = 'path='+self.path+'\n'
        with open('config.cfg', 'w') as f:
                f.writelines(data)
        
    def exit_command(self):
        self.master.update_idletasks()
        with open('config.cfg', 'r') as f:
            data = f.readlines()
        data[2] = 'width={}\n'.format(self.master.winfo_width())
        data[3] = 'height={}\n'.format(self.master.winfo_height())
        data[4] = 'x={}\n'.format(self.master.winfo_x())
        data[5] = 'y={}\n'.format(self.master.winfo_y())
        data[6] = 'start_collapsed={}\n'.format(self.start_collapsed.get())
        with open('config.cfg', 'w') as f:
            f.writelines(data)
        will_continue = self._save_changes()
        if will_continue:
            self.root.destroy()

    def update_unsaved_indicator(self,event=None):
        data = self._get_data()
        if data != self.original_data:
            self.root.title(self.name+'*'+self.basename+'*')
            

    def open_modlist_notes(self, event=None):
        '''Creates a textbox to edit modlist notes in'''
        frame = Toplevel(self)
        frame.geometry('500x300')
        frame.protocol('WM_DELETE_WINDOW', lambda \
                       a=frame: self._close_notes(a))
        textbox = Text(frame)
        textbox.insert('1.0', self.notes)
        textbox.pack(fill='both',expand=True)
        self.notebox = textbox
##        textbox.bind('<KeyRelease>', lambda event, a=textbox: self._save_text(a))

##    def _save_text(self, textbox):
##        '''Sets the notes variable to the contents of the notes textbox'''
##        self.notes = textbox.get('1.0', END)

    def _close_notes(self, frame):
        self.notes = self.notebox.get('1.0', END).rstrip()+'\n'
        self.notebox = None
        frame.destroy()

    #====Misceallaneous Methods====

    def focus_filter(self, event=None):
        self.filter.focus_set()

    def _get_default_center(self):
        '''Gets the center of the screen at the default width and height'''
        self.update_idletasks()
        width = 600
        height = 650
        screen_width=self.master.winfo_screenwidth()
        screen_height=self.master.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        return (int(x),int(y))

    def _get_all_children (self, wid) :
        '''Gets ALL children of a widget'''
        _list = wid.winfo_children()
        for item in _list :
            if item.winfo_children() :
                _list.extend(item.winfo_children())
        return _list

    def open_all_mods_command(self):
        msgBox = messagebox.askquestion ('Opening All Mod Links',
                                         'Open all mods links in the modlist in your default browser?',
                                         icon = 'warning')
        if msgBox == 'yes':
            for modlist in self.modlistbox.modlists:
                modlist.open_all_links()


    def _has_mods_command(self):
        for modlist in self.modlistbox.modlists:
            if len(modlist.modlabel_list) > 0:
                self.edit_menu.entryconfig('Open All Mod Links', state='normal')
                return
        self.edit_menu.entryconfig('Open All Mod Links', state='disabled')

def check_for_updates(notifyHasLatest=False):
    '''Checks for an updated version online'''
    global latest_url
    global version
    try:
        latest = ParseURL.get_web_version(latest_url)
    except:
        return
    if float(latest) > version:
        msgBox = messagebox.askquestion('New Version Found', 'New version found. Go to download page?')
        if msgBox == 'yes':
            r = requests.head(download_url)
            #Check for valid status codes. 200 for valid, 302 for redirect, 503 for service unavailable
            if r.status_code in [200, 302]:
                webbrowser.open_new(download_url)
            else:
                messagebox.showinfo('Nexus Page Unreachable', 'Nexus page unreachable. Opening Github download page instead.')
                webbrowser.open_new(latest_url)
    elif notifyHasLatest:
        messagebox.showinfo('Up to Date', 'You have the latest version of the program.')


if __name__ == '__main__':
##    with open(os.getcwd()+'\log.txt', 'w') as f:
##        with redirect_stderr(f):
            root = Tk()
            Main(root)
            check_for_updates()
            root.mainloop()
