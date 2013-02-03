

from Tkinter import *
import threading
import Tkinter, tkFileDialog, ttk, tkFont
import os, base64, time, string
import urllib2, paramiko
from datetime import datetime
import webbrowser



class App:
    def __init__(self, master):
        # Variables #
        self.hostURL            = StringVar()
        self.isTraversal        = StringVar()
        self.xMode              = StringVar()
        self.isAuth             = StringVar()
        self.isFind             = StringVar()
        self.isFileOrFolder     = StringVar()
        self.selectedFileName   = StringVar()
        self.isErrMsg           = StringVar()
        self.fileTypes          = StringVar()
        self.isSkip             = StringVar()
        self.useTypes           = StringVar()
        self.isFreeTextTypes    = StringVar()
        self.isFreeTextTypes2   = StringVar()
        self.is_cb_graphics     = StringVar()
        self.is_cb_documents    = StringVar()
        self.is_cb_archive      = StringVar()
        self.is_cb_web          = StringVar()
        self.is_cb_java         = StringVar()
        self.is_cb_documents2   = StringVar()
        self.is_cb_archive2     = StringVar()
        self.is_cb_java2        = StringVar()
        self.is_cb_web2         = StringVar()

        self.inProgress         = 1.0
        self.startPressed       = 0
        self.isHelped           = 0
        self.isLoaded           = 0
        self.isTopLevelOpen     = 0
        self.isEnabled          = 0
        self.getFileFromHost    = 0
        self.lastLocation       = 0
        self.isContinue         = 0
        self.stopThread         = 0
        self.lineCounter        = 0
        self.runIn200Mode       = 0
        self.forcedPaused       = 0
        self.totalLines         = 1
        self.headers            = {}
        self.excludeTypes       = []
        self.onlyTypes          = []
        self.folderList         = []
        self.word_list          = []
        self.all_words_list     = []
        
        self.localPath = os.path.join(os.getcwd())
        self.savedFileName = 'template.ptt'
        self.targetFile = 'listofFiles.txt'
        self.requestsFile = 'requestsLog.txt'

        self.logoB64 = "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"

        self.tabs =  ttk.Notebook(root)
        frame = Frame(self.tabs, width=650, height=620)
        tab_conf = ttk.Frame(self.tabs)
        tab_log = ttk.Frame(self.tabs)
        tab_res = ttk.Frame(self.tabs)
        tab_res.bind("<FocusIn>", self.ResTabSelected)
        tab_help = ttk.Frame(self.tabs)
        tab_about = ttk.Frame(self.tabs)

        self.tabs.add(frame, text="     Main     ")
        self.tabs.add(tab_conf, text=" Configuration ")
        self.tabs.add(tab_log, text="      Log      ")
        self.tabs.add(tab_res, text="    Results    ")
        self.tabs.add(tab_about, text="    About    ")#, state=HIDDEN)
        self.tabs.pack()


        ######################
        #      About TAB:    #
        ######################

        # LOGO
        self.logo = PhotoImage(data=self.logoB64)
        self.label_logo = Label(tab_about, image=self.logo)
        self.label_logo.place(bordermode=OUTSIDE, x=118, y=250)

        self.about_label_00 = Label(tab_about, text="", height=8)
        self.about_label_00.pack()
        
        # app + version        
        self.about_label = Label(tab_about, text="Path Traverser v1.3")
        self.about_label.place(bordermode=OUTSIDE, x=275, y=50)
        self.about_label.pack()

        self.about_label_02 = Label(tab_about, text="", height=1)
        self.about_label_02.pack()

        # home page address - clickable
        self.about_label_2 = Label(tab_about, underline=True, text="http://appsec.it/pt", fg="blue", cursor="hand1")
        self.about_label_2.bind("<Button-1>", self.callback)
        self.about_label_2.pack()

        self.about_label_0101 = Label(tab_about, text="", height=1)
        self.about_label_0101.pack()
        
        # underline font
        self.f = tkFont.Font(self.about_label_2, self.about_label_2.cget("font"))
        self.f.configure(underline = True)
        self.about_label_2.configure(font=self.f)

        #contact email
        self.about_label_5 = Label(tab_about, text="pt@appsec.it")
        self.about_label_5.pack()

        ######################
        #      Main TAB:     #
        ######################
        
        # Application URL: LABEL
        self.label_url = Label(frame, text="Application URL (https://myAppSrvr:777):", foreground="black")
        self.label_url.pack(side=LEFT)
        self.label_url.place(bordermode=OUTSIDE, x=5, y=45)

        # App URL: TEXT
        self.text_url = Entry(frame, width=65)
        #self.text_url.bind("<FocusIn>", self.removeStar(self.label_url))
        self.text_url.place(bordermode=OUTSIDE, x=240, y=45)

        # Home directory (in environment): LABEL
        self.label_homeDir = Label(frame, text="Home directory (app/versions/last/home):", foreground="black")
        self.label_homeDir.place(bordermode=OUTSIDE, x=5, y=85)

        # Home directory: TEXT
        self.text_homeDir = Entry(frame, width=62)
        self.text_homeDir.place(bordermode=OUTSIDE, x=240, y=85)

        # redirects to configuration tab
        self.button_ask = Button(frame, text='?', command=self.askHomeDir, cursor="question_arrow")
        self.button_ask.place(bordermode=OUTSIDE, x=620, y=81)     

        # Access to internal files
        self.radiobutton_unauth = Radiobutton(frame, indicatoron=0, text="Application files only", variable=self.isTraversal, value='n')
        self.radiobutton_unauth.place(bordermode=OUTSIDE, x=10, y=129)

        # PATH TRAVERSAL
        self.radiobutton_traversal = Radiobutton(frame, indicatoron=0, text='Path Travesal ', variable=self.isTraversal, value='y')
        self.radiobutton_traversal.place(bordermode=OUTSIDE, x=125, y=129)
        self.radiobutton_traversal.select()

        # LABEL: Cookie
        self.checkbutton_auth = Checkbutton(frame, text='Authenticated | Cookie :', variable=self.isAuth, onvalue="y", offvalue="n", command=self.useCookie)
        self.checkbutton_auth.place(bordermode=OUTSIDE, x=234, y=130)
        self.checkbutton_auth.deselect()

        # TEXT: Cookie
        self.text_cookie = Entry(frame, width=40, state=DISABLED)
        self.text_cookie.place(bordermode=OUTSIDE, x=392, y=131)
        
        # Response 
        self.label_resCodes = Label(frame, text="Select 'HTTP Status Codes' to be logged:")
        self.label_resCodes.place(bordermode=OUTSIDE, x=5, y=210)

        # status codes frame
        self.codeFrame = Frame(frame)
        self.codeFrame.place(bordermode=OUTSIDE, x=5, y=230)

        # Scroll Bar
        self.codeScrollBar = Scrollbar(self.codeFrame)
        self.codeScrollBar.pack(side=RIGHT, fill=Y)

        # List of HTTP STATUS CODES
        self.listbox_codes = Listbox(self.codeFrame, selectmode=EXTENDED, width=33, exportselection=0, yscrollcommand=self.codeScrollBar.set)
        #self.listbox_codes.insert(END, " 200:   OK")
        listofCodes = [
                        " 100:   Continue",
                        " 101:   Switching Protocols",
                        " 200:   OK",                      
                        " 201:   Created",
                        " 202:   Accepted",
                        " 203:   Non-Authoritative Information",
                        " 204:   No Content",
                        " 205:   Reset Content",
                        " 206:   Partial Content",
                        " 300:   Multiple Choices",
                        " 301:   Moved Permanently",
                        " 302:   Found",
                        " 303:   See Other",
                        " 304:   Not Modified",
                        " 305:   Use Proxy",
                        " 307:   Temporary Redirect",
                        " 400:   Bad Request",
                        " 401:   Unauthorized",
                        " 402:   Payment Required",
                        " 403:   Forbidden",
                        " 404:   Not Found",
                        " 405:   Method Not Allowed",
                        " 406:   Not Acceptable",
                        " 407:   Proxy Authentication Required",
                        " 408:   Request Timeout",
                        " 409:   Conflict",
                        " 410:   Gone",
                        " 411:   Length Required",
                        " 412:   Precondition Failed",
                        " 413:   Request Entity Too Large",
                        " 414:   Request-URI Too Long",
                        " 415:   Unsupported Media Type",
                        " 416:   Requested Range Not Satisfiable",
                        " 417:   Expectation Failed",
                        " 500:   Internal Server Error",
                        " 501:   Not Implemented",
                        " 502:   Bad Gateway",
                        " 503:   Service Unavailable",
                        " 504:   Gateway Timeout",
                        " 505:   HTTP Version Not Supported",
                        ]
        
        for item in listofCodes:
            self.listbox_codes.insert(END, item)
        #self.listbox_codes.bind("<Key>", self.listboxEnter)
        #self.listbox_codes.bind("<Button-1>", self.listboxEnter)
        #self.listbox_codes.bind("<ButtonRelease-1>", self.listboxEnter)
        #self.listbox_codes.bind("<FocusOut>", self.listboxEnter)
        #self.listbox_codes.bind("<FocusIn>", self.listboxEnter)
        #self.listbox_codes.place(bordermode=OUTSIDE, x=5, y=230)
        self.listbox_codes.pack()
        self.listbox_codes.select_set(2)
        self.codeScrollBar.configure(command=self.listbox_codes.yview)

        # Use local file (upload) / Get file from HOST
        self.radiobutton_getFilefromHost = Radiobutton(frame, text='Get file from Host',
                                                       command=self.setFileMode, variable=self.xMode, value='1')
        self.radiobutton_getFilefromHost.place(bordermode=OUTSIDE, x=275, y=210)
        self.radiobutton_getFilefromHost.select()

        # Remote connection (HOST)
        self.label_host = Label(frame, text="Host:", foreground="black")
        self.label_host.place(bordermode=OUTSIDE, x=280, y=250)
        self.entry_host = Entry(frame, width=17)
        self.entry_host.place(bordermode=OUTSIDE, x=315, y=250)

        # Remote connection (USER)
        self.label_user = Label(frame, text="User:", foreground="black")
        self.label_user.place(bordermode=OUTSIDE, x=450, y=210)
        self.entry_user = Entry(frame, width=20)
        self.entry_user.place(bordermode=OUTSIDE, x=510, y=210)

        # Remote connection (PW)
        self.label_pw = Label(frame, text="Password:", foreground="black")
        self.label_pw.place(bordermode=OUTSIDE, x=450, y=250)
        self.entry_pw = Entry(frame, width=20, show='*')
        self.entry_pw.place(bordermode=OUTSIDE, x=510, y=250)
        
        # Upload File: LABEL
        self.radiobutton_uploadFile = Radiobutton(frame, text='Upload file', command=self.setFileMode, variable=self.xMode, value='2')
        self.radiobutton_uploadFile.place(bordermode=OUTSIDE, x=275, y=325)

        # Upload File: Button
        self.upload_button = Button(frame, text="  Browse...", command=self.browseFile, disabledforeground="gray", state=DISABLED)
        self.upload_button.place(bordermode=OUTSIDE, x=385, y=325)

        # Upload File: Label
        self.upload_label = Label(frame, text="", state=DISABLED)
        self.upload_label.place(bordermode=OUTSIDE, x=295, y=360)

        # Check Button: Skip Line
        self.checkbutton_skipLine = Checkbutton(frame, text='Skip to line # ', variable=self.isSkip, onvalue="y", offvalue="n", command=self.useSkip, state=DISABLED)
        self.checkbutton_skipLine.place(bordermode=OUTSIDE, x=495, y=325)
        self.checkbutton_skipLine.deselect()

        # TEXT: Skip Line
        self.text_skipLine = Entry(frame, width=6, state=DISABLED)
        self.text_skipLine.pack()
        self.text_skipLine.place(bordermode=OUTSIDE, x=590, y=325)

        # Check Button: Error Msg
        self.checkbutton_errMsg = Checkbutton(frame, text='Error Message :', variable=self.isErrMsg, onvalue="y", offvalue="n", command=self.useErrMsg)
        self.checkbutton_errMsg.place(bordermode=OUTSIDE, x=280, y=420)
        self.checkbutton_errMsg.deselect()

        # TEXT: Error Msg
        self.text_errMsg = Entry(frame, width=38, state=DISABLED)
        self.text_errMsg.place(bordermode=OUTSIDE, x=400, y=420)

        # File types: Label
        self.types_label = Label(frame, text="File Types configuration:", state=NORMAL)
        self.types_label.place(bordermode=OUTSIDE, x=10, y=420)

        # File types: Default
        self.radiobutton_fileTypeDefault = Radiobutton(frame, text='Default Settings', command=self.setFileTypes, variable=self.fileTypes, value='1')
        self.radiobutton_fileTypeDefault.place(bordermode=OUTSIDE, x=10, y=455)
        self.radiobutton_fileTypeDefault.select()
        
        # File types: Manual
        self.radiobutton_fileTypeManual = Radiobutton(frame, text='Manual', command=self.setFileTypes, variable=self.fileTypes, value='2')
        self.radiobutton_fileTypeManual.place(bordermode=OUTSIDE, x=10, y=495)

        # File types: Button
        self.fileType_button = Button(frame, text="  Configure  ", command=self.configureFileTypes, disabledforeground="gray", state=DISABLED)
        self.fileType_button.place(bordermode=OUTSIDE, x=100, y=494)
       

        ########## Main Buttons ###########

        # >> Run Button
        self.button_run = Button(frame, text="Start", width=25, height=2, command=self.runPressed)
        self.button_run.place(bordermode=OUTSIDE, x=225, y=525)

        # >> Stop/Quit Button
        self.button_stop = Button(frame, text="Quit", width=10, height=2, command=self.executeQuit)
        self.button_stop.place(bordermode=OUTSIDE, x=400, y=525)

        # >> Quit Button
        #self.quit_button = Button(frame, text="Quit", width=10, height=2, command=self.executeQuit)
        #self.quit_button.place(bordermode=OUTSIDE, x=570, y=525)

        # >> Load session Buttons

        self.log_button = Button(frame, text=" Load state ", command=self.executeLoad)
        self.log_button.place(bordermode=OUTSIDE, x=570, y=2)

        # >> Save State Button
        self.help_button = Button(frame, text="Save state", width=10, height=1, command=self.executeSave)
        self.help_button.place(bordermode=OUTSIDE, x=490, y=2)

        # Status bars     
        self.text_status = Text(frame, state=NORMAL, width=92, height=10, background="#DDDDDD", foreground="#990000")
        self.text_status.insert(INSERT, "Status")
        self.text_status.pack()
        self.text_status.configure(state=DISABLED)
        self.text_status.place(bordermode=OUTSIDE, x=0, y=568)

        # Progress bar
        self.progress = ttk.Progressbar(frame, orient="horizontal", length=648, mode="determinate")
        #self.progress.pack()
        self.progress.place(bordermode=OUTSIDE, x=1, y=600)
        

        ######################
        # Configuration TAB: #
        ######################

        self.button_conf_default = Button(tab_conf, text=" Restore to Default ", command=self.restoreDefaultConfiguration, state=DISABLED)
        self.button_conf_default.place(bordermode=OUTSIDE, x=525, y=120)

        # File types: Enable
        self.radiobutton_fileTypeEnable = Button(tab_conf, text='Enable', command=self.enableTypes)
        self.radiobutton_fileTypeEnable.place(bordermode=OUTSIDE, x=558, y=80)

        # Exclude types
        self.radiobutton_excludeTypes = Radiobutton(tab_conf, text='Exclude the following File Types: ', command=self.useFileTypes, variable=self.useTypes, value='1', state=DISABLED)
        self.radiobutton_excludeTypes.place(bordermode=OUTSIDE, x=25, y=10)
        self.radiobutton_excludeTypes.select()

        # Use only types
        self.radiobutton_useOnlyTypes = Radiobutton(tab_conf, text='Use only to following File Types: ', command=self.useFileTypes, variable=self.useTypes, value='2', state=DISABLED)
        self.radiobutton_useOnlyTypes.place(bordermode=OUTSIDE, x=275, y=10)

        # CheckButton types to exclude:
        self.cb_graphics = Checkbutton(tab_conf, text='gif, png, jpg, bmp', state=DISABLED,
                                         variable=self.is_cb_graphics, offvalue='n', onvalue='y')
        self.cb_graphics.place(bordermode=OUTSIDE, x=45, y=50)
        self.cb_graphics.select()

        self.cb_documents = Checkbutton(tab_conf, text='xml, txt, doc, xls, ppt, pdf', state=DISABLED,
                                         variable=self.is_cb_documents, offvalue='n', onvalue='y')
        self.cb_documents.place(bordermode=OUTSIDE, x=45, y=75)
        self.cb_documents.deselect()

        self.cb_archive = Checkbutton(tab_conf, text='zip, rar, tar, tar.gz', state=DISABLED,
                                         variable=self.is_cb_archive, offvalue='n', onvalue='y')
        self.cb_archive.place(bordermode=OUTSIDE, x=45, y=100)
        self.cb_archive.deselect()

        self.cb_web = Checkbutton(tab_conf, text='php, jsp, html, aspx, js', state=DISABLED,
                                         variable=self.is_cb_web, offvalue='n', onvalue='y')
        self.cb_web.place(bordermode=OUTSIDE, x=45, y=125)
        self.cb_web.select()

        self.cb_source = Checkbutton(tab_conf, text='c, cpp, dba, cs, py, vb', state=DISABLED)
        #self.cb_source.place(bordermode=OUTSIDE, x=45, y=150)

        self.cb_java = Checkbutton(tab_conf, text='java, class, jar, war, ear', state=DISABLED,
                                         variable=self.is_cb_java, offvalue='n', onvalue='y')
        self.cb_java.place(bordermode=OUTSIDE, x=45, y=150)
        self.cb_java.deselect()
        
        self.cb_freeText = Checkbutton(tab_conf, text='Others (type1, type2, type3):', state=DISABLED,
                                       variable=self.isFreeTextTypes, offvalue='n', onvalue='y', command=self.allowFreeTextTypes)
        self.cb_freeText.place(bordermode=OUTSIDE, x=45, y=190)
        self.cb_freeText.deselect()
        
        self.exclude_freeText = Entry(tab_conf, width=30, state=DISABLED)
        self.exclude_freeText.place(bordermode=OUTSIDE, x=67, y=225)
        

        # CheckButton types to test (only):
        self.cb_graphics2 = Checkbutton(tab_conf, text='gif, png, jpg, bmp', state=DISABLED)
        #self.cb_graphics2.place(bordermode=OUTSIDE, x=295, y=175)

        self.cb_documents2 = Checkbutton(tab_conf, text='xml, txt, doc, xls, ppt, pdf', state=DISABLED,
                                         variable=self.is_cb_documents2, offvalue='n', onvalue='y')
        self.cb_documents2.place(bordermode=OUTSIDE, x=295, y=50)
        self.cb_documents2.select()

        self.cb_source2 = Checkbutton(tab_conf, text='c, cpp, dba, cs, py, vb', state=DISABLED)
        #self.cb_source2.place(bordermode=OUTSIDE, x=295, y=100)
        #self.cb_source2.select()

        self.cb_archive2 = Checkbutton(tab_conf, text='zip, rar, tar, tar.gz', state=DISABLED,
                                         variable=self.is_cb_archive2, offvalue='n', onvalue='y')
        self.cb_archive2.place(bordermode=OUTSIDE, x=295, y=125)
        self.cb_archive2.select()

        self.cb_java2 = Checkbutton(tab_conf, text='java, class, jar, war, ear', state=DISABLED,
                                         variable=self.is_cb_java2, offvalue='n', onvalue='y')
        self.cb_java2.place(bordermode=OUTSIDE, x=295, y=75)
        self.cb_java2.select()

        self.cb_web2 = Checkbutton(tab_conf, text='php, jsp, html, js, aspx, css', state=DISABLED,
                                         variable=self.is_cb_web2, offvalue='n', onvalue='y')
        self.cb_web2.place(bordermode=OUTSIDE, x=295, y=100)
        self.cb_web2.deselect()
        
        # other - checkbox
        self.cb_freeText2 = Checkbutton(tab_conf, text='Others (type1, type2, type3):', state=DISABLED,
                                       variable=self.isFreeTextTypes2, offvalue='n', onvalue='y', command=self.allowFreeTextTypes2)
        self.cb_freeText2.place(bordermode=OUTSIDE, x=295, y=190)
        self.cb_freeText2.deselect()

        # free text enty
        self.only_freeText = Entry(tab_conf, width=30, state=DISABLED)
        self.only_freeText.place(bordermode=OUTSIDE, x=317, y=225)

        #file name to search field
        self.text_findFile = Entry(tab_conf, width=30, state=DISABLED)
        self.text_findFile.place(bordermode=OUTSIDE, x=275, y=355)

        # find button - to find file in host
        self.button_findFile = Button(tab_conf, text='Find', command=self.findMyFile, state=DISABLED)
        self.button_findFile.place(bordermode=OUTSIDE, x=225, y=350)      

        # grid frame
        self.gridFframe=Frame(tab_conf)
        self.gridFframe.place(bordermode=OUTSIDE, x=50, y=385)

        # grid VERTICAL scrollbar
        self.gridVERTICALscrollbar = Scrollbar(self.gridFframe) 
        self.gridVERTICALscrollbar.pack(side=RIGHT, fill=Y)

        # grid HORIZONTAL scrollbar
        self.gridHORIZONTALLscrollbar = Scrollbar(self.gridFframe, orient=HORIZONTAL) 
        self.gridHORIZONTALLscrollbar.pack(side=BOTTOM, fill=X)
        
        # grid listbox for results
        self.listboxFind = Listbox(self.gridFframe, width=90, yscrollcommand=self.gridVERTICALscrollbar.set, xscrollcommand=self.gridHORIZONTALLscrollbar.set) 
        self.listboxFind.pack()
        
        self.gridVERTICALscrollbar.config(command=self.listboxFind.yview)
        self.gridHORIZONTALLscrollbar.config(command=self.listboxFind.xview)

        # location select button
        self.button_useSelected = Button(tab_conf, text='Use selected', state=DISABLED, command=self.useSelection)
        self.button_useSelected.place(bordermode=OUTSIDE, x=518, y=350)

        # HEADER
        self.label_header = Label(tab_conf, text="Find file/folder in host's File System")
        self.label_header.place(bordermode=OUTSIDE, x=75, y=320)
        
        #enable find location        
        self.checkbox_header = Checkbutton(tab_conf, command=self.enableFindFile, variable=self.isFind, offvalue='n', onvalue='y')
        self.checkbox_header.place(bordermode=OUTSIDE, x=45, y=320)
        self.checkbox_header.deselect()

        # find file - radio button
        self.radio_findFile = Radiobutton(tab_conf, text='File', variable=self.isFileOrFolder, value='_file', state=DISABLED)
        self.radio_findFile.place(bordermode=OUTSIDE, x=45, y=350)
        self.radio_findFile.select()

        # find Library - radio button
        self.radio_findLibrary = Radiobutton(tab_conf, text='Library', variable=self.isFileOrFolder, value='_folder', state=DISABLED)
        self.radio_findLibrary.place(bordermode=OUTSIDE, x=100, y=350)
        self.radio_findLibrary.deselect()



        ######################
        #    Results TAB:    #
        ######################
        self.results_text = Text(tab_res, width=90, height=39, state=DISABLED)
        self.results_text.bind("<Double-Button-1>", self.hyperlinkURL)
        self.results_text.bind("<ButtonRelease-1>", self.copyLink)
        self.results_text.bind("<Motion>", self.hyperlinkCurser)
        self.results_text.bind("<Enter>", self.hyperlinkCurser)
        self.results_text.place(bordermode=OUTSIDE, x=5, y=5)
        self.button_clearRes = Button(tab_res, text="Clear Results", command=self.clearResults)
        self.button_clearRes.place(bordermode=OUTSIDE, x=300, y=593)

        # Scroll Bar
        self.resScrollBar = Scrollbar(tab_res)
        self.resScrollBar.pack(side=RIGHT, fill=Y)
        self.resScrollBar.configure(command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=self.resScrollBar.set)


        ######################
        #      Log TAB:      #
        ######################
        self.log_text = Text(tab_log, width=90, height=39, state=DISABLED)
        self.log_text.place(bordermode=OUTSIDE, x=5, y=5)
        self.button_clearLog = Button(tab_log, text="  Clear Log  ", command=self.clearLog)
        self.button_clearLog.place(bordermode=OUTSIDE, x=300, y=593)

        # Scroll Bar
        self.logScrollBar = Scrollbar(tab_log)
        self.logScrollBar.pack(side=RIGHT, fill=Y)
        self.logScrollBar.configure(command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=self.logScrollBar.set)
        



        self.tabs.select(self.tabs.tabs()[0])




