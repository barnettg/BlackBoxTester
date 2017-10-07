import tkinter as Tk
from tkinter import ttk

 
class Model():
 
    def __init__(self):
        self.xpoint=200
        self.ypoint=200
        self.res = None
  
  
    def calculate(self):
        pass

 
class View():
    def __init__(self, master):
        content = ttk.Frame(master) # not used

        # get screen size
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        # set min size to 70%
        frameWidth = int(screen_width * 7 /10)
        frameHeight = int(screen_height * 7 /10)
        
        master.minsize(width = frameWidth, height = frameHeight)

        # place in center of screen
        # calculate position x and y coordinates
        x = (screen_width/2) - (frameWidth/2)
        y = (screen_height/2) - (frameHeight/2)
        master.geometry('%dx%d+%d+%d' % (frameWidth, frameHeight, x, y))

        #menubar
        self.menus = Menus(master)

        # top panel
        self.topPanel=TopPanel(master)

        # center tabbed notebooks
        self.centerPanel=CenterPanel(master)

        # bottom panel
        self.bottompanel=BottomPanel(master)

        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=0)
        master.rowconfigure(1, weight=1)
        master.rowconfigure(2, weight=0)
        print ("grid size " + str(master.grid_size()) )

class Menus():
    def __init__(self, root):
        self.menubar = Tk.Menu(root) # frame that holds the menu buttons
        # Create File menu
        self.filemenu = Tk.Menu(self.menubar, tearoff=0 )
        self.filemenu.add_command(label="Exit", accelerator='Alt+F4')
        # all file menu choices will be placed here
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # Create About menu
        self.aboutmenu = Tk.Menu(self.menubar, tearoff=0)
        self.aboutmenu.add_command(label="About")
        self.aboutmenu.add_command(label="Help")
        self.menubar.add_cascade(label="About", menu=self.aboutmenu)

        # Displaying menu on top of root.
        root.config(menu=self.menubar)


class CenterPanel():
    def __init__(self, root):
        panedwin = Tk.PanedWindow(root, sashwidth=6, sashrelief=Tk.RAISED, borderwidth =10, handlesize=10, orient=Tk.HORIZONTAL)
        nbLeft = ttk.Notebook(panedwin)
        scriptsTab(nbLeft)
        portsTab(nbLeft)
        #page1Left = self.page1_left(nbLeft) #ttk.Frame(nbLeft)
        #nbLeft.add(page1Left, text='tab1')
        #self.addTabsLeft(nbLeft)
        panedwin.add(nbLeft)

        nbRight = ttk.Notebook(panedwin)
        page1Right = ttk.Frame(nbRight)
        nbRight.add(page1Right, text='tab1')
        panedwin.add(nbRight)

        panedwin.grid(row=1,column=0, rowspan=20,sticky=(Tk.N, Tk.S, Tk.E, Tk.W)) #

    # def addTabsLeft(self, root):
    #     page1Left = self.page1_left(root) #
    #     root.add(page1Left, text='Scripts')
    #     #page2Left = self.page2_left(root) #
    #     #root.add(page2Left, text='Com Ports')
    #     pass
    #
    # def page1_left(self, root):
    #     page1Left = ttk.Frame(root)
    #     return page1Left
    #
    # def page2_left(self, root):
    #     page2Left = ttk.Frame(root)
    #     return page2Left

class scriptsTab():
    def __init__(self, root):
        tab = ttk.Frame(root, relief="sunken", borderwidth=1)#, width=200, height=100)
        frame = ttk.Frame(tab, relief="sunken", borderwidth=1)#, width=200, height=100 )
        frame.pack(side=Tk.TOP, expand=Tk.YES, fill=Tk.BOTH)
        #frame.grid(row=0,column=0,sticky=(Tk.N, Tk.S, Tk.E, Tk.W)) #
        #Tk.Grid.columnconfigure(frame, 0, weight=1)

        tree = ttk.Treeview(frame)
        tree.pack(side=Tk.TOP, expand=Tk.YES, fill=Tk.BOTH, anchor =Tk.NW)#

        # bottom frame
        bottomFrame = ttk.Frame(frame, relief="sunken", borderwidth=5)#, width=200, height=100)
        timeLabel = Tk.Label(bottomFrame, text="Time Estimate: ")
        timeLabel.grid(row=0,column=0, columnspan = 2,sticky=(Tk.E))
        self.SaveBtn = Tk.Button(bottomFrame, text="test ")
        self.SaveBtn.grid(row=0,column=2)

        bottomFrame.pack(side=Tk.BOTTOM, expand=Tk.YES, fill=Tk.X, anchor =Tk.SE)


        #self.But = Tk.Button(frame, text="test ")
        #self.But.pack(side="top")
        root.add(tab, text='Scripts')
        pass

class portsTab():
    def __init__(self, root):
        tab = ttk.Frame(root, relief="sunken", borderwidth=1, width=100, height=100)
        frame = Tk.Frame( tab, relief="sunken", borderwidth=1)#, width=200, height=100 )
        frame.pack(side=Tk.TOP, expand=Tk.YES, fill=Tk.BOTH)

        topframe = Tk.Frame( frame, relief="sunken", borderwidth=1)#, width=200, height=100 )
        topframe.pack(side=Tk.TOP, expand=Tk.YES, fill=Tk.BOTH)

        self.portAddBtn = Tk.Button(topframe, text="Add Port...")
        self.portAddBtn.pack(side="left", anchor =Tk.W, padx=5, pady=5)

        self.portDelBtn = Tk.Button(topframe, text="Delete Port")
        self.portDelBtn.pack(side="right", anchor =Tk.E, padx=5, pady=5)

        ports = Tk.Listbox(frame, width=100, height=100)
        ports.pack(side=Tk.TOP, expand=Tk.NO, fill=Tk.BOTH, anchor =Tk.NW, padx=5, pady=5)

        root.add(tab, text='Com Ports')
        pass

        
class TopPanel():
    def __init__(self, root):
        self.frame3 = Tk.Frame( root, relief="sunken", borderwidth=5, width=200, height=100 )
        self.frame3.grid(row=0,column=0, sticky=(Tk.N, Tk.S, Tk.E, Tk.W)) #
        self.topBut = Tk.Button(self.frame3, text="Plot ")
        self.topBut.pack(side="top")#,fill=Tk.BOTH)

        
class BottomPanel():
    def __init__(self, root):
        self.frame2 = Tk.Frame( root , relief="sunken", borderwidth=5)#, width=200, height=100)
        self.frame2.grid(row=21,column=0, sticky=(Tk.N, Tk.S, Tk.E, Tk.W)) #
        self.plotBut = Tk.Button(self.frame2, text="Plot ")
        self.plotBut.pack(side="top",fill=Tk.BOTH)
        self.clearButton = Tk.Button(self.frame2, text="Clear")
        self.clearButton.pack(side="top")#,fill=Tk.BOTH)
  
class Controller():
    def __init__(self):
        self.root = Tk.Tk()
        self.model=Model()
        self.view=View(self.root)
        #self.view.sidepanel.plotBut.bind("<Button>",self.my_plot)
        #self.view.sidepanel.clearButton.bind("<Button>",self.clear)
  
    def run(self):
        self.root.title("Tkinter MVC example")
        self.root.deiconify()
        self.root.mainloop()
         
    def clear(self,event):
        pass
  
    def my_plot(self,event):
        pass
  
 
 
if __name__ == '__main__':
    c = Controller()
    c.run()
