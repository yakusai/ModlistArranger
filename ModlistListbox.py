from tkinter import *
from tkinter import messagebox
from ModLabel import ModLabel
from operator import itemgetter
from ordered_set import OrderedSet
from tkinter.simpledialog import askstring
import webbrowser
import os
#custom imports
from TagLabel import TagLabel
from CustomModMessageBox import CustomModMessageBox
from ParseURL import ParseURL
#parsing imports
from urllib.parse import urlparse
import validators
import requests
from bs4 import BeautifulSoup
        

class ModlistListbox(Frame):
    def __init__(self, parent, listview=False, name='Mods'):
        Frame.__init__(self, parent, bg='#2d2d2d')
        self.mod_list = []
        self.modlabel_list = []
        self.selected_modlabel_list = OrderedSet([])
        self.listview = listview
        self.listview_height = 29
        self.defaultview_height = 68
        self.name_height = 35
        self.current_index = None
        #category selection variables
        self.is_top_entered = False
        self.is_top_selected = False
        #collapse variable
        self.is_collapsed = False
        #enter variable
        self.is_entered_all = False
        #create mod listbox frame
        self.mlb_frame = Frame(self)
        #naming initalization
        self.name = name
        self.name_label = TagLabel(self, bordercolor='#666666', size=12,
                                   font=('roboto',16,'bold'), text=self.name,
                                   bg='#444444', fg='#f0f0f0', borderwidth=4,
                                   relief='flat')
        #limit the minimum size of name label
        if self.name_label.label.winfo_reqwidth() < 205:
            self.name_label.label.configure(width=15)
        #enter and leave events
        self.name_label.bind('<Enter>', self.on_enter_top)
        self.name_label.bind('<Leave>', self.on_leave_top)
        self.bind('<Enter>', self.on_enter_all)
        self.bind('<Leave>', self.on_leave_all)
        #lay out the name frame and mod listbox frame
        self.name_label.pack(side='top', fill='y', anchor='sw', padx=10)
        self.mlb_frame.pack(side='bottom', fill='both', expand=True)
        self.mlb_frame.grid_columnconfigure(0,weight=1)
        self.update_idletasks()

    def update_name(self, name):
        self.name = name