## ============================================================================================================================= ##
## ======================================================  FUNCTUIONS  ========================================================= ##
## ============================================================================================================================= ##

    # open home page by clicking address in About Tab
    def callback(self, event):
        webbrowser.open('http://appsec.it/pt')
    

    # if URL is double-clicked - open URL in browser
    def hyperlinkURL(self, event):
        index = self.results_text.index("@%s,%s" % (event.x, event.y))
        line = index.split(".")
        myURL= self.results_text.get(line[0]+'.6', line[0] +'.end')
        if myURL[0:4] == "http":
            webbrowser.open(myURL)


    # hand (clickable) curser when over a URL
    def hyperlinkCurser(self, event):
        index = self.results_text.index("@%s,%s" % (event.x, event.y))
        line = index.split(".")
        myURL = self.results_text.get(line[0]+'.6', line[0] +'.end')
        if (string.atoi(line[1]) > 5) and (myURL[0:4] == "http") and (self.results_text.get(index) != '\n'):
            self.results_text.configure(cursor="hand2")
        else:
            self.results_text.configure(cursor="")


    # copy selected text into clipboard
    def copyLink(self, event):
        Tk.clipboard_clear(root)
        try:
            text = self.results_text.get("sel.first", "sel.last")
            Tk.clipboard_append(root, text)
        except:
            pass


    # Results Tab selected
    def ResTabSelected(self, event):
        if self.startPressed == 1:
            self.pausePressed()
        self.clearResults()
        #self.editStatus(self.lastTime, 4)
        try:
            dirList = os.listdir(self.resultsFolder)
            for file in self.codeFilesList:
                codeLoc = len(file)
                code = file[codeLoc-10:codeLoc]
            #for file in dirList:
                #if os.path.getsize(self.resultsFolder +'\\' +file) > 0:
                    #lines = open(self.resultsFolder +'\\' +file, 'r').read().split('\n')
                if os.path.getsize(file) > 0:
                    lines = open(file, 'r').read().split('\n')
                    for line in lines:
                        if line != '' and line !='\n':
                            self.editStatus('[' +code[3:6] +']\t' +line, 4)
        except:
            self.editStatus('No Results so far...', 4)



    # redirect to find file in env.
    def askHomeDir(self):
        self.tabs.select(self.tabs.tabs()[1])
        self.checkbox_header.select()
        self.button_findFile.configure(state=NORMAL)
        self.text_findFile.configure(state=NORMAL)
        self.listboxFind.configure(state=NORMAL)
        self.radio_findLibrary.configure(state=NORMAL)
        self.radio_findFile.configure(state=NORMAL)
        #self.label_header.configure(foreground="black")
        self.getFileFromHost = 1



    def enableFindFile(self):
        if self.isFind.get() == 'y':
            self.askHomeDir()
        else:
            self.button_findFile.configure(state=DISABLED)
            self.text_findFile.configure(state=DISABLED)
            self.listboxFind.configure(state=DISABLED)
            self.radio_findLibrary.configure(state=DISABLED)
            self.radio_findFile.configure(state=DISABLED)
            self.getFileFromHost = 0
            #self.tabs.select(self.tabs.tabs()[0])



    # serach in host enviroment for entered file
    def findMyFile(self):
        if len(self.text_findFile.get()) > 1:
            self.getFileFromHost = 1
            if self.sshHost():
                self.getFileFromHost = 0
                self.listboxFind.delete(0, END)
                tmpFile = open('locationOptions.txt', 'r')
                lines = tmpFile.readlines()
                tmpFile.close()
                for line in lines:
                    self.listboxFind.insert(END, line)
                    
            else:
                self.editStatus('Error! could not connect to host (user/password?)', 1)
                self.tabs.select(self.tabs.tabs()[0])
                
            self.listboxFind.pack()
            self.button_useSelected.configure(state=NORMAL)       
        


    # use selection as Home Dir path
    def useSelection(self):
        i = 0
        selectedLocation = []
        tmpList = self.listboxFind.get(0, END)
        listLength = len(tmpList)
        fileLength = len(self.text_findFile.get())
        for i in range(listLength):
            x = self.listboxFind.get(i)
            mylen = len(x)
            if self.listboxFind.select_includes(i) == True:
                self.text_homeDir.delete(0, END)
                if self.isFileOrFolder.get() == '_file':
                    self.text_homeDir.insert(0, x[2:mylen -fileLength -2])
                else:
                    self.text_homeDir.insert(0, x[2:-1])
                    
                self.editStatus("Would you like to save your settings? press the 'Save State' button...", 1)
                self.tabs.select(self.tabs.tabs()[0])
                self.checkbox_header.deselect()
                self.enableFindFile()
                return 1

        self.editStatus('No selection was chosen', 1)
        return 0



    # clears log in 'Log' tab
    def clearLog(self):
        self.log_text.configure(state=NORMAL)
        self.log_text.delete(1.0, END)
        self.log_text.configure(state=DISABLED)
        

    # clears results in 'Results' tab
    def clearResults(self):
        self.results_text.configure(state=NORMAL)
        self.results_text.delete(1.0, END)
        self.results_text.configure(state=DISABLED)



    # saves current state into a file
    def executeSave(self):
        #verifyPath = sys.path[0] + '\\' +self.saveFileName
        self.isLoaded = 0
        verifyPath = os.path.join(os.getcwd()) + '\\' +self.savedFileName
        if len(self.text_url.get()) > 1:
            file = open(self.savedFileName, 'w')
            file.write('start_of_new_session\n')
            file.write('host:' +self.entry_host.get() +'\n')
            file.write('user:' +self.entry_user.get() +'\n')
            file.write('url:' +self.text_url.get() +'\n')
            file.write('homedir:' +self.text_homeDir.get()+ '\n')
            if self.isErrMsg.get() == "y":
                file.write('err:' +self.text_errMsg.get() +'\n')
            else:
                file.write('NO ERROR MESSAGE\n')

            if self.xMode.get() == '1':
                file.write('mode:1\n')
            else:
                try:
                    tmpFile = open(self.selectedFileName, 'r')
                    file.write('mode:2\n')
                    file.write('file:' +self.selectedFileName +'\n')
                except:
                    self.editStatus('Could not save - please select a file', 3)
                    return 0
                
            self.editStatus('Saved details to: %s' %verifyPath, 3)
            file.close()




    # Load saved state from saved file
    def executeLoad(self):
            #verifyPath = sys.path[0] + '\\' +self.saveFileName
            if self.isLoaded != 1:
                self.isLoaded = 1
                verifyPath = os.path.join(os.getcwd()) + '\\' +self.savedFileName
                if os.path.exists(verifyPath) == True:
                    file = open(self.savedFileName, 'r')
                    lines = file.read().split('\n')
                    self.entry_host.insert(0, lines[1][5:])
                    self.entry_user.insert(0, lines[2][5:])
                    self.text_url.insert(0, lines[3][4:])
                    self.text_homeDir.insert(0, lines[4][8:])
                    try:
                        loadErr = lines[5]
                        if loadErr[:4] == 'err:':
                            self.checkbutton_errMsg.select()
                            self.text_errMsg.configure(state=NORMAL)
                            self.text_errMsg.insert(0, loadErr[4:])                 
                    except:
                        self.editStatus('No error message was loaded', 3)

                    if lines[6][5:] == '2':
                        self.xMode.set('2')
                        self.setFileMode()
                        self.selectedFileName = lines[7][5:]
                        self.upload_label.configure(text = '...' +self.selectedFileName)
                        selectedFileLength = len(self.selectedFileName)
                        if selectedFileLength > 40:
                            displayedFileName = '...' +self.selectedFileName[selectedFileLength -37:]
                        else:
                            displayedFileName = self.selectedFileName
                        self.upload_label.configure(state=NORMAL, text='Selected file:        %s' %displayedFileName, foreground="darkblue")
                        self.radiobutton_uploadFile.select()
                    else:
                        self.xMode.set('1')
                        self.setFileMode()

                    self.editStatus('Loaded details from: %s' %verifyPath, 3)
                    file.close()
                        
                else:
                    self.editStatus('No save file to load.', 1)



    # skip file to chosen line    
    def useSkip(self):
        if self.isSkip.get() == 'y':
            self.text_skipLine.configure(state=NORMAL)
        else:
            self.text_skipLine.configure(state=DISABLED)



    # use maunal error message in response
    def useErrMsg(self):
        if self.isErrMsg.get() == 'y':
            self.text_errMsg.configure(state=NORMAL)
        else:
            self.text_errMsg.configure(state=DISABLED)
    


    # use cookie for requests
    def useCookie(self):
        if self.isAuth.get() == 'y':
            self.text_cookie.configure(state=NORMAL)
        else:
            self.text_cookie.configure(state=DISABLED)


    # if = 1: get file from HOST, else: use uploaded file
    def setFileMode(self):
        if self.xMode.get() == '1':
            self.upload_button.configure(state=DISABLED)
            self.checkbutton_skipLine.configure(state=DISABLED)
            self.entry_host.configure(state=NORMAL)
            self.entry_user.configure(state=NORMAL)
            self.entry_pw.configure(state=NORMAL)
            #self.upload_label.configure(text="")
        else:
            self.checkbutton_skipLine.configure(state=NORMAL)
            self.upload_button.configure(state=NORMAL)
            self.entry_host.configure(state=DISABLED)
            self.entry_user.configure(state=DISABLED)
            self.entry_pw.configure(state=DISABLED)



    # manual selection of files types is selected
    def enableTypes(self):
        if self.isEnabled == 0:
            self.isEnabled = 1
            self.radiobutton_fileTypeManual.select()
            self.setFileTypes()
            self.radiobutton_fileTypeEnable.configure(text="Disable")
        else:
            self.radiobutton_fileTypeEnable.configure(text="Enable")
            self.isEnabled = 0
            self.radiobutton_fileTypeDefault.select()
            self.setFileTypes()
            #self.tabs.select(self.tabs.tabs()[0])



    # in default all selections of File Types are disabled
    # enables when choosed
    def setFileTypes(self):   
        if self.fileTypes.get() == '1':
            self.button_conf_default.configure(state=DISABLED)
            self.fileType_button.configure(state=DISABLED)
            self.radiobutton_excludeTypes.configure(state=DISABLED)
            self.radiobutton_useOnlyTypes.configure(state=DISABLED)
            self.cb_graphics.configure(state=DISABLED)
            self.cb_documents.configure(state=DISABLED)
            self.cb_archive.configure(state=DISABLED)
            self.cb_web.configure(state=DISABLED)
            #self.cb_source.configure(state=DISABLED)
            self.cb_java.configure(state=DISABLED)
            self.cb_freeText.configure(state=DISABLED)
            #self.cb_graphics2.configure(state=DISABLED)
            self.cb_documents2.configure(state=DISABLED)
            self.cb_archive2.configure(state=DISABLED)
            self.cb_web2.configure(state=DISABLED)
            #self.cb_source2.configure(state=DISABLED)
            self.cb_java2.configure(state=DISABLED)
            self.cb_freeText2.configure(state=DISABLED)       
        else:
            self.fileType_button.configure(state=NORMAL)
            self.button_conf_default.configure(state=NORMAL)
            self.restoreDefaultConfiguration()
            self.isEnabled = 1
            self.radiobutton_fileTypeEnable.configure(text="Disable")



    # use free text field to add file types to use-only
    def allowFreeTextTypes(self):
        if self.isFreeTextTypes.get() == 'y':
            self.exclude_freeText.configure(state=NORMAL)
        else:
            self.exclude_freeText.configure(state=DISABLED)



    # use free text field to add file types to exclude
    def allowFreeTextTypes2(self):
        if self.isFreeTextTypes2.get() == 'y':
            self.only_freeText.configure(state=NORMAL)
        else:
            self.only_freeText.configure(state=DISABLED)
     


    # goes to 'File Types' tab
    def configureFileTypes(self):
        self.tabs.select(self.tabs.tabs()[1]) 
            


    # brings File Types settings to default selection
    def restoreDefaultConfiguration(self):
        self.radiobutton_excludeTypes.configure(state=NORMAL)
        self.radiobutton_useOnlyTypes.configure(state=NORMAL)
        self.radiobutton_useOnlyTypes.deselect()
        self.radiobutton_excludeTypes.select()

        self.cb_graphics.configure(state=NORMAL)
        self.cb_documents.configure(state=NORMAL)
        self.cb_archive.configure(state=NORMAL)
        self.cb_web.configure(state=NORMAL)
        self.cb_source.configure(state=NORMAL)
        self.cb_java.configure(state=NORMAL)
        self.cb_freeText.configure(state=NORMAL)
        self.exclude_freeText.configure(state=DISABLED)
        
        #self.cb_graphics2.configure(state=DISABLED)
        self.cb_documents2.configure(state=DISABLED)
        self.cb_archive2.configure(state=DISABLED)
        self.cb_web2.configure(state=DISABLED)
        #self.cb_source2.configure(state=DISABLED)
        self.cb_java2.configure(state=DISABLED)
        self.cb_freeText2.configure(state=DISABLED)
        self.only_freeText.configure(state=DISABLED)  
        
        self.cb_graphics.select()
        self.cb_documents.deselect()
        self.cb_archive.deselect()
        self.cb_web.select()
        #self.cb_source.deselect()
        self.cb_java.deselect()
        self.cb_freeText.deselect()
        #self.cb_graphics2.deselect()
        self.cb_documents2.select()
        self.cb_archive2.select()
        self.cb_web2.deselect()
        #self.cb_source2.select()
        self.cb_java2.select()
        self.cb_freeText2.deselect()



    # exclude/use-only File Types
    def useFileTypes(self):
        if self.useTypes.get() == '2': #use only
            #self.cb_graphics2.configure(state=NORMAL)
            self.cb_documents2.configure(state=NORMAL)
            self.cb_archive2.configure(state=NORMAL)
            self.cb_web2.configure(state=NORMAL)
            #self.cb_source2.configure(state=NORMAL)
            self.cb_java2.configure(state=NORMAL)
            self.cb_freeText2.configure(state=NORMAL)

            self.cb_graphics.configure(state=DISABLED)
            self.cb_documents.configure(state=DISABLED)
            self.cb_archive.configure(state=DISABLED)
            self.cb_web.configure(state=DISABLED)
            #self.cb_source.configure(state=DISABLED)
            self.cb_java.configure(state=DISABLED)
            self.cb_freeText.configure(state=DISABLED)
                
        else: #exclude
            self.cb_graphics.configure(state=NORMAL)
            self.cb_documents.configure(state=NORMAL)
            self.cb_archive.configure(state=NORMAL)
            self.cb_web.configure(state=NORMAL)
            #self.cb_source.configure(state=NORMAL)
            self.cb_java.configure(state=NORMAL)
            self.cb_freeText.configure(state=NORMAL)
            
            #self.cb_graphics2.configure(state=DISABLED)
            self.cb_documents2.configure(state=DISABLED)
            self.cb_archive2.configure(state=DISABLED)
            self.cb_web2.configure(state=DISABLED)
            #self.cb_source2.configure(state=DISABLED)
            self.cb_java2.configure(state=DISABLED)
            self.cb_freeText2.configure(state=DISABLED)
            
        

    # Browse file system to get file to use for requests
    def browseFile(self):
        self.selectedFileName = tkFileDialog.askopenfilename(filetypes = ( ("Text files", "*.txt"), ("All files", "*.*") ))
        try:
            tmpFile = open(self.selectedFileName, 'r')
            self.editStatus('opened: %s' %self.selectedFileName, 3)
            tmpFile.close()
            selectedFileLength = len(self.selectedFileName)
            if selectedFileLength > 40:
                displayedFileName = '...' +self.selectedFileName[selectedFileLength -37:]
            else:
                displayedFileName = self.selectedFileName
                
            self.upload_label.configure(state=NORMAL, text='Selected file:        %s' %displayedFileName, foreground="darkblue")
            tmpFile.close()
            
        except:
            self.editStatus('Error! file does not exist', 3)



