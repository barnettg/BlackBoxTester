import tkinter as Tk
from tkinter import ttk
from tkinter import font
 
class View():
    def __init__(self, Controller=None):
        #root.update_idletasks()
        self.master = Tk.Tk()
        content = ttk.Frame(self.master) # not used

        self.controller = Controller

        #font
        default_font = Tk.font.nametofont("TkDefaultFont")
        default_font.configure(size=11)
        self.master.option_add("*Font", default_font)

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

    def setProjectLabel(self, val):
        print("set project label")
        self.topPanel.varProjLbl.set("Project: " + val)

    def setConfigurationLabel(self, val):
        print("set Configuration label")
        self.topPanel.varConfigLbl.set("Configuration: " + val)

    def setStatusLabel(self, val):
        print("set Status label")
        self.bottompanel.varStatusLbl.set("Status: " + val)

    #### Scripts Tab
    def setTabScriptDebugButtonCall(self, method):
        self.centerPanel.scriptstab.SetOpenEditorButtonCallback(method)

    def setTabScriptEditButtonCall(self, method):
        self.centerPanel.scriptstab.SetEditConfigButtonCallback(method)

    def setTabScriptTree(self, tree):
        pass

    #### Ports Tab
    def setTabPortsAddButtonCall(self,method):
        self.centerPanel.ports_tab.SetAddButtonCallback(method)

    def setTabPortsEditButtonCall(self,method):
        self.centerPanel.ports_tab.SetEditButtonCallback(method)

    def setTabPortsRemoveButtonCall(self,method):
        self.centerPanel.ports_tab.SetRemoveButtonCallback(method)

    def setTabPortsListbox(self, lb):
        pass

    #### Plugins Tab
    def setTabPluginsAddButtonCall(self,method):
        self.centerPanel.plugins_tab.SetAddButtonCallback(method)

    def setTabPluginsRemoveButtonCall(self,method):
        self.centerPanel.plugins_tab.SetRemoveButtonCallback(method)

    def setTabPluginsListbox(self, lb):
        pass

    #### Project Settings Tab
    def setTabProjOpenDirectoryButtonCall(self,method):
        self.centerPanel.projectSettings_tab.SetOpenDirButtonCallback(method)

    def setTabProjShowConfSettingsButtonCall(self,method):
        self.centerPanel.projectSettings_tab.SetShowConfSettingsButtonCallback(method)

    def setTabProjShowProjSettingsButtonCall(self,method):
        self.centerPanel.projectSettings_tab.SetShowProjSettingsButtonCallback(method)

    def setTabProjSelectEditorButtonCall(self,method):
        self.centerPanel.projectSettings_tab.SetSelEditorButtonCallback(method)

    def setMessagingMethod(self, method):
        self.menus.menuMessaging = method


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
        self.testsMenu.add_command(label="Show Communications Window", command=self.testsShowCommWin)
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
        self.fileExitMenuCallback = None
        self.testShowCommunicationsMenuCallback = None
        self.menuMessaging = None

    def setFileExitMenuCallback(self, method):
        self.fileExitMenuCallback = method

    def setMenuMessaging(self, method):
        self.menuMessaging = method

    def exitMenu(self):
        if self.menuMessaging is not None:
            self.menuMessaging("Menu File Exit")
        else:
            print("Exit Menu messaging not set")

    def showAbout(self):
        if self.menuMessaging is not None:
            self.menuMessaging("Menu About About")
        else:
            print("About Menu messaging not set")

    def showManual(self):
        if self.menuMessaging is not None:
            self.menuMessaging("Menu About Manual")
        else:
            print("Manual Menu messaging not set")

    def newProject(self):
        if self.menuMessaging is not None:
            self.menuMessaging("Menu Project New")
        else:
            print("newProject Menu messaging not set")

    def openProject(self):
        if self.menuMessaging is not None:
            self.menuMessaging("Menu Project Open")
        else:
            print("openProject Menu messaging not set")

    def saveProject(self):
        if self.menuMessaging is not None:
            self.menuMessaging("Menu Project Save")
        else:
            print("saveProject Menu messaging not set")

    def saveProjectAs(self):
        if self.menuMessaging is not None:
            self.menuMessaging("Menu Project SaveAs")
        else:
            print("saveProjectAs Menu messaging not set")

    def closeProject(self):
        if self.menuMessaging is not None:
            self.menuMessaging("Menu Project Close")
        else:
            print("closeProject Menu messaging not set")

    def openConfiguration(self):
        if self.menuMessaging is not None:
            self.menuMessaging("Menu Project OpenConfiguration")
        else:
            print("openConfiguration Menu messaging not set")

    def saveConfiguration(self):
        if self.menuMessaging is not None:
            self.menuMessaging("Menu Project SaveConfiguration")
        else:
            print("saveConfiguration Menu messaging not set")

    def saveConfigurationAs(self):
        if self.menuMessaging is not None:
            self.menuMessaging("Menu Project SaveConfigurationAs")
        else:
            print("saveConfigurationAs Menu messaging not set")

    def testsShowCommWin(self):
        if self.menuMessaging is not None:
            self.menuMessaging("Menu Tests ShowCommunicationsWin")
        else:
            print("testsShoeCommWin Menu messaging not set")

    def testsShowMessageWin(self):
        if self.menuMessaging is not None:
            self.menuMessaging("Menu Tests ShowMessagesWin")
        else:
            print("testsShowMessageWin Menu messaging not set")

    def testsStart(self):
        if self.menuMessaging is not None:
            self.menuMessaging("Menu Tests Start")
        else:
            print("testsStart Menu messaging not set")

    def testsStop(self):
        if self.menuMessaging is not None:
            self.menuMessaging("Menu Tests Stop")
        else:
            print("testsStop Menu messaging not set")

    def testsPause(self):
        if self.menuMessaging is not None:
            self.menuMessaging("Menu Tests Pause")
        else:
            print("testsPause Menu messaging not set")

    def testsContinue(self):
        if self.menuMessaging is not None:
            self.menuMessaging("Menu Tests Continue")
        else:
            print("testsContinue Menu messaging not set")

    def testsSaveReport(self):
        if self.menuMessaging is not None:
            self.menuMessaging("Menu Tests SaveReport")
        else:
            print("testsSaveReport Menu messaging not set")