##        self.name_label.update_text(name)
        #resizing a pre-existing TagLabel isn't working when changing text
        #so just make a new one 4Head
        new_name = TagLabel(self, bordercolor='#666666', size=12,
                               font=('roboto',16,'bold'), text=name,
                               bg='#444444', fg='#f0f0f0', borderwidth=4,
                               relief='flat')
        self.name_label.pack_forget()
        self.name_label.destroy()
        self.name_label = new_name
        self.name_label.pack(side='top', fill='y', anchor='sw', padx=10)
        if self.name_label.label.winfo_reqwidth() < 205:
            self.name_label.label.configure(width=15)

    def get_name(self):
        return self.name

    def toggle_collapse(self):
        '''Collapses or expands the mod listbox'''
        if len(self.modlabel_list) > 0:
            if self.is_collapsed:
                self.force_expand()
            else:
                self.force_collapse()
            self.update_idletasks()

    def force_collapse(self):
        if len(self.modlabel_list) > 0:
            for mod in self.modlabel_list:
                mod.grid_remove()
                self.mlb_frame.configure(height=1)
            self.is_collapsed = True
            self.name_label.configure(bg='white')

    def force_expand(self):
        if len(self.modlabel_list) > 0:
            for mod in self.modlabel_list:
                mod.grid()
            self.is_collapsed = False
            self.name_label.configure(bg='#666666')

    def insert(self, index, info):
        '''inserts a mod at the given index, and with the given info'''
        if index == END or index > len(self.mod_list):
            index = len(self.mod_list)
        mod_label = ModLabel(self.mlb_frame, info=info, index=index,
                             listview=self.listview)
        #Try to update the new indices. Fails if from an older mod
        try:
            mod_label.update_color(info[6])
            mod_label.incompatibilities = info[7]
        except IndexError:
            pass
        self.mod_list.insert(index, info)
        self.modlabel_list.insert(index,mod_label)
        if len(self.mod_list) > index:
            for x in range(index,len(self.mod_list)):
                self.modlabel_list[x].update_index(x)
                self.modlabel_list[x].grid(row=x, column=0, sticky='nsew')
        else:
            mod_label.grid(row=len(self.mod_list), column=0, sticky='nsew')
        if self.is_collapsed:
            self.force_expand()

    def delete(self, index):
        '''Delete a mod at the given index'''
        if index == END:
            index = len(self.mod_list)-1
        if index<len(self.mod_list)-1:
            for x in range(index,len(self.mod_list)-1):
                self.modlabel_list[x+1].grid(row=x, column=0, sticky='nsew')
                self.modlabel_list[x+1].update_index(x)
        if self.modlabel_list[index] in self.selected_modlabel_list:
            self.selected_modlabel_list.remove(self.modlabel_list[index])
        self.modlabel_list[index].grid_forget()
        self.modlabel_list[index].destroy()
        del self.mod_list[index]
        del self.modlabel_list[index]
        if len(self.modlabel_list) == 0:
            self.mlb_frame.configure(height=1)
        if self.is_collapsed:
            self.force_expand()
            #Quick fix for a category not properly expanding if last mod deleted
            self.is_collapsed = False
            self.name_label.configure(bg='#666666')

    def delete_selected(self):
        for x in range(len(self.selected_modlabel_list)):
            self.delete(self.selected_modlabel_list[0].get_index())

    def delete_all_confirm(self):
        msgBox = messagebox.askquestion ('Removing All',
                                         'Remove all mods from the '+self.name+' Category?',
                                         icon = 'warning')
        if msgBox == 'yes':
            self.delete_all()

    def delete_all(self):
        '''deletes all mods from the list'''
        for x in range(len(self.modlabel_list)):
            self.delete(0)
        #Quick fix for a category not properly expanding if last mod deleted
        self.is_collapsed = False
        self.name_label.configure(bg='#666666')

    def open_link(self, modlabel):
        webbrowser.open_new(modlabel.get_info()[0])

    def open_selected_links(self):
        for mod in sorted(self.selected_modlabel_list,
                          key=lambda x: x.get_index()):
            self.open_link(mod)

    def open_all_links(self):
        for mod in self.modlabel_list:
            self.open_link(mod)

    def get_size(self):
        return len(self.modlabel_list)

    def get_all_info(self):
        '''return a list of lists of all mod info'''
        l = []
        for mod in self.modlabel_list:
            l.append(mod.get_info())
        return l

    def get_info(self,index):
        '''return a list of the mod info at the given index'''
        return self.modlabel_list[index].get_info()

    def get_height(self):
        return len(self.modlabel_list)
    
    def toggle_view(self):
        for mod in self.modlabel_list:
            mod.toggle_view()
        self.listview = not self.listview

    def force_listview(self):
        for mod in self.modlabel_list:
            mod.display_listview()
        self.listview = True

    def force_defaultview(self):
        for mod in self.modlabel_list:
            mod.display_default()
        self.listview = False

    def on_enter_top(self, event):
        '''event to determine if the list's category title is focused'''
        self.is_top_entered = True

    def on_leave_top(self, event):
        self.is_top_entered = False

    def on_enter_all(self, event):
        self.is_entered_all = True

    def on_leave_all(self, event):
        self.is_entered_all = False

    #====Right Click Menu Functionality

    def rightClickMenu(self,event,rc_menu):
        for mod in self.modlabel_list:
            if mod.is_focused:
                #If the mod clicked is not selected, select it
                if mod not in self.selected_modlabel_list:
                    self.onClickEvent(event)