#####################################################################################################################
#########################################         START OF RUN()       ##############################################
#####################################################################################################################

    def runPressed(self):
        try:
            self.stopThread = 0
            self.executeRun()            
        except:
            self.progress["value"] = 0
            self.isContinue = 0
            self.lastLocation = 0
            self.editStatus('Could not start (server down?) please try again...', 3)
            self.button_run.configure(text="Start", command=self.runPressed)
            self.button_stop.configure(text="Quit", command=self.executeQuit)


    def pausePressed(self):
        self.stopThread = 1
        self.lastLocation = self.lineCounter
        self.button_run.configure(text="Continue", command=self.continuePressed)
        self.editStatus('-- Paused @ line: ' +str(self.lastLocation), 3)


    def continuePressed(self):
        self.stopThread = 0
        self.editStatus('-- Resume @ line: ' +str(self.lastLocation), 3)
        self.isContinue = 1
        self.progress["value"] = (self.lastLocation / float(self.totalLines)) * 100
        self.lineCounter = self.lastLocation
        self.button_run.configure(text="Pause", command=self.pausePressed)
        self.button_stop.configure(text="Stop", command=self.stopPressed)
        self.executeRun()


    def stopPressed(self):
        #self.startPressed = 0
        self.stopThread = 1
        if self.lineCounter > 1:
            current = self.lineCounter -1
            self.editStatus('Stopped @ line: %d' %current, 3)
            time.sleep(1)
            self.lineCounter = 0
        #self.progress["value"] = 0
        #self.isContinue = 0
        #self.lastLocation = 0
        #self.button_run.configure(text="Start", command=self.runPressed)
        #self.button_stop.configure(text="Quit", command=self.executeQuit)
        self.terminator()

        