class CenterPanel():
    def __init__(self, root):
        panedwin = Tk.PanedWindow(root, sashwidth=6,
                                  sashrelief=Tk.RAISED,
                                  borderwidth=10,
                                  handlesize=10,
                                  orient=Tk.HORIZONTAL)

        nbLeft = ttk.Notebook(panedwin)
        self.scriptstab = scriptsTab(nbLeft)
        self.ports_tab = portsTab(nbLeft)
        self.projectSettings_tab = ProjectSettingsTab(nbLeft)
        self.plugins_tab = PluginsTab(nbLeft)
        self.notifications_tab = NotificationsTab(nbLeft)


        #page1Left = self.page1_left(nbLeft) #ttk.Frame(nbLeft)
        #nbLeft.add(page1Left, text='tab1')
        #self.addTabsLeft(nbLeft)
        panedwin.add(nbLeft)

        nbRight = ttk.Notebook(panedwin)
        self.passed_tab = PassedTab(nbRight)
        self.failed_tab = FailedTab(nbRight)
        self.progress_tab = ProgressTab(nbRight)
        #page1Right = ttk.Frame(nbRight)
        #nbRight.add(page1Right, text='tab1')
        panedwin.add(nbRight)

        panedwin.grid(row=1,column=0, rowspan=20,sticky=(Tk.N, Tk.S, Tk.E, Tk.W)) #
        print("sash pos" + str(panedwin.sash_coord(0)))
        panedwin.update() # need to do to set sash correctly
        position = int(root.winfo_width()/2)
        panedwin.sash_place(0, position, 0)
        print("sash pos" + str(panedwin.sash_coord(0)))

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

        # add tree view
        frame = ttk.Frame(tab, relief="sunken", borderwidth=1)#, width=200, height=100 )
        frame.pack(side=Tk.TOP, expand=Tk.YES, fill=Tk.BOTH)
        #frame.grid(row=0,column=0,sticky=(Tk.N, Tk.S, Tk.E, Tk.W)) #
        #Tk.Grid.columnconfigure(frame, 0, weight=1)

        self.tree = ttk.Treeview(frame, displaycolumns = '#all')
        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')

        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.bind("<Double-1>", self.OnDoubleClick)

        self.test_add_misc_tree_data()

        self.tree.pack(side=Tk.TOP, expand=Tk.YES, fill=Tk.BOTH, anchor =Tk.NW)#

        # add button frame
        bottomFrame = ttk.Frame(tab, relief="sunken", borderwidth=5)#
        self.OpenEditorBtn = Tk.Button(bottomFrame, text="Edit/Debug Terminal ",
                                       width=20, command=self.OpenEditorButton)
        self.OpenEditorBtn.pack(anchor = Tk.W)
        self.EditConfigurationBtn = Tk.Button(bottomFrame, text="Edit Configuration ",
                                              width=20, command=self.EditConfigButton)
        self.EditConfigurationBtn.pack(anchor = Tk.W)

        bottomFrame.pack(side=Tk.RIGHT, expand=Tk.YES, fill=Tk.X, anchor=Tk.E)

        root.add(tab, text='Scripts')
        self.openEditorButtonCallback = None
        self.editConfigButtonCallback = None

    def OnDoubleClick(self, event):
        item = self.tree.selection()[0]
        print("you clicked on", self.tree.item(item,"text"), self.tree.item(item,"values")[0], str(self.tree.item(item)))
        print("the parent is: ", self.tree.parent(item))


    def test_add_misc_tree_data(self):
        #-----------------------------------------------------------------------
        # group name
        #   name of script
        #   selected * or blank
        #   priority level
        #   estimated time
        #   protocol file/class
        #   helper class

        # you clicked on file 2 * {'text': 'file 2', 'image': '', 'values': ['*', 1, 26, 'Simple/Simple', 'Helper.py'], 'open': True, 'tags': ''}

        self.tree["columns"]=("Selected","Level","Time Est","Protocol","Helper")
        #self.tree.column("one", width=100 )
        #self.tree.column("two", width=100)
        self.tree.heading("Selected", text="Selected")
        self.tree.heading("Level", text="Level")
        self.tree.heading("Time Est", text="Time Est.")
        self.tree.heading("Protocol", text="Protocol")
        self.tree.heading("Helper", text="Helper")


        #self.tree.insert("" , 0,    text="Group 1", values=("*"))

        id2 = self.tree.insert("", "end", "Group1", text="Group 1", values=("*"))
        self.tree.insert(id2, "end", text="file 1", values=("*","1","25.4","Simple/Simple","Helper.py"))
        self.tree.insert(id2, "end", text="file 2", values=("*","1","50","Simple/Simple","Helper.py"))
        self.tree.insert(id2, "end", text="file 3", values=("*","1","110","Simple/Simple","Helper.py"))

        ##alternatively:
        #self.tree.insert("", 3, "dir3", text="Dir 3")
        #self.tree.insert("dir3", 3, text=" sub dir 3",values=("3A"," 3B"))

        self.tree.insert("", "end", "Group2", text="Group 2", values=("*"))
        self.tree.insert("Group2", "end", text="file 1", values=("*","1","25","Simple/Simple","Helper.py"))
        self.tree.insert("Group2", "end", text="file 2", values=("*","1","26","Simple/Simple","Helper.py"))
        self.tree.insert("Group2", "end", text="file 3", values=("*","1","100","Simple/Simple","Helper.py"))


        #----------------------------------------------------------------------------

    def SetOpenEditorButtonCallback(self, method):
        self.openEditorButtonCallback = method

    def SetEditConfigButtonCallback(self, method):
        self.editConfigButtonCallback = method

    def OpenEditorButton(self):
        if self.openEditorButtonCallback is not None:
            self.openEditorButtonCallback()
        else:
            print("Open Editor button method not set")

    def EditConfigButton(self):
        if self.editConfigButtonCallback is not None:
            self.editConfigButtonCallback()
        else:
            print("Edit Configuration button method not set")

