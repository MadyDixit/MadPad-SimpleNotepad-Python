from tkinter import *
import tkinter.filedialog
import os
import tkinter.messagebox
root = Tk()
root.title("MadPad")
root.geometry('350x350')

#FUNCTION
def cut():
	textpad.event_generate("<<Cut>>")
	update_line_number()

def undo():
	textpad.event_generate("<<Undo>>")
	update_line_number()

def redo():
	textpad.event_generate("<<Redo>>")
	update_line_number()

def copy():
	textpad.event_generate("<<Copy>>")
	update_line_number()

def paste():
	textpad.event_generate("<<Paste>>")
	update_line_number()

def select_all():
	textpad.tag_add('sel','1.0','end')
def on_find():
	t2 = Toplevel(root)
	t2.title('Find')
	t2.geometry('262x65+200+250')
	t2.transient(root)
	Label(t2,text = 'Find All:').grid(row = 0, column = 0, sticky = E)
	v = StringVar()
	e = Entry(t2, width = 25,textvariable = v).grid(row = 0, column = 1, pady = 2, padx = 2, sticky = EW)
	c=IntVar()
	Checkbutton(t2, text='Ignore Case', variable=c).grid(row=1, column=1, sticky='e', padx=2, pady=2)
	Button(t2, text = 'Find ALL',command=lambda: search_for(v.get(),c.get(), textpad, t2,e)).grid(row=0, column=2, sticky='e'+'w', padx=2, pady=2)
	def close_search():
		textpad.tag_remove('match', '1.0', END)
		t2.destroy()
	t2.protocol('WM_DELETE_WINDOW', close_search)#override close button


def search_for(needle,cssnstv, textpad, t2,e) :
        textpad.tag_remove('match', '1.0', END)
        count =0
        if needle:
                pos = '1.0'
                while True:
                    pos = textpad.search(needle, pos, nocase=cssnstv, stopindex=END)
                    if not pos: break
                    lastpos = '%s+%dc' % (pos, len(needle))
                    textpad.tag_add('match', pos, lastpos)
                    count += 1
                    pos = lastpos
                textpad.tag_config('match', foreground='red', background='yellow')
        t2.title('%d matches found' %count)

def open_file():
	global filename
	filename = tkinter.filedialog.askopenfilename(defaultextension = ".txt",filetype = [("All Files","."),("Text Documents","*.txt")])
	if filename == "":
		filename = None # Absence of file.
	else:
		root.title(os.path.basename(filename) + " - MADPad") #
	#Returning the basename of 'file'
		textpad.delete(1.0,END)
		fh = open(filename,"r")
		textpad.insert(1.0,fh.read())
		fh.close()
	update_line_number()

def save():
	global filename
	try:
		f = open(filename,'w')
		letter = textpad.get(1.0,'end')
		f.write(letter)
		f.close()
	except:
		save_as()