############################################################################################################################################
        ############################################################ RUN #########################################################
                ############################################################################################################

    def executeRun(self):
        self.startPressed = 1
        if self.isContinue == 0:
            self.progress["value"] = 0
            self.button_run.configure(text="Pause", command=self.pausePressed)
            self.button_stop.configure(text="Stop", command=self.stopPressed)
            self.editStatus("\n\nInitializing! please wait...", 3)
            # print Date to Results Tab
            self.lastTime = "\n\n*************************** [ %s ]***************************\n" %str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.progress["value"] = 3
            isMissing = 0
            self.onlyTypes = []
            self.excludeTypes = []
            # is URL missing?
            self.URL_TEXT = self.text_url.get().strip()
            if len(self.URL_TEXT) < 1:
                isMissing = 1
                self.addStar(self.label_url)
            else:
                self.removeStar(self.label_url)
                
            # is HOME DIR missing?
            self.homeDir_TEXT = self.text_homeDir.get().strip()
            if len(self.homeDir_TEXT) < 1:
                isMissing = 1 
                self.addStar(self.label_homeDir)
            else:
                self.removeStar(self.label_homeDir)

            # Connect to hose to get file
            if self.xMode.get() == "1":

                #is HOST missing
                self.host_TEXT = self.entry_host.get().strip()
                if len(self.host_TEXT) < 1:
                    isMissing = 1 
                    self.addStar(self.label_host)
                else:
                    self.removeStar(self.label_host)

                #is USER missing               
                self.user_TEXT = self.entry_user.get().strip()
                if len(self.user_TEXT) < 1:
                    isMissing = 1
                    self.addStar(self.label_user)
                else:
                    self.removeStar(self.label_user)

                #is PW missing
                self.pw_TEXT =   self.entry_pw.get().strip()
                if len(self.pw_TEXT) < 1:
                    isMissing = 1
                    self.addStar(self.label_pw)
                else:
                    self.removeStar(self.label_pw)               
                    
                if isMissing == 1:
                    self.editStatus("Please fill in the missing fields (Red) and Press 'Run' again", 1)
                    self.terminator()
                    return 0

                else:
                    self.editStatus('Trying to connect to host: %s,  please wait...' %self.entry_host.get(), 3)
                    self.progress["value"] = 10
                    self.getFileFromHost = 0
                    if self.sshHost() == 1:
                        self.progress["value"] = 25
                        self.editStatus('File transferred!', 3)
                    else:
                        self.editStatus('could not connect to host: %s; please try again or upload manualy' %self.entry_host.get(), 3)
                        self.terminator()
                        return 0
                    
                    """self.progress["value"] = 30
                    self.getFileFromHost = 0
                    if self.ftpHost() == 1:
                        self.progress["value"] = 50
                        self.editStatus('File transferred!', 3)
                    else:
                        self.editStatus('could not connect to host: %s; please try again or upload manualy' %self.entry_host.get(), 3)
                        self.terminator()
                        return 0"""

            # using uploaded file if self.xMode.get() == "2":
            else:
                self.removeStar(self.label_host)
                self.removeStar(self.label_user)
                self.removeStar(self.label_pw)
                try:
                    tmpFile = open(self.selectedFileName, 'r')
                    self.removeStar(self.upload_button)

                except:
                    isMissing = 1
                    self.addStar(self.upload_button)

                if isMissing == 1:
                    self.terminator()
                    return 0
                
                tmpFile.close()
                
            # is Authentication | Cookie checkbox is checked
            if self.isAuth.get() == 'y':
                if len(self.text_cookie.get()) < 1:
                    self.editStatus("No Cookie entered - Running in unauthenticated mode", 3)
                    self.checkbutton_auth.deselect()
                    
                else:
                    self.headers = { 'Cookie' : self.text_cookie.get(),  'User-Agent' : "Jakarta Commons-HttpClient/3.1" , 'Content-Type' : "application/octet-stream", 'Accept-Encoding' : "gzip" }
                    self.editStatus('Using Cookie: ' +self.text_cookie.get(), 3)

            # is Error Message checkbox is checked
            if self.isErrMsg.get() == 'y':
                if len(self.text_errMsg.get()) < 1:
                    self.editStatus("No Error Message entered - Ignoring...", 3)
                    self.checkbutton_errMsg.deselect()
                    self.text_errMsg.configure(state=DISABLED)
                else:
                    self.editStatus('Using self defined Error Message: ' +self.text_errMsg.get(), 3)
                    
            data = ''
            self.progress["value"] = 65
            self.editStatus('Starting file manipulation', 3)
            word_file = self.manipulateFile()
            self.progress["value"] = 85
            if word_file == 0:
                self.terminator()
                return 0
            
            word_file = self.localPath +'\\' +word_file
            myFile = open(word_file, 'r')
            self.word_list = myFile.read().split('\n')
            self.all_words_list = self.word_list
            myFile.close()
            
            self.progress["value"] = 90
            self.resultsFolder = self.localPath +'\\' +self.entry_host.get() +'_Results'
            # Create Results folder and files
            """if self.xMode.get() == '1':    
                resultsFolder = self.localPath +'\\' +self.entry_host.get() +'_Results'
            else:
                resultsFolder = self.localPath +'\\' +'_Results'"""
                
            # Creates 'Results' folder
            try:
                os.makedirs(self.resultsFolder)
                self.editStatus('Results folder created!', 3)
            except:
                self.editStatus('Results folder already exists.', 3)
      
            self.codesList = self.getCodeSelection()
            # create files for each desired Response Code
            ##DEBUG: listofCodes = [403]
            self.codeFilesList = []
            self.filesToClose = []
            for code in self.codesList:
                codeFile = '%s\\Res%s.txt' %(self.resultsFolder, code)
                createFile = open(codeFile, 'w')
                createFile.close()
                self.filesToClose.append(createFile)
                self.codeFilesList.append(codeFile)
                
            self.progress["value"] = 100
            self.totalLines = len(self.all_words_list)
            self.editStatus('Total lines in file: %d' %self.totalLines, 3)
            # number of reconnection times in case connection has been losts
            timestoTry = 12
            timesTried = 1
            
            #print type(skipLen)
            if self.isSkip.get() == 'y':
                try:
                    skipLen = string.atoi(self.text_skipLine.get())
                    if skipLen > 0 and skipLen < self.totalLines:
                        self.word_list =  self.all_words_list[skipLen -1:]
                        self.lineCounter = skipLen
                        self.editStatus('entering file from line #%d' %skipLen, 3)
                        
                                                
                    else:
                        self.editStatus('Error! line cannot be zero, or line to high', 3)
                        self.terminator()
                        return 0
                except:
                    if self.text_skipLine.get() == '':
                        self.editStatus('no line inserted, ignoring...', 3)
                    else:
                        self.editStatus('Error! illegal input', 3)
                        self.terminator()
                        return 0
                    
            else:
                self.progress["value"] = 0
            
        else:
            self.word_list = self.all_words_list
            self.word_list = self.word_list[self.lineCounter -1:]
             
        try:
            self.checkbutton_skipLine.deselect()
            self.text_skipLine.configure(state=DISABLED)
            self.reqFile = open(os.path.join(os.getcwd()) + '\\' +self.requestsFile, 'w')
            self.filesToClose.append(self.reqFile)
            self.myThread = threading.Thread(target=self.sendRequests, args=())
            try:
                self.myThread.start()
            except:
                print str(Exception)
            
        except:
            print Exception
            
    

