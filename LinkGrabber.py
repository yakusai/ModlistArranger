from tkinter import *
from urllib.parse import urlparse
from ToolTips import CreateToolTip
from collections import *
from ParseURL import ParseURL
import validators

class LinkGrabber(Toplevel):
    def __init__(self, parent, info_list, nexus=False, font='roboto', fg='#f0f0f0', bg='#444444', bg2='#2d2d2d', *args, **kwargs):
        Toplevel.__init__(self, bg=bg2, takefocus=True, *args,**kwargs)
        self.grab_set()
        self.geometry('500x300')
        self.title('Link Grabber')
        self.nexus = nexus
        self.last_content = ''
        self.text = Text(self, font=font, bg=bg, fg=fg, insertbackground='white')
        tiptext = 'Links will automatically be grabbed whenever you copy a ' \
                  'URL to your clipboard while this window is open. '
        if nexus:
            tiptext += 'ONLY Nexus links will be accepted and used as input.'
        else:
            tiptext += 'ANY link will be accepted and used as input. '
        tiptext += 'Duplicate links will be removed.'
        self.tooltip = CreateToolTip(self.text, tiptext, waittime = 0)
        self.b1 = Button(self, font=font, bg=bg, fg=fg, text='Insert', command=lambda:self.insert(info_list))
        self.b2 = Button(self, font=font, bg=bg, fg=fg, text='Cancel', command=self.destroy)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.text.grid(row=0,column=0, columnspan=2, sticky='nsew', padx=20,pady=(10,0))
        self.b1.grid(row=1, sticky='e',padx=5, ipadx=20, pady=5)
        self.b2.grid(row=1,column=1, sticky='w', padx=5, ipadx=20, pady=5)
        #binds
        self.after('100', self.grab)
        #Center the window
        self.update_idletasks()
        x = (self.master.winfo_width()/2) + self.master.winfo_x() - (self.winfo_width()/2)
        y = (self.master.winfo_height()/2) + self.master.winfo_y() - (self.winfo_height()/2)
        self.geometry('+{}+{}'.format(int(x),int(y)))
        #Prevent code execution from parent until this window closes
        self.wait_window()
    
    def grab(self):
        try:
            content = self.clipboard_get()
            if content != self.last_content and validators.url(content):
                self.last_content = content
                self.text.insert(END, content+'\n')
        except TclError:
            pass
        self.after(100, self.grab)

    def insert(self, info_list):
        text = self.text.get('1.0', END)
        urls = text.splitlines()
        urls[:] = [x for x in urls if x != '']
        #Makes sure Nexus mods are correctly stripped
        for i in range(len(urls)):
            urls[i] = self.strip_nexus_mod(urls[i])
        infos = []
        if self.nexus:
            #Adds the information of only Nexus mods to the list
            for url in urls:
                info = ParseURL.parse_nexus_url(url, warning=False)
                if info is not None:
                    info_list.append(info)
        else:
            #Adds all the obtained urls to the list
            info_list += urls
        #Remove duplicates from the list
        info_list[:] = self.remove_dupes(info_list)
        self.destroy()

    def remove_dupes(self, a_list):
        seen = set()
        seen_add = seen.add
        return [x for x in a_list if not (x in seen or seen_add(x))]

    def strip_nexus_mod(self, url):
        '''if a url is found to be a Nexus mod url, returns its base url'''
        parsed_url = urlparse(url)
        hostsite = parsed_url.netloc
        protoc = parsed_url.scheme
        try:
            category = parsed_url.path.split('/')[2]
        except:
            return url
        if protoc not in ['https','http']:
            return url
        elif hostsite not in ['nexusmods.com','www.nexusmods.com']:
            return url
        elif category != 'mods':
            return url
        else:
            return url.split('?')[0]
                
#testing  
if __name__ == '__main__':
    root = Tk()
    l = []
    b = Button(root, text='E', command = lambda : LinkGrabber(root, l))
    b.pack()
    root.mainloop()