class NotificationsTab():
    def __init__(self, root):
        tab = ttk.Frame(root, relief="sunken", borderwidth=1, width=100, height=100)
        button_width = 25
        self.notebook = ttk.Notebook(tab)

        # email tab
        panelEmail = ttk.Frame(self.notebook )
        self.notebook.add(panelEmail, text='Email', compound=Tk.TOP)

        self.var_include = Tk.IntVar()
        self.check_include = Tk.Checkbutton(panelEmail, text="Include Email Report", variable=self.var_include)
        self.check_include.pack(side=Tk.TOP, anchor=Tk.NW, padx=5, pady=5)

        self.var_report = Tk.IntVar()
        self.check_report = Tk.Checkbutton(panelEmail, text="Attach Report Files", variable=self.var_report)
        self.check_report.pack(side=Tk.TOP, anchor=Tk.NW, padx=5, pady=5)

        emailAddressesLabel = Tk.Label(panelEmail, text="Email Address(es) (; seperated) ")
        self.emailToAddressTextBox = Tk.Text(panelEmail,height=1, width=60, padx=5)
        emailAddressesLabel.pack(side=Tk.TOP, anchor=Tk.NW)
        self.emailToAddressTextBox.pack(side=Tk.TOP, anchor=Tk.NW, padx=5) #, fill=Tk.X

        dummySpace = Tk.Label(panelEmail, text=" ")
        dummySpace.pack(side=Tk.TOP, anchor=Tk.NW)

        emailSubjectLabel = Tk.Label(panelEmail, text="Subject")
        self.emailSubjectTextBox = Tk.Text(panelEmail,height=1, width=60, padx=5)
        emailSubjectLabel.pack(side=Tk.TOP, anchor=Tk.NW)
        self.emailSubjectTextBox.pack(side=Tk.TOP, anchor=Tk.NW, padx=5) #, fill=Tk.X

        dummySpace1 = Tk.Label(panelEmail, text=" ")
        dummySpace1.pack(side=Tk.TOP, anchor=Tk.NW)

        emailHostLabel = Tk.Label(panelEmail, text="SMPT Host")
        self.emailHostTextBox = Tk.Text(panelEmail,height=1, width=40, padx=5)
        emailHostLabel.pack(side=Tk.TOP, anchor=Tk.NW)
        self.emailHostTextBox.pack(side=Tk.TOP, anchor=Tk.NW, padx=5) #, fill=Tk.X

        dummySpace2 = Tk.Label(panelEmail, text=" ")
        dummySpace2.pack(side=Tk.TOP, anchor=Tk.NW)

        emailPortLabel = Tk.Label(panelEmail, text="Port")
        self.emailPortTextBox = Tk.Text(panelEmail,height=1, width=20, padx=5)
        emailPortLabel.pack(side=Tk.TOP, anchor=Tk.NW)
        self.emailPortTextBox.pack(side=Tk.TOP, anchor=Tk.NW, padx=5)

        dummySpace3  = Tk.Label(panelEmail, text=" ")
        dummySpace3.pack(side=Tk.TOP, anchor=Tk.NW)

        emailFromLabel = Tk.Label(panelEmail, text="From Address")
        self.emailFromTextBox = Tk.Text(panelEmail,height=1, width=40, padx=5)
        emailFromLabel.pack(side=Tk.TOP, anchor=Tk.NW)
        self.emailFromTextBox.pack(side=Tk.TOP, anchor=Tk.NW, padx=5) #, fill=Tk.X

        dummySpace4  = Tk.Label(panelEmail, text=" ")
        dummySpace4.pack(side=Tk.TOP, anchor=Tk.NW)

        self.testEmailBtn = Tk.Button(panelEmail, text="Test Email", command=self.TestEmailButton)
        self.testEmailBtn.pack(side=Tk.TOP, anchor=Tk.NW, padx=5, pady=5)


        # text tab
        panelText = ttk.Frame(self.notebook )
        self.notebook.add(panelText, text='Text', compound=Tk.TOP)

        self.var_include = Tk.IntVar()
        self.check_includeText = Tk.Checkbutton(panelText, text="Include Text", variable=self.var_include)
        self.check_includeText.pack(side=Tk.TOP, anchor=Tk.NW, padx=5, pady=5)

        textNumbersLabel = Tk.Label(panelText, text="Phone numbers (; seperated) ")
        self.textNumTextBox = Tk.Text(panelText,height=1, width=60, padx=5)
        textNumbersLabel.pack(side=Tk.TOP, anchor=Tk.NW)
        self.textNumTextBox.pack(side=Tk.TOP, anchor=Tk.NW, padx=5) #, fill=Tk.X

        dummySpaceT0 = Tk.Label(panelText, text=" ")
        dummySpaceT0.pack(side=Tk.TOP, anchor=Tk.NW)

        textAccountSidLabel = Tk.Label(panelText, text="Account SID")
        self.textAccountSidTextBox = Tk.Text(panelText,height=1, width=60, padx=5)
        textAccountSidLabel.pack(side=Tk.TOP, anchor=Tk.NW)
        self.textAccountSidTextBox.pack(side=Tk.TOP, anchor=Tk.NW, padx=5) #, fill=Tk.X

        dummySpaceT1 = Tk.Label(panelText, text=" ")
        dummySpaceT1.pack(side=Tk.TOP, anchor=Tk.NW)

        textAuthTokenLabel = Tk.Label(panelText, text="Authentication Token")
        self.textAuthTokenTextBox = Tk.Text(panelText,height=1, width=40, padx=5)
        textAuthTokenLabel.pack(side=Tk.TOP, anchor=Tk.NW)
        self.textAuthTokenTextBox.pack(side=Tk.TOP, anchor=Tk.NW, padx=5) #, fill=Tk.X

        dummySpaceT2 = Tk.Label(panelText, text=" ")
        dummySpaceT2.pack(side=Tk.TOP, anchor=Tk.NW)

        textFromLabel = Tk.Label(panelText, text="From Number")
        self.textFromTextBox = Tk.Text(panelText,height=1, width=20, padx=5)
        textFromLabel.pack(side=Tk.TOP, anchor=Tk.NW)
        self.textFromTextBox.pack(side=Tk.TOP, anchor=Tk.NW, padx=5)

        dummySpaceT3  = Tk.Label(panelText, text=" ")
        dummySpaceT3.pack(side=Tk.TOP, anchor=Tk.NW)

        self.testTextBtn = Tk.Button(panelText, text="Test Email", command=self.TestTextButton)
        self.testTextBtn.pack(side=Tk.TOP, anchor=Tk.NW, padx=5, pady=5)


        self.notebook.pack(side=Tk.RIGHT, expand=Tk.YES, fill=Tk.BOTH, anchor =Tk.NW)
        root.add(tab, text='Notifications')

    def TestEmailButton(self):
        print("Test Email Button")

    def TestTextButton(self):
        print("Test Text Button")