#####################################################################################################################
###########################################         END OF RUN()       ##############################################
#####################################################################################################################
    def loc200(self):
        i = 0
        for code in self.codesList:
            if code == '200':
                return i
            else:
                i = i + 1

        return -1
        


    # receives:
    # list        -> list of URL to send
    # self.lineCounter -> number of line in file to start from
    # returns: current line number in file
    def sendRequests(self):

        self.runIn200Mode = self.loc200()
        
        for word in self.word_list:
    
            if self.stopThread == 1:
                #self.counter = counter
                return 1
            
            else:
                self.editStatus('Sending %d/%d' %(self.lineCounter, self.totalLines), 1)
                self.editStatus('Sent: %s' %(word), 5)
                self.lineCounter = self.lineCounter +1
                self.inProgress = (self.lineCounter / float(self.totalLines)) * 100
                self.progress["value"] = self.inProgress
            
                try:
                    myRequest = urllib2.Request(word, data=None, headers=self.headers)
                    myResponse = urllib2.urlopen(myRequest, timeout=5)
                       
                    ##DEBUG: print _response.getcode()
                    res_html = myResponse.read()
                    myResponse.close()

                    if myResponse.getcode() == 200 and self.runIn200Mode != -1:
                        if self.isErrMsg.get() == 'n' or (self.isErrMsg.get() == 'y' and self.findErrorMessage(res_html) == 0):
                            #self.editStatus(str('[%d] %s\n' %(myResponse.getcode(), word)), 4)
                            resFile = open(self.codeFilesList[self.runIn200Mode], 'a')
                            resFile.write(word +'\n')
                            resFile.close()
                            
                                        
                # not '200 OK'
                except urllib2.HTTPError as e:
                    i = 1
                    for code in self.codesList:
                        if e.code == code:
                            self.editStatus('[%s] %s\n' %(code, word), 4)
                            forbFile = open(self.codeFilesList[i], 'a')
                            forbFile.write(word +'\n')
                            forbFile.close()
                        else:
                            i = i + 1

                # server is not accepting requests
                except urllib2.URLError as e:
                    
                    """if errorStatus.find('unknown url type') != -1:
                        self.editStatus('ERROR! invalid URL: %s (line: %d)' %(word, counter), 3)
                        
                    elif errorStatus.find('Only one usage of each socket address') != -1:
                        self.editStatus('Connection terminated, to continue from the same location, Skip to line: %d' %self.lineCounter, 1)
                        
                    else:
                        self.editStatus('Error! server is not responding; stopped at line: %d, URL: %s\n' %(self.lineCounter, word), 1)"""
                    self.editStatus(str(e), 2)
                        
                    self.button_run.configure(state=NORMAL, text="Start", command=self.runPressed)
                    self.button_stop.configure(state=NORMAL, text="Quit", command=self.executeQuit)
                    return 0


                except Exception as e:
                    if str(e) == "unknown url type: ":
                        pass

        if self.lineCounter == self.totalLines or self.lineCounter -1 == self.totalLines:
            self.finito()
            return 1
        
        else:
            self.editStatus('errrr... something went wrong!', 3)
            self.button_run.configure(state=NORMAL, text="Start", command=self.runPressed)
            self.button_stop.configure(state=NORMAL, text="Quit", command=self.executeQuit)
            return 0


    # grand finale!
    def finito(self):
        self.startPressed = 0
        self.lineCounter = 0
        for file in self.filesToClose:
            file.close()
        self.editStatus('                 ', 2)
        self.editStatus('** !!! Mission accomplished !!! **', 3)
        self.editStatus('**********************************', 2)
        self.editStatus(' ', 2)
        self.isContinue = 0
        self.button_run.configure(state=NORMAL, text="Start", command=self.runPressed)
        self.button_stop.configure(state=NORMAL, text="Quit", command=self.executeQuit)


    # execution is done with something wrong...
    def terminator(self):
        self.startPressed = 0
        self.progress["value"] = 0
        self.isContinue = 0
        self.lastLocation = 0
        self.lineCounter = 0
        for file in self.filesToClose:
            file.close()
        self.button_run.configure(text="Start", command=self.runPressed)
        self.button_stop.configure(text="Quit", command=self.executeQuit)
    



    # returns list of  HTTP Status Codes selected by the user
    def getCodeSelection(self):
        i = 0
        selectedCodesList = []
        tmpList = self.listbox_codes.get(0, END)
        listLength = len(tmpList)
        for i in range(listLength):
            if self.listbox_codes.select_includes(i) == True:
                code = tmpList[i][1:4]
                #selectedCodesList.append(string.atol(code))
                selectedCodesList.append(code)
        self.editStatus('Using codes: ' +'; '.join(selectedCodesList), 3)
        return selectedCodesList


    # SSH to Host
    def sshHost(self):
        _fileName = 'locationOptions.txt'
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.entry_host.get() , port=22, username=self.entry_user.get(), password=self.entry_pw.get())
        except:
            return 0

        self.editStatus('SSH Connection established!', 3)
        
        if self.getFileFromHost == 1:
            if self.isFileOrFolder.get() == '_file':
                 self.ssh.exec_command("find . -type f -name %s > %s" %(self.text_findFile.get(), _fileName))
            else:
                 self.ssh.exec_command("find . -type d -name %s > %s" %(self.text_findFile.get(), _fileName))
                
            self.editStatus('file %s was created.' %_fileName, 3)

        else:
            self.editStatus('creating file...', 3)
            if self.isTraversal.get() == 'n':
                # create list of files from application home directory
                self.ssh.exec_command('cd ' +self.homeDir_TEXT +' ; ls -R > ~/' +self.targetFile +'\n')
            else:
                # create list of files from root
                self.ssh.exec_command('cd ; ls -R > ' +self.targetFile +'\n')
            
        self.editStatus('Establishing sFTP connection...', 3)
        if self.getFileFromHost == 1:
            _fileToDownload = _fileName
        else:
            _fileToDownload = self.targetFile
            
        try:
            self.sftp = self.ssh.open_sftp()
            self.editStatus('sFTP connection established successfully!', 3)
            self.sftp.chmod(_fileToDownload, 0755)
            time.sleep(1)
            self.sftp.get('./' +_fileToDownload, self.localPath + '\\' +_fileToDownload)
            #time.sleep(1)
            self.sftp.close()
        except:
            self.editStatus('Could not establish sFTP', 3)
            
        time.sleep(1)
        self.ssh.exec_command('cd; rm -f ' +_fileToDownload +'\n')  # comment in DEBUG mode
        self.ssh.close()
        
        return 1
    

    # manipulate the file received from host into compatible for requests
    def manipulateFile(self):
        if self.xMode.get() == '1':
            usingFile = self.localPath +'//' +self.targetFile
        else:
            usingFile = self.selectedFileName
        
        try:
            tmpFile = open(usingFile, 'r')
        except:
            self.editStatus('Error! file does not exist', 3)
            return 0
        
        self.progress["value"] = 68
        self.toExclude = 0
        
        ###########################
        # file type manipulations #
        ###########################
        if self.fileTypes.get() == '1':
            self.editStatus("Using Default 'File Types' settings.", 3)
            self.excludeTypes = [ '.gif', '.png', '.jpg', '.js', '.bmp', '.css']
            self.editStatus('Excluding: %s' %' ; '.join(self.excludeTypes), 3)
            flag = "n"
            self.progress["value"] = 73
        
        else: #manual
            flag = self.useListofFileTypes()
            if flag == "y":
                self.editStatus('Running on the following File Types only: ', 3)
                self.editStatus(', '.join(self.onlyTypes), 3)
                self.progress["value"] = 73
            else:
                self.toExclude = 1
                self.editStatus('Excluding the following File Types: ', 3)
                self.editStatus(', '.join(self.excludeTypes), 3)
                self.progress["value"] = 73

        dir = self.homeDir_TEXT +'/'
        fileName = 'url_list.txt'
        lines = tmpFile.read().split('\n')
        tmpFile.close()
        filePath = self.localPath +'//' +fileName
        newFile = open(filePath, 'w')

        # using uploaded (Ready) file                
        if self.xMode.get() == "2":
            if self.selectedFileName == filePath:
                newFile.close()
                newFile = open(self.localPath +'//tempFileName.txt', 'w')
            
            for line in lines:
                self.toExclude = self.typesManipulations(line, flag)
                if self.toExclude == 0 and line != '' and line != '\n':
                    newFile.write(line +'\n')
                    
            newFile.close()        
            try:
                if self.selectedFileName == filePath:
                    os.remove(filePath)
            except:
                pass
                
            os.rename(filePath, self.localPath +'//' +fileName)            
            
            return fileName

        # Application files only....
        elif self.isTraversal.get() == 'n':
            folder = '/'
            self.toExclude = 0
            for line in lines:
                if line != '' and line != '\n':
                    if line.find(':') != -1:
                        line = line.replace(':', '/')
                        folder = line[1:]
                        #newline = self.URL_TEXT +folder
                        #self.toExclude = 0
                    else:
                        self.toExclude = self.typesManipulations(line, flag)
                        newline = self.URL_TEXT +folder +line

                        if self.toExclude == 0:

                            newFile.write(newline +'\n')
                        else:
                            self.toExclude = 0
                
            newFile.close()
            return fileName
            
        else:
            isFolder = '/'
            lenURL = len(self.URL_TEXT)
            self.progress["value"] = 75
            newFile.write(self.URL_TEXT +'/../../../../../../../../../../../../../../../../../../../../../etc/passwd\n')

            # Creating list of home directories
            #if self.isTraversal.get() == 'y':
            origDepth = dir.count('/')
            self.depth = origDepth -1
            myDirList = self.homeDir_TEXT.split('/')
            listLen = len(myDirList)
            tmpFolder = ''
            ##DEBUG: print tmpList
            for folder in myDirList:
                tmpFolder = tmpFolder + folder + '/'
                self.folderList.append(tmpFolder)
            self.progress["value"] = 77
                
            for line in lines:
                # is Folder line
                if line.find(':') != -1:
                    line = line.replace(':', '/')
                    line = line[1:]
                    if line.find(dir) != 0:
                        ##DEBUG: print 'traversal >> ' +isFolder
                        isFolder = '/' +self.traversalManipulation(line)
                        line = isFolder
                    else:
                        location = len(dir)
                        rest = line[location:]
                        isFolder = line
                        
                    ## selected files only
                    if flag == 'y':
                        self.toExclude = 1
                    else:
                        self.toExclude = 0

                # is Empty line
                elif line == '\n' or line == '':
                    self.toExclude = 1

                # is File line    
                else:
                    self.toExclude = self.typesManipulations(line, flag)
                    line = isFolder + line
                    
                if self.toExclude == 0:
                    newFile.write(self.URL_TEXT +line +'\n')
                else:
                    self.toExclude = 0

            newFile.close()
            self.progress["value"] = 80
            
            return fileName



    # remove unrelevant file types from selected requests file
    def typesManipulations(self, line, flag):
        if flag == 'y':
            x = 0
            for _type in self.onlyTypes:
                if line.find(_type) != -1:
                    x = 1
            if x == 0:
                return 1
            else:
                return 0
            
        else:
            for type in self.excludeTypes:
                if line.find(type) != -1:
                    return 1
            return 0
        



    # adds File Types exclude/use-only
    def useListofFileTypes(self):
            if self.useTypes.get() == "2": #use only types
                if self.is_cb_archive2.get() == "y":
                    tmpTypes = ['.zip', '.rar', '.tar', '.tar.gz']
                    self.onlyTypes.extend(tmpTypes)

                if self.is_cb_documents2.get() == "y":
                    tmpTypes = ['.xml', '.doc', '.xls', '.ppt', '.pdf', '.txt', '.log']
                    self.onlyTypes.extend(tmpTypes)

                if self.is_cb_java2.get() == "y":
                    tmpTypes = ['.java', '.class', '.jar', '.war', '.ear']
                    self.onlyTypes.extend(tmpTypes)

                if self.is_cb_web2.get() == "y":
                    tmpTypes = ['.php', '.jsp', '.html', '.aspx', '.js']
                    self.onlyTypes.extend(tmpTypes)

                if self.isFreeTextTypes2.get() == "y" and len(self.only_freeText.get()) > 1: #
                    _types = self.only_freeText.get().replace(' ', '')
                    tmp =_types.split(',')
                    tmpTypes = []
                    for type in tmp:
                        type = '.' +type
                        tmpTypes.append(type)
                    self.onlyTypes.extend(tmpTypes)
                    
                return 'y'
                    
            else: #exclude types (self.useTypes.get()=="1")
                if self.is_cb_graphics.get() == "y":
                    tmpTypes = ['.gif', '.png', '.jpg', '.bmp']
                    self.excludeTypes.extend(tmpTypes)

                if self.is_cb_archive.get() == "y":
                    tmpTypes = ['.zip', '.rar', '.tar', '.tar.gz']
                    self.excludeTypes.extend(tmpTypes)

                if self.is_cb_documents.get() == "y":
                    tmpTypes = ['.xml', '.doc', '.xls', '.ppt', '.pdf', '.txt', '.log']
                    self.excludeTypes.extend(tmpTypes)

                if self.is_cb_java.get() == "y":
                    tmpTypes = ['.java', '.class', '.jar', '.war', '.ear']
                    self.excludeTypes.extend(tmpTypes)

                if self.is_cb_web.get() == "y":
                    tmpTypes = ['.php', '.jsp', '.html', '.js', '.aspx', '.css']
                    self.excludeTypes.extend(tmpTypes)
                
                if self.isFreeTextTypes.get() == "y" and len(self.exclude_freeText.get()) > 1:
                    _types = self.exclude_freeText.get().replace(' ', '')
                    tmp =_types.split(',')
                    tmpTypes = []
                    for type in tmp:
                        type = '.' +type
                        tmpTypes.append(type)   
            
                    self.excludeTypes.extend(tmpTypes)
                return 'n'



    # adds required amount of ../ to request
    def traversalManipulation(self, line):
        newStr = ''
        tmpTXT = '../'
        isFound = 0
        for i in range(self.depth , -1, -1):
            if line.find('/' +self.folderList[i]) == 0:
                isFound = 1
                break;
            
        if isFound == 0:
            for j in range(self.depth +1):
                newStr = newStr + tmpTXT

            folderName = newStr
            ##DEBUG: print "No folder found! returning: >> " +folderName
            return folderName

        else:
            location = len(self.folderList[i])
            ##length = len(_line)
            rest = line[location +1:]
            ##DEBUG: print 'REST >> ' +rest
            self.progress["value"] = 83
            for i in range(self.depth -i):
                newStr = newStr + tmpTXT

            folderName = newStr +rest
            ##DEBUG: print 'FOUND! [%s]; returning: %s (%d)' %(_folderList[i], folderName, newStr.count('/'))
            return folderName



    # receives an Error message and a string
    # returns:
    # 0 - if error message was not found in string
    # 1 - if found
    def findErrorMessage(self, str):
        if str.find(self.text_errMsg.get()) == -1:
            return 0
        else:
            return 1



    # if '1' is passed - print String to Status
    # if '2' is passed - print String to Log Tab
    # if '3' is passed - 1 + 2
    # if '4' is passed - print String to Results Tab
    # if '5' is passed - print String to Results file
    # if '6' is passed - print String to debug file
    # if 'else' is passed - print String to I/O
    
    def editStatus(self, newStatus, toLog):
        if toLog == 1:
            self.text_status.configure(state=NORMAL)
            self.text_status.delete(1.0, END)
            self.text_status.insert(END, newStatus)
            self.text_status.configure(state=DISABLED)
            
        elif toLog == 2:
            self.log_text.configure(state=NORMAL)
            self.log_text.insert(END, newStatus +'\n')
            self.log_text.configure(state=DISABLED)

        elif toLog == 3:
            self.text_status.configure(state=NORMAL)
            self.text_status.delete(1.0, END)
            self.text_status.insert(END, newStatus)
            self.text_status.configure(state=DISABLED)
            self.log_text.configure(state=NORMAL)
            self.log_text.insert(END, newStatus +'\n')
            self.log_text.configure(state=DISABLED)  

        elif toLog == 4:
            self.results_text.configure(state=NORMAL)
            self.results_text.insert(END, newStatus +'\n')
            self.results_text.configure(state=DISABLED)

        elif toLog == 5:
            self.reqFile.write(newStatus +'\n')

        elif toLog == 6:
            try:
                file = open('debug.txt', 'a')
            except:
                file = open('debug.txt', 'w')
            file.write(newStatus + '\n')
            file.close()
            self.text_status.configure(state=NORMAL)
            self.text_status.delete(1.0, END)
            self.text_status.insert(END, newStatus)
            self.text_status.configure(state=DISABLED)
            self.log_text.configure(state=NORMAL)
            self.log_text.insert(END, newStatus +'\n')
            self.log_text.configure(state=DISABLED) 

        else:
            print newStatus +'\n'
            

    # receives an object to color in RED
    def addStar(self, obj):
        obj.configure(foreground='red')

    # receives an object to color in BLACK
    def removeStar(self, obj):
        obj.configure(foreground='black')



    # 'Quit' button clicked
    def executeQuit(event=None):
        root.destroy()




