import tkinter as Tk
from tkinter import ttk
 
class View():
    def __init__(self):
        #root.update_idletasks()
        self.master = Tk.Tk()
        content = ttk.Frame(self.master) # not used

        # get screen size
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        # set min size to 70%
        frameWidth = int(screen_width * 7 /10)
        frameHeight = int(screen_height * 7 /10)
        
        self.master.minsize(width = frameWidth, height = frameHeight)

        # place in center of screen
        # calculate position x and y coordinates
        x = (screen_width/2) - (frameWidth/2)
        y = (screen_height/2) - (frameHeight/2)
        self.master.geometry('%dx%d+%d+%d' % (frameWidth, frameHeight, x, y))

        #menubar
        self.menus = Menus(self.master)

        # top panel
        self.topPanel=TopPanel(self.master)

        # center tabbed notebooks
        self.centerPanel=CenterPanel(self.master)

        # bottom panel
        self.bottompanel=BottomPanel(self.master)

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=0)
        self.master.rowconfigure(1, weight=1)
        self.master.rowconfigure(2, weight=0)
        print ("grid size " + str(self.master.grid_size()))

    def run(self):
        self.master.title("Black Box Tester")
        self.master.deiconify()
        self.master.mainloop()

class Menus():
    def __init__(self, root):
        self.menubar = Tk.Menu(root) # frame that holds the menu buttons

        # Create File menu
        self.fileMenu = Tk.Menu(self.menubar, tearoff=0 )
        self.fileMenu.add_command(label="Exit", accelerator='Alt+F4', command=self.exitMenu)
        # all file menu choices will be placed here
        self.menubar.add_cascade(label="File", menu=self.fileMenu)

        # Create Project menu
        self.projectMenu = Tk.Menu(self.menubar, tearoff=0)
        self.projectMenu.add_command(label="New", command=self.newProject)
        self.projectMenu.add_command(label="Open", command=self.openProject)
        self.projectMenu.add_command(label="Save", command=self.saveProject)
        self.projectMenu.add_command(label="Save As", command=self.saveProjectAs)
        self.projectMenu.add_command(label="Close", command=self.closeProject)
        self.projectMenu.add_separator()
        self.projectMenu.add_command(label="Open Configuration", command=self.openConfiguration)
        self.projectMenu.add_command(label="Save Configuration", command=self.saveConfiguration)
        self.projectMenu.add_command(label="Save Configuration AS", command=self.saveConfigurationAs)
        self.menubar.add_cascade(label="Project", menu=self.projectMenu)

        # Create Tests menu
        self.testsMenu = Tk.Menu(self.menubar, tearoff=0)
        self.testsMenu.add_command(label="Show Communications Window", command=self.testsShoeCommWin)
        self.testsMenu.add_command(label="Show Message Window", command=self.testsShowMessageWin)
        self.testsMenu.add_separator()
        self.testsMenu.add_command(label="Start", command=self.testsStart)
        self.testsMenu.add_command(label="Stop", command=self.testsStop)
        self.testsMenu.add_command(label="Pause", command=self.testsPause)
        self.testsMenu.add_command(label="Continue", command=self.testsContinue)
        self.testsMenu.add_separator()
        self.testsMenu.add_command(label="Save Report", command=self.testsSaveReport)
        self.menubar.add_cascade(label="Tests", menu=self.testsMenu)


        # Create About menu
        self.aboutMenu = Tk.Menu(self.menubar, tearoff=0)
        self.aboutMenu.add_command(label="About", command=self.showAbout)
        self.aboutMenu.add_command(label="Manual", command=self.showManual)
        self.menubar.add_cascade(label="About", menu=self.aboutMenu)

        # Displaying menu on top of root.
        root.config(menu=self.menubar)

    def exitMenu(self):
        print("Exit Menu")

    def showAbout(self):
        print("About Menu")

    def showManual(self):
        print("Manual Menu")

    def newProject(self):
        print("newProject Menu")

    def openProject(self):
        print("openProject Menu")

    def saveProject(self):
        print("saveProject Menu")

    def saveProjectAs(self):
        print("saveProjectAs Menu")

    def closeProject(self):
        print("closeProject Menu")

    def openConfiguration(self):
        print("openConfiguration Menu")

    def saveConfiguration(self):
        print("saveConfiguration Menu")

    def saveConfigurationAs(self):
        print("saveConfigurationAs Menu")


    def testsShoeCommWin(self):
        print("testsShoeCommWin Menu")

    def testsShowMessageWin(self):
        print("testsShowMessageWin Menu")

    def testsStart(self):
        print("testsStart Menu")

    def testsStop(self):
        print("testsStop Menu")

    def testsPause(self):
        print("testsPause Menu")

    def testsContinue(self):
        print("testsContinue Menu")

    def testsSaveReport(self):
        print("testsSaveReport Menu")