def save_as():
	try:
		f = tkFileDialog.asksaveasfilename(initialfile ='Untitled.txt', defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
		fh = open(f, 'w')
		textoutput = textPad.get(1.0, END)
		fh.write(textoutput)
		fh.close()
		root.title(os.path.basename(f) + " - MadPad")
	except:
		pass

def new():
	root.title("Untitled")
	global filename
	filename = None
	textpad.delete(1.0,END)
	update_line_number()

def about(event = None):
	tkinter.messagebox.showinfo("About","MadPad")

def help(event = None):
	tkinter.messagebox.showinfo("Help","MadPad:Create By Madhav")

def exit_editor(event=None):
	if tkinter.messagebox.askokcancel("Quit", "Do you really want to quit?"):
		root.destroy()
root.protocol('WM_DELETE_WINDOW', exit_editor) 

def update_line_number(event=None):
	txt = ''
	if showln.get():
		endline, endcolumn = textpad.index('end-1c').split('.')
		txt = '\n'.join(map(str, range(1, int(endline))))
	lnlabel.config(text=txt, anchor='nw')
def theme(event=None):
        global bgc,fgc
        val = themechoice.get()
        clrs = clrschms.get(val)
        fgc, bgc = clrs.split('.')
        fgc, bgc = '#'+fgc, '#'+bgc
        textpad.config(bg=bgc, fg=fgc)


#GUI
newicon = PhotoImage(file='icons/new_file.gif')
openicon = PhotoImage(file='icons/open_file.gif')
saveicon = PhotoImage(file='icons/Save.gif')
cuticon = PhotoImage(file='icons/Cut.gif')
copyicon = PhotoImage(file='icons/Copy.gif')
pasteicon = PhotoImage(file='icons/Paste.gif')
undoicon = PhotoImage(file='icons/Undo.gif')
redoicon = PhotoImage(file='icons/Redo.gif')
menubar = Menu(root)
filemenu = Menu(menubar, tearoff = 0)
filemenu.add_command(label = "New",accelerator = "Ctrl+N", compound = LEFT, image = newicon, underline = 0, command = new )
filemenu.add_command(label = "Open",accelerator = "Ctrl+O", compound = LEFT, image = openicon, underline = 0, command = open_file )
filemenu.add_command(label = "Save",accelerator = "Ctrl+S", compound = LEFT, image = saveicon, underline = 0 ,command = save)
filemenu.add_command(label = "Save As", accelerator = "Shift+Ctrl+S",command = save_as)
filemenu.add_separator()
filemenu.add_command(label = "Exit", accelerator = "Alt+F4",command = exit_editor)
menubar.add_cascade(label = "File", menu = filemenu)


editmenu = Menu(menubar, tearoff = 0)
editmenu.add_command(label = "Undo", accelerator = "Ctrl+Z", compound = LEFT, image = undoicon, underline = 0, command = undo)
editmenu.add_command(label = "Redo", accelerator = "Ctrl+Y",compound = LEFT, image = redoicon, underline = 0, command = redo)
editmenu.add_separator()
editmenu.add_command(label = "Cut",accelerator = "Ctrl+X",compound = LEFT,image = cuticon, underline = 0, command = cut)
editmenu.add_command(label = "Copy",accelerator = "Ctrl+C",compound = LEFT,image = copyicon, underline = 0, command = copy)
editmenu.add_command(label = "Paste",accelerator = "Ctrl+V",compound = LEFT,image = pasteicon, underline = 0,command = paste)
editmenu.add_separator()
editmenu.add_command(label = "Find", accelerator = "Ctrl+F",command = on_find)
editmenu.add_separator()
editmenu.add_command(label = "Select All", accelerator = "Ctrl+A", command = select_all)
menubar.add_cascade(label = "Edit", menu = editmenu)

'''
viewmenu = Menu(menubar, tearoff = 0)
showln = IntVar()
showln.set(1)
viewmenu.add_checkbutton(label = "Show Line Number", variable = showln,command = update_line_number)
showin = IntVar()
showin.set(1)
viewmenu.add_checkbutton(label = "Show Info bar at bottom", variable = showin)
htln = IntVar()
viewmenu.add_checkbutton(label = "Highliht the Current Line", variable = htln)
themesmenu = Menu(menubar, tearoff=0)
viewmenu.add_cascade(label="Themes", menu=themesmenu)
clrschms = {
'1. Default White': 'FFFFFF',
'2. Greygarious Grey':'D1D4D1',
'3. Lovely Lavender':'E1E1FF' , 
'4. Aquamarine': 'D1E7E0',
'5. Bold Beige': 'FFF0E1',
'6. Cobalt Blue':'333AA',
'7. Olive Green': '5B8340',
}
themechoice= StringVar()
themechoice.set('1. Default White')
for k in sorted(clrschms):
    themesmenu.add_radiobutton(label=k, variable=themechoice,command = theme)


menubar.add_cascade(label = "View", menu = viewmenu)
'''

aboutmenu = Menu(menubar, tearoff = 0)
aboutmenu.add_command(label ="Help",command = help)
aboutmenu.add_command(label = "About",command = about)
menubar.add_cascade(label = "About", menu = aboutmenu)


shortcut = Frame(root, height = 25, bg = "light sea green")
shortcut.pack(expand = NO, fill = X)
lnlabel = Label(root,  width=5,  bg = 'antique white')
lnlabel.pack(side=LEFT, anchor='nw', fill=Y)



textpad = Text(root)
textpad.pack(expand = YES, fill = BOTH)

scroll = Scrollbar(textpad)
textpad.config(yscrollcommand = scroll.set)
scroll.config(command = textpad.yview)
scroll.pack(side = RIGHT, fill = Y)

root.config(menu = menubar)
#

root.mainloop()