root = Tk()
root.title("Path Traverser v1.3")
# use ico (top-left)
ico_encoded = "AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAAMMOAADDDgAAAAAAAAAAAADulDn/7pQ5/+6UOf+srt7/OT2o/2Bbvf+MjtP/t7zj/+6UOf/ulDn/7pQ5/+6UOf/ulDn/7pQ5/+6UOf/ulDn/7pQ5/+6UOf/ulDn/7pQ5/2ZmvP8PEJn/FBKe/yYnp/9CQbL/amzA/52c1P/Fw+T/7pQ5/+6UOf/ulDn/7pQ5/+6UOf/ulDn/7pQ5/+6UOf/ulDn/NDOp/xIUoP8UEp//EhGd/xENnP8YFZz/JCOm/4N9w//ulDn/7pQ5/+6UOf/ulDn/7pQ5/+6UOf+Zl9b/7pQ5/5GQ0f8XGZ3/FhWf/xcXn/8XF57/FRSg/xAPnP+Cg8v/7pQ5/+6UOf/ulDn/7pQ5/+6UOf/ulDn/LjKn/+6UOf/ulDn/VFW1/xQTm/8XFp7/FxWe/xYVn/8fHKD/qqvY/+6UOf8WFp7/eHnF/+6UOf/ulDn/7pQ5/yckov9JTK7/7pQ5/6yw4P8iJKL/FRSe/xYUoP8SE53/Pz6r/+6UOf+ys97/tbLZ/xYWnv/ulDn/7pQ5/+6UOf8nJ6H/S0u1/+6UOf/ulDn/cHLC/xYVnv8UFZ3/GRme/5KW1f/ulDn/7pQ5/xYWnv+GhMn/7pQ5/+6UOf/ulDn/KCal/zMzrP+GiMv/hojQ/0hKtP8REZ3/Ghqe/3+CzP/ulDn/7pQ5/+6UOf/ulDn/ub3k/+6UOf/ulDn/7pQ5/zMup/8ZFZz/FxSb/xcUnf8hH6H/TlC0/6am2f/0nW//g4PM/42Tz/8WFp7/7pQ5/+6UOf/ulDn/7pQ5/+6UOf/ulDn/7pQ5/+6UOf/ulDn/7pQ5/+6UOf/ulDn/Zme+/+6UOf+/vOH/rqvb/7q74f/ulDn/7pQ5/+6UOf/ulDn/oKjX/6mp2f+fpdX/k5LR/3l3yf9bXr//bWjC/7i04P/ulDn/7pQ5/x0doP93dsT/7pQ5/+6UOf/ulDn/Y1+6/xkYn/9LSK//V1u6/2xkwP+Jic3/Fhae/+6UOf+Jjs3/Fhae/+6UOf/ulDn/Fhae/+6UOf/ulDn/mZfW/xgZnv9LULj/qKXa/4mCzf/ulDn/jpHO/xYWnv/ulDn/T1W3/xwXnv+Rkcr/7pQ5/+6UOf/ulDn/vrzl/y80q/8VFZ3/o6ba/4B/yv87Oq7/7pQ5/25xwv8WFp7/7pQ5/+6UOf9DRrP/sK7c/+6UOf/ulDn/7pQ5/4F1yP8gHaH/S0y0/+6UOf9MU7T/JySn/+6UOf/ulDn/Gxig/2lnwP/ulDn/7pQ5/+6UOf/ulDn/7pQ5/+6UOf8WFp7/Fhae/+6UOf/ulDn/aWfA/1NVt/9pZ8D/7pQ5/+6UOf/ulDn/7pQ5/+6UOf/ulDn/7pQ5/+6UOf/ulDn/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=="
ico_decoded = base64.b64decode(ico_encoded)
temp_file = "pt.ico"
fout = open(temp_file,"wb")
fout.write(ico_decoded)
fout.close()
root.wm_iconbitmap(temp_file)
#remove temp file
os.remove(temp_file)

app = App(root)

root.mainloop()