##                rc_menu.add_command(label='Select',
##                                    command=lambda mod=mod: self.rightClickSelect(mod))
##                rc_menu.add_command(label='Select All Mods in "'+self.name+'" Category',
##                                    command=self.selectAll)
##                rc_menu.add_separator()
##                rc_menu.add_separator()
##                rc_menu.add_command(label='Remove',
##                                    command=lambda mod=mod: self.delete(mod.get_index()))
##                if len(self.selected_modlabel_list) > 0:
##                    rc_menu.add_command(label='Remove Selected',
##                                        command=self.delete_selected)
##                if len(self.modlabel_list) > 0:
##                    rc_menu.add_command(label='Remove All Mods In "'+self.name+'" Category',
##                                        command=self.delete_all_confirm)

    def insertInput(self, index):
        url = askstring('New Mod at Index '+str(index+1),'Input Nexus URL')
        info = None
        if(url is not None):
            info = ParseURL.parse_nexus_url(url)
        if info is not None:
            self.insert(index, info)

    def insertCustomInput(self, index):
        info = []
        CM = CustomModMessageBox(self,'New Mod at Index '+str(index+1),info)
        if info != []:
            self.insert(index, info)


    #====Selection Functionality====


    def onClickEvent(self,event):
        deselect_others = True
        self._check_descs()
        if len(self.modlabel_list) > 0:
            #if clicked mod is already part of selection, prevents the deselection of other mods
            for x in range(len(self.modlabel_list)):
                if self.modlabel_list[x].is_index_focused and self.modlabel_list[x].is_selected:
                    deselect_others = False
                    self.current_index = x
            if deselect_others:
                #checks every modlabel to see if any are selected
                for x in range(len(self.modlabel_list)):
                    self.modlabel_list[x].select()
                    #code for multi-selection capabilities
                    if self.modlabel_list[x].is_selected and self.modlabel_list[x] not in self.selected_modlabel_list:
                        #adds selected modlabels to the selected modlabels list
                        self.current_index = x
                        self.selected_modlabel_list.append(self.modlabel_list[x])
                    elif not self.modlabel_list[x].is_selected and self.modlabel_list[x] in self.selected_modlabel_list:
                        #removes deselected modlabels from the selected modlabels list
                        self.selected_modlabel_list.remove(self.modlabel_list[x])

    def _check_descs(self):
        '''checks whether mouse is over a mod description or not'''
        #Get widget type under mouse
        x,y = self.winfo_pointerxy()
        widget = self.winfo_containing(x,y)
        for mod in self.modlabel_list:
            if widget is not mod.description:
                mod.disable_desc_edit()
            else:
                mod.enable_desc_edit()
        

    def onDoubleClickEvent(self, event):
        if self.is_top_entered and len(self.modlabel_list) > 0:
            self.toggle_collapse()
                            
    def onShiftClickEvent(self,event):
        #code for multi-selection
        if len(self.selected_modlabel_list) > 0:
            #set original index to start multi-selection from
            origin=self.selected_modlabel_list[-1].get_index()
            for x in range(len(self.modlabel_list)):
                # checks every modlabel for a valid multi-selection activation
                if self.modlabel_list[x].is_index_focused:
                    #checks whether the index of the target modlabel is above
                    #or below origin, then multi-selects accordingly
                    if (x - origin) > 0:
                        for y in range(origin,x+1):
                            self.selected_modlabel_list.append(self.modlabel_list[y])
                            self.modlabel_list[y].force_select()
                    elif (x - origin) < 0:
                        for y in range(x, origin):
                            self.selected_modlabel_list.append(self.modlabel_list[y])
                            self.modlabel_list[y].force_select()

    def rightClickSelect(self, mod_index):
        mod = self.modlabel_list[mod_index]
        self.deselectAll()
        mod.force_select()
        self.selected_modlabel_list.append(mod)

    def selectAll(self):
        '''Selects all the mods'''
        if len(self.modlabel_list) > 0:
            for mod in self.modlabel_list:
                self.selected_modlabel_list.append(mod)
                mod.force_select()

    def deselectAll(self):
        if len(self.selected_modlabel_list) > 0:
            for mod in self.selected_modlabel_list:
                mod.force_deselect()
            self.selected_modlabel_list.clear()

    def selectTop(self):
        if self.is_top_entered:
            self.forceSelectTop()
        else:
            self.forceDeselectTop()

    def forceSelectTop(self):
        self.is_top_selected = True
        self.name_label.label.configure(bg='#f0f0f0', fg='#444444')

    def forceDeselectTop(self):
        self.is_top_selected = False
        self.name_label.label.configure(bg='#444444', fg='#f0f0f0')

    def is_top_selected(self):
        return self.is_top_selected
        

    #====Drag and Drop Functionality====

    def moveSelectionUp(self):
        '''Goes through the selected mods and moves them up by 1'''
        if len(self.selected_modlabel_list) > 0:
            for mod in self.selected_modlabel_list:
                #if mod at upper limit, don't move anything
                if mod.get_index() == 0:
                    return -1
            #sorts selected mods using the index as the key, then iterates
            for mod in sorted(self.selected_modlabel_list,
                              key=lambda x: x.get_index()):
                modtomove_data = self.modlabel_list[mod.get_index()-1].get_info()
                modtomove_index = mod.get_index()-1
                self.delete(modtomove_index)
                self.insert(modtomove_index+1,modtomove_data)

    def moveSelectionDown(self):
        '''Goes through the selected mods and moves them down by 1'''
        if len(self.selected_modlabel_list) > 0:
            for mod in self.selected_modlabel_list:
                #if mod at lower limit, don't move anything
                if mod.get_index() == len(self.modlabel_list)-1:
                    return 1
            #sorts selected mods using the index as the key, then iterates
            for mod in sorted(self.selected_modlabel_list,
                              key=lambda x: x.get_index(), reverse=True):
                modtomove_data = self.modlabel_list[mod.get_index()+1].get_info()
                modtomove_index = mod.get_index()+1
                self.delete(modtomove_index)
                self.insert(modtomove_index-1,modtomove_data)


    def dragSelection(self, event):
        '''Moves all selected ModLabels up or down depending on
        mouse movement while the mouse is held'''
        i = self.nearest()
        if self.current_index is not None:
            if i < self.current_index and i != -1:
                self.moveSelectionUp()
                self.current_index = i
            elif i > self.current_index and i != len(self.modlabel_list):
                self.moveSelectionDown()
                self.current_index = i
        return i

    def nearest(self):
        '''get index of ModLabel item nearest to the mouse y position
        using hardcoded ModLabel heights'''
        index = 0
        current_nearest_index = 0
        #get the correct height of the ModLabels
        if self.listview:
            height = self.listview_height
        else:
            height = self.defaultview_height
        #get the absolute position of the mouse in relation to the ModlistListbox position
        mouse_y = self.mlb_frame.winfo_pointery() - self.mlb_frame.winfo_rooty()
        if len(self.modlabel_list) > 0:
            current_index = 0
            distance_from_current = abs((height/2) - mouse_y)
            for i in range(len(self.modlabel_list)):
                distance_from_next = abs((i * height + (height/2)) - mouse_y)
                if distance_from_current > distance_from_next:
                    distance_from_current = distance_from_next
                    current_index = i
            #if going beyond the list, return an index beyond the list to signify it moving into a different category