class ProjectSettingsTab():
    def __init__(self, root):
        tab = ttk.Frame(root, relief="sunken", borderwidth=1, width=100, height=100)
        button_width = 25

        self.openDirectoryBtn = Tk.Button(tab, text="Open Directory Browser",
                                          width=button_width, command=self.OpenDirectoryButton)
        self.openDirectoryBtn.pack(side=Tk.TOP, anchor =Tk.W, padx=5, pady=5)

        self.showConfSettingsBtn = Tk.Button(tab, text="Show Configuration Settings",
                                             width=button_width, command=self.ShowConfigSettingsButton)
        self.showConfSettingsBtn.pack(side=Tk.TOP, anchor =Tk.W, padx=5, pady=5)

        self.showProjSettingsBtn = Tk.Button(tab, text="Show Project Settings",
                                             width=button_width, command=self.ShowProjSettingsButton)
        self.showProjSettingsBtn.pack(side=Tk.TOP, anchor =Tk.W, padx=5, pady=5)

        self.selectEditorBtn = Tk.Button(tab, text="Select Editor",
                                         width=button_width, command=self.SelectEditorButton)
        self.selectEditorBtn.pack(side=Tk.TOP, anchor =Tk.W, padx=5, pady=5)

        self.editorTextBox = Tk.Text(tab,height=1)
        self.editorTextBox.pack(side=Tk.TOP, anchor=Tk.NW, padx=5, pady=5, expand=Tk.YES)

        root.add(tab, text='Project Settings')
        self.openDirButtonCallback = None
        self.showConfSettingsButtonCallback = None
        self.showProjSettingsButtonCallback = None
        self.selectEditorButtonCallback = None

    def SetOpenDirButtonCallback(self,method):
        self.openDirButtonCallback = method

    def SetShowConfSettingsButtonCallback(self, method):
        self.showConfSettingsButtonCallback = method

    def SetShowProjSettingsButtonCallback(self, method):
        self.showProjSettingsButtonCallback = method

    def SetSelEditorButtonCallback(self, method):
        self.selectEditorButtonCallback = method

    def OpenDirectoryButton(self):
        if self.openDirButtonCallback is not None:
            self.openDirButtonCallback()
        else:
            print("Open Directory button method not set")

    def ShowConfigSettingsButton(self):
        if self.showConfSettingsButtonCallback is not None:
            self.showConfSettingsButtonCallback()
        else:
            print("Show Config Settings button method not set")

    def ShowProjSettingsButton(self):
        if self.showProjSettingsButtonCallback is not None:
            self.showProjSettingsButtonCallback()
        else:
            print("Show Proj Settings  button method not set")

    def SelectEditorButton(self):
        if self.selectEditorButtonCallback is not None:
            self.selectEditorButtonCallback()
        else:
            print("Select Editor button method not set")

