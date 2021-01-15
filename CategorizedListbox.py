from tkinter import *
from tkinter import messagebox
from ordered_set import OrderedSet
from tkinter.simpledialog import askstring
import webbrowser
from ModlistListbox import ModlistListbox
from TagLabel import TagLabel
from IncompatibilityManager import IncompatibilityManager, ConflictListbox


class CategorizedListbox(Frame): #AKA CLB
    def __init__(self, parent, listview):
        Frame.__init__(self, parent)
        self.root = parent
        #creates the list that will house all controlled ModlistListboxes
        self.modlists = []
        self.selected_modlists = OrderedSet([])
        self.listview = listview
        self.current_index = 0
        self.grid_columnconfigure(0,weight=1)
        #checks for whether a pre-made CLB was input
        if len(self.modlists) <= 0:
            #Creates the default category 'Mods' when a new CLB is created
            self.insert(0, 'Mods')
        else:
            #Populates CLB with modlists given
            self.modlists = modlists
        
    def split(self, name, modlist_index, first, Last=None):
        '''Creates a new mod listbox with the mods of its original mod
        listbox based on the given indices, or an empty mod listbox'''
        modlist = self.modlists[modlist_index]
        if Last is None:
            pass

    def load(self, named_modlists):
        for i in range(len(self.modlists)):
            self.delete(0, force_delete=True)
        for named_modlist in named_modlists:
            self.insert(END, named_modlist[0], named_modlist[1])

    def get_mod_count(self):
        n = 0
        for modlist in self.modlists:
            n += len(modlist.modlabel_list)
        return 'Total Modcount: '+str(n)

    def insert(self, index, name, modlist_info=None, is_collapsed=False):
        '''Create and insert a new modlist at the given modlist index'''
        modlist = ModlistListbox(self, self.listview, name)
        #if modlist info given, populate modlistbox with mods
        if modlist_info is not None and modlist_info != []:
            for i in range(len(modlist_info)):
                modlist.insert(i, modlist_info[i])
        #collapse mods if necessary
        if is_collapsed:
            modlist.force_collapse()
        #check last index values and set index accordingly
        if index == END or index >= len(self.modlists):
            index = len(self.modlists)
        #insert modlist into modlists list
        self.modlists.insert(index, modlist)
        #move modlists down if after inserted modlist
        if len(self.modlists) > index:
            for x in range(index,len(self.modlists)):
                self.modlists[x].grid(row=x, column=0, sticky='nsew')
        else:
            modlist.grid(row=len(self.mod_list), column=0, sticky='nsew')
        #Set modlist name label size
        self.update()

    def insert_input(self, index):
        if index == END:
            index = len(self.modlists)
        name = askstring('New Category at Index '+str(index+1), 'Name of new category:')
        if name is not None and name != '':
            self.insert(index, name)

    def merge_up(self, index):
        '''Merge the modlist at the given index with the modlist above it'''
        msgBox = messagebox.askquestion ('Merge Categories Confirmation',
                                         'Merge "'+self.modlists[index].name+'" into "'+self.modlists[index-1].name+'"?',
                                         icon = 'warning')
        if msgBox == 'yes':
            #populate list of mod info lists to add to and from, then get name
            l1 = self.modlists[index-1].get_all_info()
            l2 = self.modlists[index].get_all_info()
            l_name = self.modlists[index-1].get_name()
            #insert new merged modlist
            self.insert(index-1, l_name, l1+l2)
            #delete both previous modlists
            for x in range(2):
                self.delete(index)
    
    def merge_down(self, index):
        '''Merge the modlist at the given index with the modlist below it'''
        msgBox = messagebox.askquestion ('Merge Categories Confirmation',
                                         'Merge "'+self.modlists[index].name+'" into "'+self.modlists[index+1].name+'"?',
                                         icon = 'warning')
        if msgBox == 'yes':
            #populate list of mod info lists to add to and from, then get name
            l1 = self.modlists[index+1].get_all_info()
            l2 = self.modlists[index].get_all_info()
            l_name = self.modlists[index+1].get_name()
            #insert new merged modlist
            self.insert(index, l_name, l1+l2)
            #delete both previous modlists
            for x in range(2):
                self.delete(index+1)
            
    def delete_confirm(self,index):
        msgBox = messagebox.askquestion ('Removing Category',
                                         'Remove the "'+self.modlists[index].name+'" Category and its contents?',
                                         icon = 'warning')
        if msgBox == 'yes':
            self.delete(index)

    def delete(self,index,force_delete=False):
        '''delete a modlist at the given index'''
        if not force_delete and len(self.modlists) == 1:
            messagebox.showinfo('Prohibited Action',
                                'You must always have at least one category in the list.')
        else:
            if index == END:
                index = len(self.mod_list)
            if index<len(self.modlists)-1:
                for x in range(index,len(self.modlists)-1):
                    self.modlists[x+1].grid(row=x, column=0, sticky='nsew')
            if self.modlists[index] in self.selected_modlists:
                self.selected_modlists.remove(self.modlists[index])
            self.modlists[index].grid_forget()
            self.modlists[index].destroy()
            del self.modlists[index]
        
    def collapse_all(self):
        '''Collapses all mod listboxes'''
        for mod in self.modlists:
            if not mod.is_collapsed:
                mod.force_collapse()

    def expand_all(self):
        for mod in self.modlists:
            if mod.is_collapsed:
                mod.force_expand()

    def get_info(self):
        '''Gets a list of lists of mods throughout ALL modlists'''
        list = []
        for modlist in self.modlists:
            list.append(modlist.get_all_info())
        return list

    def get_all_info(self):
        '''Gets a list of lists of all modlists'''
        return self.modlists

    def rename(self, index):
        '''Rename a category at the given index by remaking the category'''
        name = askstring('Rename Category at Index '+str(index+1),
                         'New name of category:')
        if name is not None and name != '':
            data = self.modlists[index].get_all_info()
            is_collapsed = self.modlists[index].is_collapsed
            self.delete(index,force_delete=True)
            self.insert(index, name, data)
            self.modlists[index].forceSelectTop()
            if is_collapsed:
                self.modlists[index].force_collapse()


    #====passed or modified modlist functions====


    def onShiftClickEvent(self, event):
        for modlist in self.modlists:
            modlist.onShiftClickEvent(event)

    def dragSelection(self, event):
        '''Moves selected mods depending on mouse movement, and moves mods
        into and out of categories they are moved into and out of'''
        for modlist in self.modlists:
            modlist.dragSelection(event)

    def moveInto(self, direction, modlist):
        '''Depending on the direction, move the selected mods from the modlist
        into the modlist below or above it'''
        modlist_index = self.modlists.index(modlist)
        if direction == -1 and modlist_index != 0:
            #Move up
            for mod in sorted(modlist.selected_modlabel_list,
                              key=lambda x: x.get_index()):
                self.modlists[modlist_index-1].insert(END, mod.get_info())
                #messy code to make the mod in the new category selected
                new_upper_mod = self.modlists[modlist_index-1].modlabel_list[-1]
                new_upper_mod.force_select()
                self.modlists[modlist_index-1].selected_modlabel_list.append(new_upper_mod)
            selected_list_len = len(modlist.selected_modlabel_list)
            for i in range(selected_list_len):
                modlist.delete(0)
            modlist.selected_modlabel_list.clear()
            self.modlists[modlist_index-1].force_expand()
        elif direction == 1 and modlist_index != len(self.modlists)-1:
            #Move down
            for mod in sorted(modlist.selected_modlabel_list,
                              key=lambda x: x.get_index(), reverse=True):
                self.modlists[modlist_index+1].insert(0, mod.get_info())
                #messy code to make the mod in the new category selected
                new_lower_mod = self.modlists[modlist_index+1].modlabel_list[0]
                new_lower_mod.force_select()
                self.modlists[modlist_index+1].selected_modlabel_list.append(new_lower_mod)
            selected_list_len = len(modlist.selected_modlabel_list)
            for i in range(selected_list_len):
                modlist.delete(END)
            modlist.selected_modlabel_list.clear()
            self.modlists[modlist_index+1].force_expand()
            
    def moveSelectionUp(self, event=None):
        focused_widget = self.master.master.focus_get()
        if event is not None and type(focused_widget) in [Entry,Text] and focused_widget.cget('state') == 'normal':
            return
        else:
            top_selected = False
            if len(self.selected_modlists) > 0:
                for modlist in self.modlists:
                    if modlist.is_top_selected:
                        top_selected = True
            if top_selected:
                sorted_selected_modlists = sorted(self.selected_modlists,
                                                  key=lambda x: self.modlists.index(x))
                if sorted_selected_modlists[-1] == self.modlists[0]:
                    return
                for modlist in sorted_selected_modlists:
                    modlist_index = self.modlists.index(modlist)
                    list_to_move = self.modlists[modlist_index-1].get_all_info()
                    list_to_move_name = self.modlists[modlist_index-1].get_name()
                    list_to_move_is_collapsed = self.modlists[modlist_index-1].is_collapsed
                    self.delete(modlist_index-1)
                    self.insert(modlist_index, list_to_move_name, list_to_move, list_to_move_is_collapsed)
                    #Collapse the category moved if it was collapsed
                    if list_to_move_is_collapsed:
                        self.modlists[modlist_index].force_collapse()
            else:
                for modlist in self.modlists:
                    n = 0
                    n = modlist.moveSelectionUp()
                    if n == -1:
                        self.moveInto(n, modlist)

    def moveSelectionDown(self, event=None):
        focused_widget = self.master.master.focus_get()
        if event is not None and type(focused_widget) in [Entry,Text] and focused_widget.cget('state') == 'normal':
            return
        else:
            top_selected = False
            if len(self.selected_modlists) > 0:
                for modlist in self.modlists:
                    if modlist.is_top_selected:
                        top_selected = True
            if top_selected:
                sorted_selected_modlists = sorted(self.selected_modlists,
                                                  key=lambda x: self.modlists.index(x))
                if sorted_selected_modlists[-1] == self.modlists[-1]:
                    return
                for modlist in sorted_selected_modlists:
                    modlist_index = self.modlists.index(modlist)
                    list_to_move = self.modlists[modlist_index+1].get_all_info()
                    list_to_move_name = self.modlists[modlist_index+1].get_name()
                    list_to_move_is_collapsed = self.modlists[modlist_index+1].is_collapsed
                    self.delete(self.modlists.index(modlist)+1)
                    self.insert(modlist_index, list_to_move_name, list_to_move, list_to_move_is_collapsed)
                    #Collapse the category moved if it was collapsed
                    if list_to_move_is_collapsed:
                        self.modlists[modlist_index].force_collapse()
            else:
                for modlist in self.modlists:
                    n = 0
                    n = modlist.moveSelectionDown()
                    if n == 1:
                        self.moveInto(n, modlist)
                        return

    def onClickEvent(self, event):
        for x in range(len(self.modlists)):
            modlist = self.modlists[x]
            modlist.selectTop()
            if modlist.is_top_selected and modlist not in self.selected_modlists:
                self.current_index = x
                self.selected_modlists.append(modlist)
            elif not modlist.is_top_selected and modlist in self.selected_modlists:
                self.selected_modlists.remove(modlist)
        for modlist in self.modlists:
            modlist.onClickEvent(event)

    def selectAll(self):
        for modlist in self.modlists:
            modlist.forceDeselectTop()
            modlist.selectAll()
        self.selected_modlists.clear()

    def deleteSelected(self):
        msgBox = messagebox.askquestion ('Removing Selected',
                                         'Remove selected mods from the list?',
                                         icon = 'warning')
        if msgBox == 'yes':
            for modlist in self.modlists:
                modlist.delete_selected()

    def deleteAll(self):
        msgBox = messagebox.askquestion ('Removing All',
                                         'Remove all mods from the list?',
                                         icon = 'warning')
        if msgBox == 'yes':
            for modlist in self.modlists:
                modlist.delete_all()

    def insert_mod(self, modlist_index, mod_index):
        self.modlists[modlist_index].insertInput(mod_index)

    def insert_custom_mod(self, modlist_index, mod_index):
        self.modlists[modlist_index].insertCustomInput(mod_index)        

    def rightClickMenu(self, event, rc_menu):
        for modlist in self.modlists:
            modlist.selectTop()
        #initialize colors submenu
        colors_menu = Menu(self.master.master)
        #get clicked modlist index
        modlist_index = self.dynamic_nearest()
        mod_index = self._get_clicked_mod_index(modlist_index)
        #General modlist commands
        rc_menu.add_command(label='Insert Nexus Mod Here...',
                            command= lambda: self.insert_mod(modlist_index, mod_index))
        rc_menu.add_command(label='Insert Non-Nexus Mod Here...',
                            command= lambda: self.insert_custom_mod(modlist_index, mod_index))
        y = self._get_clicked_cat_index(modlist_index)
        rc_menu.add_command(label='Insert Category Here...',
                            command=lambda: self.insert_input(y))
        rc_menu.add_command(label='Insert Category At End...',
                            command=lambda: self.insert_input(END))
        #Adds the colors submenu menu
        if len(self.modlists[modlist_index].modlabel_list) > 0:
            rc_menu.add_separator()
            rc_menu.add_cascade(label='Change Mod Color To...',
                                menu=colors_menu)
            colors_menu.add_command(label='Default',
                                    command=lambda: \
                                    self.update_color(modlist_index,
                                                      mod_index,'#383838'))
            colors_menu.add_command(label='Red',
                                    command=lambda: \
                                    self.update_color(modlist_index,
                                                      mod_index, 'red'))
            colors_menu.add_command(label='Blue',
                                    command=lambda: \
                                    self.update_color(modlist_index,
                                                      mod_index, 'blue'))
            colors_menu.add_command(label='Green',
                                    command=lambda: \
                                    self.update_color(modlist_index,
                                                      mod_index, 'green'))
            colors_menu.add_command(label='Yellow',
                                    command=lambda: \
                                    self.update_color(modlist_index,
                                                      mod_index, 'yellow'))
            rc_menu.add_separator()
            #incompatibilities commands
            rc_menu.add_command(label='Manage Incompatibilities...',
                                command=lambda: \
                                self.manage_incomp(modlist_index, mod_index))
            if len(self.modlists[modlist_index].modlabel_list[mod_index].conflicts) > 0:
                rc_menu.add_command(label='View Conflicts',
                                    command=lambda: self.view_conflicts( \
                                        modlist_index, mod_index))
        rc_menu.add_separator()
        rc_menu.add_command(label='Rename Category',
                            command=lambda: self.rename(y))
        rc_menu.add_separator()
        rc_menu.add_command(label='Copy Mod Link', command=lambda:self.copyURL(modlist_index, mod_index))
        for modlist in self.modlists:
            if len(modlist.selected_modlabel_list) > 0:
                rc_menu.add_command(label='Open Selected Mod Links', command=self.openSelected)
                break
        rc_menu.add_command(label='Open All Mod Links in "{}"'.format(self.modlists[modlist_index].name),
                            command=lambda x=modlist_index:self.openAll(x))
        rc_menu.add_separator()
        rc_menu.add_command(label='Select All Mods', command=self.selectAll)
        rc_menu.add_separator()
        for i in range(len(self.modlists)):
            if self.modlists[i].is_entered_all:
                n = 0
                if i > 0:
                    rc_menu.add_command(label='Merge "'+self.modlists[i].name+'" Category Into Upper',
                                        command=lambda i=i:self.merge_up(i))
                    n += 1
                if i < len(self.modlists)-1:
                    rc_menu.add_command(label='Merge "'+self.modlists[i].name+'" Category Into Lower',
                                        command=lambda i=i:self.merge_down(i))
                    n+=1
                if n > 0:
                    rc_menu.add_separator()
                self.modlists[i].rightClickMenu(event, rc_menu)
        rc_menu.add_command(label='Remove All Mods', command=self.deleteAll)
        rc_menu.add_command(label='Remove "'+self.modlists[modlist_index].name+'" Category', command=lambda i=i: self.delete_confirm(i))
        #Selects and deselects appropriate mods
        for modlist in self.modlists:
            modlist.onClickEvent(event)

    def view_conflicts(self, modlist_index, mod_index):
        conflicts = self.modlists[modlist_index].modlabel_list[mod_index].conflicts
        ConflictListbox(self, conflicts)

    def copyURL(self, modlist_index, mod_index):
        self.master.master.clipboard_clear()
        self.master.master.clipboard_append(self.modlists[modlist_index].modlabel_list[mod_index].get_info()[0])

    def openAll(self, modlist_index):
        msgBox = messagebox.askquestion ('Opening All Mod Links',
                                         'Open all mod links in the "'+self.modlists[modlist_index].name+'" category in your default browser?',
                                         icon = 'warning')
        if msgBox == 'yes':
            self.modlists[modlist_index].open_all_links()

    def openSelected(self):
        for modlist in self.modlists:
            modlist.open_selected_links()

    def update_color(self, modlist_index, mod_index, color, state='normal'):
        self.modlists[modlist_index].modlabel_list[ \
            mod_index].update_color(color,state)

    def manage_incomp(self, modlist_index, mod_index):
        l = self.modlists[modlist_index].modlabel_list[mod_index].incompatibilities
        IncompatibilityManager(self, l)

    def _get_clicked_mod_index(self,modlist_index):
        '''return updated index if mouse is below the last mod in a given list'''
        modlist = self.modlists[modlist_index]
        mod_index = modlist.nearest()
        if modlist.listview:
            height = modlist.listview_height
        else:
            height = modlist.defaultview_height
        mouse_y = modlist.mlb_frame.winfo_pointery() - modlist.mlb_frame.winfo_rooty()
        if len(modlist.modlabel_list) > 1 and (height*mod_index+height) < mouse_y:
            return mod_index+1
        else:
            return mod_index

    def _get_clicked_cat_index(self, modlist_index):
        '''return updated index if mouse is below the last category'''
        modlist = self.modlists[modlist_index]
        height = modlist.winfo_height()
        mouse_y = self.winfo_pointery() - self.winfo_rooty()
        if (modlist.winfo_y()+modlist.winfo_height()) < mouse_y:
            return modlist_index+1
        else:
            return modlist_index
        

    def onDoubleClickEvent(self,event):
        for modlist in self.modlists:
            modlist.onDoubleClickEvent(event)

    def toggle_view(self):
        for modlist in self.modlists:
            modlist.toggle_view()

    def dynamic_nearest(self):
        '''get index of mod listbox nearest to the mouse y position.
        designed to work with widgets of variable sizes'''
        index = 0
        current_nearest_index = 0
        #get the absolute position of the mouse in relation to the ModlistListbox position
        mouse_y = self.winfo_pointery() - self.winfo_rooty()
        if len(self.modlists) > 1:
            #initialize y_maps, a list of 2-lengthed lists that store the
            #start and end y values of each modlist
            y_maps = []
            for i in range(len(self.modlists)):
                #populate heights
                modlist = self.modlists[i]
                #Set y-extending values
                if i == 0:
                    base = 0
                else:
                    base = y_maps[i-1][1]
                if modlist.listview:
                    mod_height = modlist.listview_height*len(modlist.modlabel_list)
                else:
                    mod_height = modlist.defaultview_height*len(modlist.modlabel_list)
                #set start and end values
                if modlist.is_collapsed:
                    y_maps.append([base, base+modlist.name_height])
                else:
                    y_maps.append([base, base+modlist.name_height+mod_height])
            for i in range(len(y_maps)):
                #find the index within the y mappings
                if y_maps[i][0] <= mouse_y < y_maps[i][1]:
                    index = i
        return index