class CenterPanel():
    def __init__(self, root):
        panedwin = Tk.PanedWindow(root, sashwidth=6, sashrelief=Tk.RAISED, borderwidth=10, handlesize=10, orient=Tk.HORIZONTAL)
        nbLeft = ttk.Notebook(panedwin)
        self.scriptstab = scriptsTab(nbLeft)
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

        # bottom frame---------------------------------------------------------------
        bottomFrame = ttk.Frame(frame, relief="sunken", borderwidth=5)#
        frameA = ttk.Frame(bottomFrame, relief="sunken", borderwidth=5)#
        frameA1 = ttk.Frame(frameA, relief="sunken", borderwidth=5)#
        frameA2 = ttk.Frame(frameA, relief="sunken", borderwidth=5)#
        frameA1.pack(side=Tk.TOP, expand=Tk.YES, fill=Tk.X, anchor =Tk.NW)
        frameA2.pack(side=Tk.BOTTOM, expand=Tk.YES, fill=Tk.X, anchor =Tk.SW)
        frameA.pack(side=Tk.LEFT, expand=Tk.YES, fill=Tk.X, anchor =Tk.NW)

        frameB = ttk.Frame(bottomFrame, relief="sunken", borderwidth=5)#
        frameB.pack(side=Tk.RIGHT)#, expand=Tk.YES, fill=Tk.X, anchor =Tk.SW)
        #A1
        self.timeLabel = Tk.Label(frameA1, text="Time Estimate: ")
        self.timeLabel.pack(side=Tk.LEFT, anchor =Tk.W)
        #A2
        self.checkboxVar1 = Tk.IntVar()
        self.IgnoreCheckbox = Tk.Checkbutton(frameA2, text="Ignore type >", variable=self.checkboxVar1)
        self.IgnoreCheckbox.pack(side=Tk.LEFT, anchor =Tk.W)
        self.levelSpin = Tk.Spinbox(frameA2, from_=1, to=10, width=3)
        self.levelSpin.pack(side=Tk.LEFT, anchor =Tk.W)
        #B
        #timeLabel.grid(row=0,column=0, columnspan = 2,sticky=(Tk.E))
        self.SaveBtn = Tk.Button(frameB, text="Save ")
        self.SaveBtn.grid(row=0,column=0, padx=5, pady=5,sticky=(Tk.N, Tk.S, Tk.E, Tk.W) )
        self.LoadBtn = Tk.Button(frameB, text="Load ")
        self.LoadBtn.grid(row=0,column=1, padx=5, pady=5,sticky=(Tk.N, Tk.S, Tk.E, Tk.W))
        self.SelectBtn = Tk.Button(frameB, text="Select All ")
        self.SelectBtn.grid(row=1,column=0, padx=5, pady=5,sticky=(Tk.N, Tk.S, Tk.E, Tk.W))
        self.ClearBtn = Tk.Button(frameB, text="Clear ")
        self.ClearBtn.grid(row=1,column=1, padx=5, pady=5,sticky=(Tk.N, Tk.S, Tk.E, Tk.W))
        self.OpenEditorBtn = Tk.Button(frameB, text="Open Editor ")
        self.OpenEditorBtn.grid(row=2,column=0, padx=5, pady=5,sticky=(Tk.N, Tk.S, Tk.E, Tk.W))
        self.OpenTermBtn = Tk.Button(frameB, text="Open Terminal ")
        self.OpenTermBtn.grid(row=2,column=1, padx=5, pady=5,sticky=(Tk.N, Tk.S, Tk.E, Tk.W))
        bottomFrame.rowconfigure(0, weight=1)
        bottomFrame.rowconfigure(1, weight=1)
        bottomFrame.rowconfigure(2, weight=1)
        bottomFrame.columnconfigure(0, weight=1)
        bottomFrame.columnconfigure(0, weight=1)
        bottomFrame.pack(side=Tk.RIGHT, expand=Tk.YES, fill=Tk.X, anchor =Tk.E)

        # --------------------------------------------------------------------------

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
        self.frame3 = Tk.Frame( root, relief="sunken", borderwidth=1, width=200, height=100 )
        self.frame3.grid(row=0,column=0, sticky=(Tk.N, Tk.S, Tk.E, Tk.W)) #
        self.varProjLbl = Tk.StringVar()
        self.varProjLbl.set('Project:')
        self.varConfigLbl = Tk.StringVar()
        self.varConfigLbl.set('Configuration:')

        self.projectLabel = Tk.Label(self.frame3, textvariable = self.varProjLbl)
        self.configurationLabel = Tk.Label(self.frame3, textvariable = self.varConfigLbl)
        #self.topBut = Tk.Button(self.frame3, text="Plot ")
        #self.topBut.pack(side="top")#,fill=Tk.BOTH)
        self.projectLabel.pack(side="top", anchor = Tk.W)
        self.configurationLabel.pack(side="top", anchor = Tk.W)


        
class BottomPanel():
    def __init__(self, root):
        self.frame2 = Tk.Frame( root , relief="sunken", borderwidth=1)#, width=200, height=100)
        self.frame2.grid(row=21,column=0, sticky=(Tk.N, Tk.S, Tk.E, Tk.W)) #

        self.varStatusLbl = Tk.StringVar()
        self.varStatusLbl.set('Status:')
        self.varStatusLbl = Tk.Label(self.frame2, textvariable = self.varStatusLbl)
        self.varStatusLbl.pack(anchor = Tk.W) #side="top",fill=Tk.X)


if __name__ == '__main__':
    view = View()
    view.run()
    print("Done")


# class Model():
#
#     def __init__(self):
#         self.xpoint=200
#         self.ypoint=200
#         self.res = None
#
#     def calculate(self):
#         pass


# class Controller():
#     def __init__(self):
#         #self.root = Tk.Tk()
#         self.model = Model()
#         self.view = View()#self.root)
#         self.view.centerPanel.scriptstab.LoadBtn.bind("<Button>",self.scriptSelectionLoadButtonClick)
#
#     def run(self):
#         self.view.run()
#         #self.root.title("Black Box Tester")
#         #self.root.deiconify()
#         #self.root.mainloop()
#
#     def clear(self,event):
#         pass
#
#     def scriptSelectionLoadButtonClick(self,event):
#         print("scriptSelectionLoadButtonClick")
#         self.view.centerPanel.scriptstab.timeLabel.config(text ='changed')