class PluginsTab():
    def __init__(self, root):
        tab = ttk.Frame(root, relief="sunken", borderwidth=1, width=100, height=100)
        button_width = 25

        self.addBtn = Tk.Button(tab, text="Add Plugin", width=button_width, command=self.AddButton)
        self.addBtn.pack(side=Tk.TOP, anchor =Tk.W, padx=5, pady=5)

        self.pluginsListBox = Tk.Listbox(tab, width=100, height=25)
        self.pluginsListBox.pack(side=Tk.TOP, expand=Tk.NO, anchor =Tk.W, padx=10, pady=5)

        self.removeBtn = Tk.Button(tab, text="Remove Plugin", width=button_width, command=self.RemoveButton)
        self.removeBtn.pack(side="top", anchor =Tk.W, padx=5, pady=5)

        root.add(tab, text='Plugins')
        self.addButtonCallback = None
        self.removeButtonCallback = None

    def SetAddButtonCallback(self, method):
        self.addButtonCallback = method

    def SetRemoveButtonCallback(self, method):
        self.removeButtonCallback = method

    def AddButton(self):
        if self.addButtonCallback is not None:
            self.addButtonCallback()
        else:
            print("Plugin Add button method not set")

    def RemoveButton(self):
        if self.removeButtonCallback is not None:
            self.removeButtonCallback()
        else:
            print("Plugin Remove Button method not set")