##            if(current_index = 
            index = current_index
        return index

                
    #====Code that doesn't fuckin' work====

    '''NOTES: This nearest() is based off of each widget's actual position on the board. It bugs out when a mod is
    inserted into the modlist, causing it to return the wrong index. For example, if you were to insert a mod at
    index 2 while your mouse is at index 2, instead of continuing to return index 2 as the nearest index, it will
    return index 3, or sometimes even 4 if the modlist is that large.'''

##    def nearest(self):
##        '''get index of ModLabel item nearest to the mouse y position.
##        designed to work with widgets of variable sizes'''
##        index = -1
##        current_nearest_index = 0
##        #get the absolute position of the mouse in relation to the ModlistListbox position
##        mouse_y = self.winfo_pointery() - self.winfo_rooty()
##        if len(self.modlabel_list) > 1:
##            #get the distance from the first widget
##            center_of_current = self.modlabel_list[0].winfo_y() + self.modlabel_list[0].winfo_height() / 2
##            distance_from_current = abs(center_of_current - mouse_y)
##            for i in range(1,len(self.modlabel_list)):
##                #get the distance from the next widget to compare
##                center_of_next = self.modlabel_list[i].winfo_y() + self.modlabel_list[i].winfo_height() / 2
##                distance_from_next = abs(center_of_next - mouse_y)
##                if distance_from_current > distance_from_next:
##                    #if the next widget is closer, set it to be the current widget, then set this widget's index as the current nearest
##                    distance_from_current = distance_from_next
##                    current_nearest_index = i
##            #set the final index
##            index = current_nearest_index
##        elif len(self.modlabel_list) == 1:
##            index = 0
##        return index