class PassedTab():
    def __init__(self, root):
        tab = ttk.Frame(root, relief="sunken", borderwidth=1, width=100, height=100)

        self.passed = Tk.Listbox(tab)#, width=100, height=15)
        self.passed.pack(side=Tk.TOP, expand=Tk.YES, anchor =Tk.W, padx=5, pady=5, fill=Tk.BOTH)

        root.add(tab, text='Passed')

class FailedTab():
    def __init__(self, root):
        tab = ttk.Frame(root, relief="sunken", borderwidth=1, width=100, height=100)

        self.failed = Tk.Listbox(tab)#, width=100, height=15)
        self.failed.pack(side=Tk.TOP, expand=Tk.YES, anchor =Tk.W, padx=5, pady=5, fill=Tk.BOTH)

        root.add(tab, text='Failed')

class ProgressTab():
    def __init__(self, root):
        tab = ttk.Frame(root, relief="sunken", borderwidth=1, width=100, height=100)


        # top button frame---------------------------------------------------------------
        topFrame = ttk.Frame(tab, relief="flat", borderwidth=5)#
        self.start_btn = Tk.Button(topFrame, text="Start ", width=10)
        self.stop_btn = Tk.Button(topFrame, text="stop ", width=10)
        self.pause_btn = Tk.Button(topFrame, text="pause ", width=10)
        self.start_btn.pack(side=Tk.LEFT, padx=15, pady=5)
        self.stop_btn.pack(side=Tk.LEFT, padx=15, pady=5)
        self.pause_btn.pack(side=Tk.LEFT, padx=15, pady=5)
        topFrame.pack(side=Tk.TOP, expand=Tk.YES, fill=Tk.X, anchor =Tk.NW, padx=5, pady=5)

        # times frame---------------------------------------------------------------
        time_frame = ttk.Frame(tab, relief="flat", borderwidth=5)#
        self.total_time_label = Tk.Label(time_frame, text="Remaining Total Time: ")
        self.total_time_label.pack(side=Tk.TOP, padx=5, pady=5, anchor =Tk.W)
        self.running_label = Tk.Label(time_frame, text="Running Script: ")
        self.running_label.pack(side=Tk.TOP, padx=5, pady=5, anchor =Tk.W)
        self.remaining_time_label = Tk.Label(time_frame, text="Script Remaining Time: ")
        self.remaining_time_label.pack(side=Tk.TOP, padx=5, pady=5, anchor =Tk.W)
        time_frame.pack(side=Tk.TOP, expand=Tk.YES, fill=Tk.X, anchor =Tk.NW, padx=5, pady=5)

        # queue frame---------------------------------------------------------------
        queue_frame = ttk.Frame(tab, relief="flat", borderwidth=5)#
        self.queue_label = Tk.Label(queue_frame, text="Queue: ")
        self.queue_label.pack(side=Tk.TOP, padx=5, pady=5, anchor =Tk.W)
        self.queue_listbox = Tk.Listbox(queue_frame)#, width=100, height=15)
        self.queue_listbox.pack(side=Tk.TOP, expand=Tk.YES, anchor =Tk.W, padx=5, pady=5, fill=Tk.BOTH)
        queue_frame.pack(side=Tk.TOP, expand=Tk.YES, fill=Tk.X, anchor =Tk.NW, padx=5, pady=5)

        # checkbox frame---------------------------------------------------------------
        checkbox_frame = ttk.Frame(tab, relief="flat", borderwidth=5)#
        self.save_report_cb = Tk.Checkbutton(checkbox_frame, text="Save Report ")
        self.save_report_cb.pack(side=Tk.TOP, padx=5, pady=1, anchor =Tk.W)
        self.stop_on_fail_cb = Tk.Checkbutton(checkbox_frame, text="Stop all tests on first fail ")
        self.stop_on_fail_cb.pack(side=Tk.TOP, padx=5, pady=1, anchor =Tk.W)
        checkbox_frame.pack(side=Tk.TOP, expand=Tk.YES, fill=Tk.X, anchor =Tk.NW, padx=5, pady=5)

        # bottom button frame---------------------------------------------------------------
        bottom_frame = ttk.Frame(tab, relief="flat", borderwidth=5)#
        self.show_mess_btn = Tk.Button(bottom_frame, text="Show Messages ", width=25)
        self.show_com_btn = Tk.Button(bottom_frame, text="Show Communications ", width=25)
        self.show_mess_btn.pack(side=Tk.LEFT, padx=15, pady=5)
        self.show_com_btn.pack(side=Tk.LEFT, padx=15, pady=5)
        bottom_frame.pack(side=Tk.TOP, expand=Tk.YES, fill=Tk.X, anchor =Tk.NW, padx=5, pady=5)



        root.add(tab, text='Progress')


class portsTab():
    def __init__(self, root):
        tab = ttk.Frame(root, relief="sunken", borderwidth=1, width=100, height=100)

        self.portAddBtn = Tk.Button(tab, text="Add", width=15, command=self.AddButton)
        self.portAddBtn.pack(side=Tk.TOP, anchor =Tk.W, padx=5, pady=5)

        self.ports = Tk.Listbox(tab, width=100, height=15)
        self.ports.pack(side=Tk.TOP, expand=Tk.NO, anchor =Tk.W, padx=10, pady=5)

        self.portEditBtn = Tk.Button(tab, text="Edit", width=15, command=self.EditButton)
        self.portEditBtn.pack(side="top", anchor =Tk.W, padx=5, pady=5)

        self.portDelBtn = Tk.Button(tab, text="Remove", width=15, command=self.RemoveButton)
        self.portDelBtn.pack(side="top", anchor =Tk.W, padx=5, pady=5)

        root.add(tab, text='Communications')
        self.addButtonCallback = None
        self.editButtonCallback = None
        self.removeButtonCallback = None


    def SetAddButtonCallback(self, method):
        self.addButtonCallback = method

    def SetEditButtonCallback(self, method):
        self.editButtonCallback = method

    def SetRemoveButtonCallback(self, method):
        self.removeButtonCallback = method

    def AddButton(self):
        if self.addButtonCallback is not None:
            self.addButtonCallback()
        else:
            print("port Add button method not set")


    def RemoveButton(self):
        if self.removeButtonCallback is not None:
            self.removeButtonCallback()
        else:
            print("port Remove Button method not set")

    def EditButton(self):
        if self.editButtonCallback is not None:
            self.editButtonCallback()
        else:
            print("port Edit Button method not set")
        
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

        self.projectLabel.pack(side="top", anchor = Tk.W)
        self.configurationLabel.pack(side="top", anchor = Tk.W)
        
class BottomPanel():
    def __init__(self, root):
        self.frame2 = Tk.Frame( root , relief="sunken", borderwidth=1)  #, width=200, height=100)
        self.frame2.grid(row=21,column=0, sticky=(Tk.N, Tk.S, Tk.E, Tk.W))  #

        self.varStatusLbl = Tk.StringVar()
        self.varStatusLbl.set('Status:')
        self.StatusLbl = Tk.Label(self.frame2, textvariable = self.varStatusLbl)
        self.StatusLbl.pack(anchor = Tk.W) #side="top",fill=Tk.X)

class scriptsTabNotUsed():
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