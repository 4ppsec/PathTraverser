
    #######################################################
    ## REGISTRED UNDER OWASP:   http://sl.owasp.org/pt   ##
    ## CREATED BY:              TAL MELAMED              ##
    ## CONTACT:                 PT [AT] APPSEC [DOT] IT  ##
    #######################################################

    ############################### DISCLAIMER ###############################
    ##                                                                      ##
    ## * Please be advised that this tool should not be used                ##
    ##   against any product/ service not owned by the individual           ##
    ##                                                                      ##
    ## * Any data/ financial loss that might be caused by improper use      ##
    ##   or abuse of this tool is under the liability of the perpetrator    ##
    ##                                                                      ##
    ## + Security Note: no input validations are used due to the need of    ##
    ##   credentials to access the attacked host. Any actions performed     ##
    ##   will take place under the provided user                            ##
    ##                                                                      ##
    ##########################################################################

from Tkinter import *
import threading
import Tkinter, tkFileDialog, ttk, tkFont, tkMessageBox
import os, base64, time, string
import urllib2, paramiko
from datetime import datetime
import webbrowser


class App:
    
    def __init__(self, master):
        # vars #
        self.hostURL            = StringVar()
        self.isTraversal        = StringVar()
        self.xMode              = StringVar()
        self.isAuth             = StringVar()
        self.isFind             = StringVar()
        self.isFileOrFolder     = StringVar()
        self.selectedFileName   = StringVar()
        self.isErrMsg           = StringVar()
        self.isFindMsg          = StringVar()
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
        self.pathEncoding       = StringVar()

        self.inProgress         = 1.0
        self.startPressed       = 0
        self.isHelped           = 0
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
        self.listofSessions     = []
        self.filesToClose       = []
        self.config             = 0
        self.p_c                = "c" 
        
        self.localPath = os.path.join(os.getcwd())
        self.savedFileName = 'pt.ini'
        self.targetFile = 'listofFiles.txt'
        self.requestsFile = 'requestsLog.txt'

        self.logoB64 = "R0lGODlhewFZAHAAACH5BAEAACcALAAAAAB7AVkAhQAAALVKSpwpGZwZEJwQGZwQEL1zc5wQAKUQCJwAAL2ttb1Ka8WEhJwxQr0ZKXsIAJxSQsVKKcWtlMV7UpylpZSElEpSShkpGRAQEDoxKUIxQhAxQmt7c2NSawAQAGtaQmt7UsW1xQAICJyljM7OzpzOrWt7lAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAb/wJNwSCwaj8ikcslsOp/QqHRKrVqv2Kx2yw14v+AAd0wum8/otHrNLg4K8Hjc0K7b7/i8fg81HAp0RwUIAwRycIFFCQUHiXyPkJGSk3cBA4sIBQlIAgQEmQKEcEiDcItilKmqq6ytQ28FAnCFBUgGCASdnp4DpHGwCQkKrsTFxsdaC4efnqWkuMyhtUe4sgWGbwebyNzd3t4McaG5BIWhDIKx5KDPnuOGCOjf8/T1kw3QndWZCA1H+J6qfeIUKx8CWfYSKlzYpsCAfLvKITgSQN0uBI6IJNj1rhzDjyBDXmEALWA5Qw6NkBxkrYA8IyxLZkrSS6TNmzbxherUcVqR/2smfcLUxZOAP2qaUOFcypQeUGbuMmU8kUCWu21GCjErJbQILlhNw4o1dktrKK0IsA4BOM4BkgQHyXlSS+QPSk1j8+qlxCviQThKX+GCcxSm34HpxnW6NHWv48dr9skVZURggcAa4ZBDmC4qygGYIYse3UUgVAIJMvptfIIls36+3ukCTLq2bSyZPhUFSySmS1IB9SF5UPJ1qMK3kyt3Ijf4KCJW8T7rRNtIAIFxqYdezr27xpO6PnXd8iYaM7re03vfaRzOSy4QoY1XT3957vCEkGtZJDtX/f/pQRUXArBxMYhf2xHBGoAMMqVOeOIdkokpCQywoC34DJLgEA8koP9fgyAuhcuIOx2i2Sx3pQQFIEuUQkiIMC6Fj1YXUafZbCedWN0VFTnkSYxA2lQSe1DpoxsthrREYAIQVGHAgeKhF+SU9RA4oYRymIfWYp9MKMVK5sBzIZVk3pQhUH/FkdqKaOn2XJlw5hWAA9SdlEkCG/Z2IISZ1BTnn2M5cKCJSghaUHAovQfookwx0CMcdy4IwWD6sMjopWMxkGE5piShSz+KYipqU4tE6CdMY46qqkgkGfLJmqvGOlpFV+Yp6616OCoALIcc8IeJhNg61C9PNGAprsiSscg1JjZ7413CDnGdVbYycImXyWa7xTWF/MVpLszqY2SKsC5hQEDH/gT/pUMTaevuFa4FN2JfptXJLLFMbISIdeKU9O6/VDwVlzu5ZHdRkV8xW24S7B4giGz7AiyxE4PQOOBhSW4mk0TiMZEbeuEEldbEJLcYFYQnFTzukM1Zs3A6l1UWpixSlmwzlPLqQiPB5Fwzb7fg/qaENSo1AIbRNif9E08DuyMAnQ04EEHURhpM1GvSEfSm0ly3iPNB8SxRkUnMmAWPipx8EmrXbA9Rb0CpngBQ02h+Ot8Qnbatd2/8+LU2EhFF9KlVCyix495tGxTd39YR6Vd4jCwYB+J7axZ42E1YHniNOSqxSNyUv+sthIwTMXZzgpuELRIzGWHAJQ6H/q5mxREg/wETTzK7OefrML6IIpCiLXu25kGDERM61b57pVlT0yTemg/vruafli4Ey7uvI1fMpKiVfCfSawv2OINN4HXK2XMU0EN3CyFUyJ98GH6s1DdjPRzjqr/8LtwLghkDBmhABOaXLIOgq3Qb0c3lsvez1v1DfgTMFqR4hrkjyAJlglPeZDyShJpFEFkGc5PktrI5iJSwZxvy4AdvNcGBHU8Q2Ancp9JnEg8GAHQrxJQJOwYcBS6QhuDZWlaGwIBFaEMbwUjAAQqUwz9N0FUCSMIDmqNBIL6GAIVjnenigAoJwCIt1qMAE8QYhWE8pgKIM9g1khAA1WHQihyBg/lIQYRwvP/hPQzARvuEAAALLAEAgAykIAc5yCFcgJAAwAASEHmBJiDykYUUQgYwAEkAZICMT7AkEixASUJqAAkUIKQiD1lJQBbhAp18ZAacYIFHFgEDqYTkKomwgVL68QwHwsUAGTawN8LxNO1zRDjgcDsFDeZURQglAJSggECiEpakBOQzY2mEQCryj4HMJCApiYELRDORlPxmNQNJAQpwIAPOfAIHErkEdGZzCesEABqJkEoLWKAD9uzkEZQJgAtQoAIV8EAgb5kEQBL0BB9gpxGaOVB8dsCdmCSCIDvwTxAIkgNmGAwB8gQXz/wyeztRoYIgNZWCeLCVfUwCBQ46BGsaIZT/4zQlNmXKhBBc85XvJEIzY4rRISR0m07oZESPIEgzJgGdNx2CO5dphFnGtAgo1SQSkGqEDiR1CPxs5CmHKoSo4hSQXM2COJQAPwN+NHvpSsKTDFFM6DSjoEDd5CJzSgSWnsClM2UqE0BgVHrSFasx7cApAzkCR/7VCKmcJ1yP4FUjaDWmfb3rYVsKgLBeVQj8vOwJFEuEChxWkGX4hK18VhQaPoWBSmrC6wYxlTY2r66CDKsSAukBJ4B2Cam8Qm4NCwAQxFSzUC1qXpVQS73Clqa8HSo/7XoCiB5BsC/FaxM6cNioFnYM/UPCpNDkw811ZH8KRKYtRhSqGd1tkI+1/21cmSBduCJ3CtFUb0q/aty5BhK6SUhlZCUKgE82dbLu5WognUoEUqZ3CZlV52HjOV8upMo1pU2fL3lniCbkMWKmM8TfUgpg99bXw0zYbRVEjFtA4lep60XCOjnAYHim8wgM3WSHiQrWmDKXujVuQoKd0OIiMFSed4iDgCRsngmDjQCq/UuoIDVXPgKSs+ydMX8VqgQST8HK7j2xJE1c4hP8+LogpjFzT9BY+e5XqPYF8hjb6+L3noCfeDDJ1RiIsRLOpl1LuDAC2iqE3LFGpvHVppvTHGIpF3rQR+ikbwcLgP0WQaFsNkJUHQ3IEMgY0fYVMKa/2VMl7LgJnnWzMv8JzAYCzfC0QJywD5OsYa+kdQjrhDU5BQ3c30YZ00E1tJMBoGXJ+je/lRVCj2dbXUxrYLKdfjQg9/vkJPwYkKSOborb/GGU3uFcT1E1nZWHH9XOQQgQgACeiD3laIf51qUkpG51fYJOstTa2JzymIegX2WTIAlRhaW+KSnbWRe4n0sIdaSJwE9w7vvDwj4sJaG8Bkh996xGloa3M4GOIoo01ERYKq3l20eH2vOeII8qwqGAZfsSOJS1HoJnD3rbJAg82aE8cBGODW0LaMDmmA4kZ9dpbkkT0tL7FKQ9b+5OFQeyr+jstRqop7wqHkwx6ivALi2MEj4v4ZARXS7H5Zv/ciGUHAqBPrRBYYlrykaUwQxXNnJzfOkPj1yy1iwzExgM4E+31OjWxIA7k92GPlURZXM+rTQKkMUohIPi2rQ1b7tO2bK3m93AdvyuE5mBpc6bsjHt+RBwHGw+dl3umPUwBjSQStmmeeR25yPe+6lvyG8BIDTcB/meTqCN4vAIudtjETgPya0vXuzrlvzjAdBpBoOZsem+tVZDmfbjvp3GxtU42FtO8BeDmq4DP8Ojdpa60zCtKLdXwlpfPVeG81PzU2b85NEd/OdP+cTUH2cJfD5txL7T8dI385RrCwVBmj/7z0VXz9YGA1AI3Ec2AkEdBEJ4ZPAkiLdmIxd2xCZ8//GXaK5ngcJHSR6gZRUoBAkFXB2odhTQTOjXVa53dNVXfzN1WamnBAJXBEvFd2ZAKxYhQwRjJQ4QANZjBbfQakxwSM0XVUqnduoHd4z3dU+AhGrHdwxmbs2GfI4ndO5ngsK3a0MlhP0nTdJGZXOncP6GBqCwO/NSDW6xBqtVABCkbBPIeCGoeFV2gfaXgQZlBAwmc7jWhglnfUpAc1M4ZVy1VCbgWEhASjLYgkkwbFPWh1bwEGXDEWDDRG2gDJkgLEV3VF9oX0WIh+tnBUr4ftCnZkJwSJeniXAHAEC3BKCnVNAXVhU4cvq0hcAVbYiIVaRYBa0iF4MXAIV3BxAQC//CgwSUJINq5361WIrsx4nsNmBpBmZsdwQmMFCoyG75B4PQl3YF11edp2yaVXDPJYOpuGWAtAFm4ABA4yrRogZ9E0UuGIWXGFN9yI3DZQXCdWu1NlFkxo7NKG3NF4fvFUqFCI1HQHeYlI91J0hXtU6ahmlLpYhQ0Iv4c45muAAMMJEGUJEBMEfBBUjCmIi8NlVCxwQLOYShKHSmtwS8dwEK4GhCEAKcBmKBFIhvqHMqKVk8lm5Q9mygmEyCdElGSHRz6JGltIVcuHskSR43NA8U0AEVUE4KYE+exmIcUAEgoJRQVU5WyQEd8AFIUAEWMAJWaU73ZARc+ZXm9AEiiQRoCtABJvCVFYCVKkZRVqkAHPABY2ZOGMVi5rRo+xSVFtCWFhCVoLSRUMUBCmCVHTACHYCVUDmYZMmVzdeWiqlUGeBNN+dyh/mViYmVFXCYMLl5giVG5eSUW6mUidlEpnmaqJmaqjkPQQAAOw=="

        self.tabs =  ttk.Notebook(root)
        tab_main = ttk.Frame(self.tabs, width=650, height=550)
        tab_main.bind("<Expose>", self.DemoTabSelected)
        tab_conf = ttk.Frame(self.tabs)
        tab_log = ttk.Frame(self.tabs)
        tab_res = ttk.Frame(self.tabs)
        tab_res.bind("<Expose>", self.ResTabSelected)
        tab_help = ttk.Frame(self.tabs)
        tab_about = ttk.Frame(self.tabs)
        tab_sessions = ttk.Frame(self.tabs)
        tab_sessions.bind("<Expose>", self.SessionTabSelected)
        tab_conf = ttk.Frame(self.tabs)

        self.tabs.add(tab_main, text="     Main     ")
        self.tabs.add(tab_conf, text=" Configuration ")
        self.tabs.add(tab_res, text="    Results    ")
        self.tabs.add(tab_log, text="      Log      ")
        self.tabs.add(tab_sessions, text="  Sessions  ")
        self.tabs.add(tab_about, text="    About    ")

        self.tabs.pack()

        ########## TOP Manue Bar #########

        self.menu = Menu(tearoff=False)
        root.config(menu = self.menu)
        
        self.filemenu = self.file_menu = None
        self.filemenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='File', menu = self.filemenu)
        self.filemenu.add_command(label='Run', command=self.executeRun)
        self.filemenu.add_command(label='Pause / Continue', command=self.pause_continue, state="disabled")
        self.filemenu.add_command(label='Stop', command=self.stopPressed, state="disabled")
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Upload File', command=self.browseFile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Save Session', command=self.executeSave)
        self.filemenu.add_command(label='Clear Data', command=self.clearData)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Quit', command=self.executeQuit)

        logmenu = self.conf_menu = None
        logmenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='Logs', menu =  logmenu)
        logmenu.add_command(label='Clear Log', command=self.clearLog)
        logmenu.add_separator()
        logmenu.add_command(label='Clear Results', command=self.clearResults)
        
        helpmenu = self.conf_menu = None
        helpmenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='Help', menu =  helpmenu)
        helpmenu.add_command(label='About', command=self.openAboutPopup)


        ###############################################################################
        ## Configuration TAB:                                                         #
        #  This tab represents the UI of the main frames within the configuration tab #
        ###############################################################################
        
        # Configuration Option 1
        self.conf_1 =  Label(tab_conf, text="File Type Configuration")
        self.conf_1.place(bordermode=OUTSIDE, x=35, y=25)
        self.demo_1 = Button(tab_conf, text="+", bd=1, cursor="hand1", command=self.expandConfiguration_1)
        self.demo_1.place(bordermode=OUTSIDE, x=10, y=25)
        self.miniframe_1 = Frame(tab_conf, width=600, height=300)

        # Configuration Option 2
        self.conf_2 =  Label(tab_conf, text="Find  File/ Directory in Host server")
        self.conf_2.place(bordermode=OUTSIDE, x=35, y=60)
        self.demo_2 = Button(tab_conf, text="+", bd=1, cursor="hand1", command=self.expandConfiguration_2)
        self.demo_2.place(bordermode=OUTSIDE, x=10, y=60)
        self.miniframe_2 = Frame(tab_conf, width=600, height=275)

        # Configuration Option 3
        self.conf_3 =  Label(tab_conf, text="Select Logged HTTP Response Codes (hold Ctrl for multiple selection)")
        self.conf_3.place(bordermode=OUTSIDE, x=35, y=95)
        self.demo_3 = Button(tab_conf, text="+", bd=1, cursor="hand1", command=self.expandConfiguration_3)
        self.demo_3.place(bordermode=OUTSIDE, x=10, y=95)
        self.miniframe_3 = Frame(tab_conf, width=600, height=270)
        
        # Configuration Option 4
        self.conf_4 =  Label(tab_conf, text="Find/ Ignore string(s) in response")
        self.conf_4.place(bordermode=OUTSIDE, x=35, y=130)
        self.demo_4 = Button(tab_conf, text="+", bd=1, cursor="hand1", command=self.expandConfiguration_4)
        self.demo_4.place(bordermode=OUTSIDE, x=10, y=130)
        self.miniframe_4 = Frame(tab_conf, width=600, height=300)

        # Check Button: Error Msg
        self.checkbutton_errMsg = Checkbutton(self.miniframe_4, text="  Ignore the response if found: ",
                                              variable=self.isErrMsg, onvalue="y", offvalue="n", command=self.useErrMsg)        
        self.checkbutton_errMsg.place(bordermode=OUTSIDE, x=50, y=50)
        self.checkbutton_errMsg.deselect()

        # TEXT: Error Msg
        self.text_errMsg = Entry(self.miniframe_4, width=75, state=DISABLED)
        self.text_errMsg.place(bordermode=OUTSIDE, x=55, y=85)

        self.checkbutton_findMsg = Checkbutton(self.miniframe_4, text="  Accept response only if found: ",
                                               variable=self.isFindMsg, onvalue="y", offvalue="n", command=self.useFindMsg)
        self.checkbutton_findMsg.place(bordermode=OUTSIDE, x=50, y=165)
        self.checkbutton_findMsg.deselect()

        # TEXT: Find Msg
        self.text_findMsg = Entry(self.miniframe_4, width=75, state=DISABLED)
        self.text_findMsg.place(bordermode=OUTSIDE, x=55, y=200)

        # status codes frame
        self.codeFrame = Frame(self.miniframe_3)
        self.codeFrame.place(bordermode=OUTSIDE, x=25, y=25)

        # Scroll Bar
        self.codeScrollBar = Scrollbar(self.codeFrame)
        self.codeScrollBar.pack(side=RIGHT, fill=Y)

        # List of HTTP STATUS CODES
        self.listbox_codes = Listbox(self.codeFrame, selectmode=EXTENDED, width=50, height=14,
                                                     exportselection=0, yscrollcommand=self.codeScrollBar.set)
        listofCodes = [
                "200   	OK",
                "100   	Continue",
                "101   	Switching Protocols",
                "102   	Processing",
                "201   	Created",
                "202   	Accepted",
                "203   	Non-Authoritative Information",
                "204   	No Content",
                "205   	Reset Content",
                "206   	Partial Content",
                "207   	Multi-Status",
                "208   	Already Reported",
                "226   	IM Used",
                "300   	Multiple Choices",
                "301   	Moved Permanently",
                "302   	Found",
                "303   	See Other",
                "304   	Not Modified",
                "305   	Use Proxy",
                "307   	Temporary Redirect",
                "308   	Permanent Redirect",
                "400   	Bad Request",
                "401   	Unauthorized",
                "402   	Payment Required",
                "403   	Forbidden",
                "404   	Not Found",
                "405   	Method Not Allowed",
                "406   	Not Acceptable",
                "407   	Proxy Authentication Required",
                "408   	Request Timeout",
                "409   	Conflict",
                "410   	Gone",
                "411   	Length Required",
                "412   	Precondition Failed",
                "413   	Payload Too Large",
                "414   	URI Too Long",
                "415   	Unsupported Media Type",
                "416   	Range Not Satisfiable",
                "417   	Expectation Failed",
                "421   	Misdirected Request",
                "422   	Unprocessable Entity",
                "423   	Locked",
                "424   	Failed Dependency",
                "426   	Upgrade Required",
                "428   	Precondition Required",
                "429   	Too Many Requests",
                "431   	Request Header Fields Too Large",
                "500   	Internal Server Error",
                "501   	Not Implemented",
                "502   	Bad Gateway",
                "503   	Service Unavailable",
                "504   	Gateway Timeout",
                "505   	HTTP Version Not Supported",
                "506   	Variant Also Negotiates",
                "507   	Insufficient Storage",
                "508   	Loop Detected",
                "510   	Not Extended",
                "511   	Network Authentication Required"
                        ]
        for item in listofCodes:
            self.listbox_codes.insert(END, item)
        self.listbox_codes.pack()
        self.listbox_codes.select_set(0)
        self.codeScrollBar.configure(command=self.listbox_codes.yview)

        self.button_conf_default = Button(self.miniframe_1, text=" Restore to Default ", command=self.restoreDefaultConfiguration, state=DISABLED)
        self.button_conf_default.place(bordermode=OUTSIDE, x=285, y=270)

        # File types: Enable
        self.radiobutton_fileTypeEnable = Button(self.miniframe_1, text='Enable', command=self.enableTypes)
        self.radiobutton_fileTypeEnable.place(bordermode=OUTSIDE, x=210, y=270)

        # Exclude types
        self.radiobutton_excludeTypes = Radiobutton(self.miniframe_1, text='Exclude the following File Types: ',
                                                    command=self.useFileTypes, variable=self.useTypes, value='1', state=DISABLED)
        self.radiobutton_excludeTypes.place(bordermode=OUTSIDE, x=25, y=10)
        self.radiobutton_excludeTypes.select()

        # Use only types
        self.radiobutton_useOnlyTypes = Radiobutton(self.miniframe_1, text='Use only to following File Types: ',
                                                    command=self.useFileTypes, variable=self.useTypes, value='2', state=DISABLED)
        self.radiobutton_useOnlyTypes.place(bordermode=OUTSIDE, x=300, y=10)

        # CheckButton types to exclude:
        self.cb_graphics = Checkbutton(self.miniframe_1, text='gif, png, jpg, bmp', state=DISABLED,
                                         variable=self.is_cb_graphics, offvalue='n', onvalue='y')
        self.cb_graphics.place(bordermode=OUTSIDE, x=45, y=50)
        self.cb_graphics.select()

        self.cb_documents = Checkbutton(self.miniframe_1, text='xml, txt, doc, xls, ppt, pdf', state=DISABLED,
                                         variable=self.is_cb_documents, offvalue='n', onvalue='y')
        self.cb_documents.place(bordermode=OUTSIDE, x=45, y=75)
        self.cb_documents.deselect()

        self.cb_archive = Checkbutton(self.miniframe_1, text='zip, rar, tar, tar.gz', state=DISABLED,
                                         variable=self.is_cb_archive, offvalue='n', onvalue='y')
        self.cb_archive.place(bordermode=OUTSIDE, x=45, y=100)
        self.cb_archive.deselect()

        self.cb_web = Checkbutton(self.miniframe_1, text='php, jsp, html, aspx, js', state=DISABLED,
                                         variable=self.is_cb_web, offvalue='n', onvalue='y')
        self.cb_web.place(bordermode=OUTSIDE, x=45, y=125)
        self.cb_web.select()

        self.cb_source = Checkbutton(self.miniframe_1, text='c, cpp, dba, cs, py, vb', state=DISABLED)

        self.cb_java = Checkbutton(self.miniframe_1, text='java, class, jar, war, ear', state=DISABLED,
                                         variable=self.is_cb_java, offvalue='n', onvalue='y')
        self.cb_java.place(bordermode=OUTSIDE, x=45, y=150)
        self.cb_java.deselect()
        
        self.cb_freeText = Checkbutton(self.miniframe_1, text='Others (type1, type2, type3):', state=DISABLED,
                                       variable=self.isFreeTextTypes, offvalue='n', onvalue='y', command=self.allowFreeTextTypes)
        self.cb_freeText.place(bordermode=OUTSIDE, x=45, y=190)
        self.cb_freeText.deselect()
        
        self.exclude_freeText = Entry(self.miniframe_1, width=30, state=DISABLED)
        self.exclude_freeText.place(bordermode=OUTSIDE, x=52, y=225)
        

        # CheckButton types to test (only):
        self.cb_graphics2 = Checkbutton(self.miniframe_1, text='gif, png, jpg, bmp', state=DISABLED)

        self.cb_documents2 = Checkbutton(self.miniframe_1, text='xml, txt, doc, xls, ppt, pdf', state=DISABLED,
                                         variable=self.is_cb_documents2, offvalue='n', onvalue='y')
        self.cb_documents2.place(bordermode=OUTSIDE, x=320, y=50)
        self.cb_documents2.select()

        self.cb_source2 = Checkbutton(self.miniframe_1, text='c, cpp, dba, cs, py, vb', state=DISABLED)

        self.cb_archive2 = Checkbutton(self.miniframe_1, text='zip, rar, tar, tar.gz', state=DISABLED,
                                         variable=self.is_cb_archive2, offvalue='n', onvalue='y')
        self.cb_archive2.place(bordermode=OUTSIDE, x=320, y=125)
        self.cb_archive2.select()

        self.cb_java2 = Checkbutton(self.miniframe_1, text='java, class, jar, war, ear', state=DISABLED,
                                         variable=self.is_cb_java2, offvalue='n', onvalue='y')
        self.cb_java2.place(bordermode=OUTSIDE, x=320, y=75)
        self.cb_java2.select()

        self.cb_web2 = Checkbutton(self.miniframe_1, text='php, jsp, html, js, aspx, css', state=DISABLED,
                                         variable=self.is_cb_web2, offvalue='n', onvalue='y')
        self.cb_web2.place(bordermode=OUTSIDE, x=320, y=100)
        self.cb_web2.deselect()
        
        # other - checkbox
        self.cb_freeText2 = Checkbutton(self.miniframe_1, text='Others (type1, type2, type3):', state=DISABLED,
                                       variable=self.isFreeTextTypes2, offvalue='n', onvalue='y', command=self.allowFreeTextTypes2)
        self.cb_freeText2.place(bordermode=OUTSIDE, x=320, y=190)
        self.cb_freeText2.deselect()

        # free text enty
        self.only_freeText = Entry(self.miniframe_1, width=30, state=DISABLED)
        self.only_freeText.place(bordermode=OUTSIDE, x=327, y=225)

        ######################################
        
        #file name to search field
        self.text_findFile = Entry(self.miniframe_2, width=30, state=DISABLED)
        self.text_findFile.place(bordermode=OUTSIDE, x=170, y=45)

        # find button - to find file in host
        self.button_findFile = Button(self.miniframe_2, text='Find', command=self.findMyFile, state=DISABLED)
        self.button_findFile.place(bordermode=OUTSIDE, x=370, y=40)      

        # grid frame
        self.gridFframe=Frame(self.miniframe_2)
        self.gridFframe.place(bordermode=OUTSIDE, x=20, y=70)

        # grid VERTICAL scrollbar
        self.gridVERTICALscrollbar = Scrollbar(self.gridFframe) 
        self.gridVERTICALscrollbar.pack(side=RIGHT, fill=Y)

        # grid HORIZONTAL scrollbar
        self.gridHORIZONTALLscrollbar = Scrollbar(self.gridFframe, orient=HORIZONTAL) 
        self.gridHORIZONTALLscrollbar.pack(side=BOTTOM, fill=X)
        
        # grid listbox for results
        self.listboxFind = Listbox(self.gridFframe, width=88, height=10, yscrollcommand=self.gridVERTICALscrollbar.set, xscrollcommand=self.gridHORIZONTALLscrollbar.set) 
        self.listboxFind.pack()
        
        self.gridVERTICALscrollbar.config(command=self.listboxFind.yview)
        self.gridHORIZONTALLscrollbar.config(command=self.listboxFind.xview)

        # location select button
        self.button_useSelected = Button(self.miniframe_2, text='Use selected', state=DISABLED, command=self.useSelection)
        self.button_useSelected.place(bordermode=OUTSIDE, x=495, y=40)

        # HEADER
        self.label_header = Label(self.miniframe_2, text="Find a file or a directory in host's File System")
        self.label_header.place(bordermode=OUTSIDE, x=35, y=5)
        
        # enable find location        
        self.checkbox_header = Checkbutton(self.miniframe_2, state=DISABLED)
        self.checkbox_header.place(bordermode=OUTSIDE, x=5, y=5)
        self.checkbox_header.deselect()

        # find file - radio button
        self.radio_findFile = Radiobutton(self.miniframe_2, text='File', variable=self.isFileOrFolder, value='_file', state=DISABLED)
        self.radio_findFile.place(bordermode=OUTSIDE, x=15, y=40)
        self.radio_findFile.select()

        # find Library - radio button
        self.radio_findLibrary = Radiobutton(self.miniframe_2, text='Directory', variable=self.isFileOrFolder, value='_folder', state=DISABLED)
        self.radio_findLibrary.place(bordermode=OUTSIDE, x=70, y=40)
        self.radio_findLibrary.deselect()



        ######################
        #    Main Frame:     #
        ######################
        
        # Frame to surround URL/HOMEDIR   
        self.framer_1 = Frame(tab_main, relief=RAISED, width=625, height=100, bd=1)
        self.framer_1.bind("<Enter>", self.sinkFramer_1)
        self.framer_1.bind("<Leave>", self.flatFramer_1)
        self.framer_1.place(bordermode=OUTSIDE, x=12, y=10)
    
        # Frame to Path Traversal / Cookie
        self.framer_2 = Frame(tab_main, relief=RAISED, width=625, height=100, bd=1)
        self.framer_2.bind("<Enter>", self.sinkFramer_2)
        self.framer_2.bind("<Leave>", self.flatFramer_2)
        self.framer_2.place(bordermode=OUTSIDE, x=12, y=120)
        
        # Frame to surround the host credentials   
        self.framer_3 = Frame(tab_main, relief=RAISED, width=625, height=100, bd=1)
        self.framer_3.bind("<Enter>", self.sinkFramer_3)
        self.framer_3.bind("<Leave>", self.flatFramer_3)
        self.framer_3.place(bordermode=OUTSIDE, x=12, y=230)
        
        # Frame to surround current configuration display
        self.framer_4 = Frame(tab_main, relief=RAISED, width=625, height=130, bd=1)
        self.framer_4.bind("<Enter>", self.sinkFramer_4)
        self.framer_4.bind("<Leave>", self.flatFramer_4)
        self.framer_4.place(bordermode=OUTSIDE, x=12, y=350)


        ############################# FRAMER 1 ############################
        #URL/HOMEDIR
        self.label_url = Label(self.framer_1, text="Application URL (https://my.domain.com/app:777):", foreground="black")
        self.label_url.place(bordermode=OUTSIDE, x=5, y=20)

        # App URL: TEXT
        self.text_url = Entry(self.framer_1, width=50, insertwidth=3)
        self.text_url.place(bordermode=OUTSIDE, x=288, y=22)

        # Home directory (in environment): LABEL
        self.label_homeDir = Label(self.framer_1, text="Home directory (home/app/ver):", foreground="black")
        self.label_homeDir.place(bordermode=OUTSIDE, x=5, y=53)

        # Home directory: TEXT
        self.text_homeDir = Entry(self.framer_1, width=50, insertwidth=3)
        self.text_homeDir.place(bordermode=OUTSIDE, x=288, y=55)

        # redirects to configuration tab
        self.button_ask = Button(self.framer_1, text='?', command=self.askHomeDir, cursor="question_arrow")
        self.button_ask.place(bordermode=OUTSIDE, x=598, y=51)


        ############################# FRAMER 2 ###########################

        # Access to internal files
        self.radiobutton_unauth = Radiobutton(self.framer_2, indicatoron=0, text="Forceful Browsing", variable=self.isTraversal,
                                              value='n', command=self.noPathTraversal)
        #self.radiobutton_unauth.pack(padx=0)
        self.radiobutton_unauth.place(bordermode=OUTSIDE, x=10, y=15)

        # PATH TRAVERSAL
        self.radiobutton_traversal = Radiobutton(self.framer_2, indicatoron=0, text='Path Traversal ', variable=self.isTraversal,
                                                 value='y', command=self.noPathTraversal)
        self.radiobutton_traversal.place(bordermode=OUTSIDE, x=150, y=15)
        self.radiobutton_traversal.select()

        # Directory Traversal Encoding (../)
        self.directoryTraversalEncoding_1 =  Radiobutton(self.framer_2, text="../", variable=self.pathEncoding, value='../')
        self.directoryTraversalEncoding_1.place(bordermode=OUTSIDE, x=350, y=15)
        #self.directoryTraversalEncoding_1.pack(ipadx=10)
        self.directoryTraversalEncoding_1.select()
        
        self.directoryTraversalEncoding_2 =  Radiobutton(self.framer_2, text="%2e%2e%2f", variable=self.pathEncoding, value='%2e%2e%2f')
        self.directoryTraversalEncoding_2.place(bordermode=OUTSIDE, x=420, y=15)
        
        self.directoryTraversalEncoding_3 =  Radiobutton(self.framer_2, text="%c0%af", variable=self.pathEncoding, value='%c0%af')
        self.directoryTraversalEncoding_3.place(bordermode=OUTSIDE, x=542, y=15)        # LABEL: Cookie
        
        self.checkbutton_auth = Checkbutton(self.framer_2, text='Authenticated | Cookie :',
                                            variable=self.isAuth, onvalue="y", offvalue="n", command=self.useCookie)
        self.checkbutton_auth.place(bordermode=OUTSIDE, x=5, y=62)
        self.checkbutton_auth.deselect()

        # TEXT: Cookie
        self.text_cookie = Entry(self.framer_2, width=72, state=DISABLED, insertwidth=3)
        self.text_cookie.place(bordermode=OUTSIDE, x=170, y=62)
        
        ############################# FRAMER 3 ###########################
        
        # Use local file (upload) / Get file from HOST
        self.radiobutton_getFilefromHost = Radiobutton(self.framer_3, text='Get file from Host',
                                                       command=self.setFileMode, variable=self.xMode, value='1')
        self.radiobutton_getFilefromHost.place(bordermode=OUTSIDE, x=5, y=15)
        self.radiobutton_getFilefromHost.select()

        # Remote connection (HOST)
        self.label_host = Label(self.framer_3, text="Host:", foreground="black")
        self.label_host.place(bordermode=OUTSIDE, x=150, y=15)
        self.entry_host = Entry(self.framer_3, width=15, insertwidth=3)
        self.entry_host.place(bordermode=OUTSIDE, x=182, y=17)

        # Remote connection (PORT)
        self.label_port = Label(self.framer_3, text="Port:", foreground="black")
        self.label_port.place(bordermode=OUTSIDE, x=288, y=15)
        self.entry_port = Entry(self.framer_3, width=15, insertwidth=3)
        self.entry_port.place(bordermode=OUTSIDE, x=320, y=17)
        self.entry_port.insert(0,"22")

        # Upload File: LABEL
        self.radiobutton_uploadFile = Radiobutton(self.framer_3, text='Upload file', command=self.setFileMode, variable=self.xMode, value='2')
        self.radiobutton_uploadFile.place(bordermode=OUTSIDE, x=435, y=15)
        
        # Upload File: Button
        self.upload_button = Button(self.framer_3, text=" Browse... ", command=self.browseFile, disabledforeground="gray", state=DISABLED)
        self.upload_button.place(bordermode=OUTSIDE, x=544, y=15)

        # Remote connection (USER)
        self.label_user = Label(self.framer_3, text="User:", foreground="black")
        self.label_user.place(bordermode=OUTSIDE, x=90, y=60)
        self.entry_user = Entry(self.framer_3, width=15, insertwidth=3)
        self.entry_user.place(bordermode=OUTSIDE, x=122, y=62)

        # Remote connection (PW)
        self.label_pw = Label(self.framer_3, text="Password:", foreground="black")
        self.label_pw.place(bordermode=OUTSIDE, x=232, y=60)
        self.entry_pw = Entry(self.framer_3, width=15, show='*', insertwidth=3)
        self.entry_pw.place(bordermode=OUTSIDE, x=290, y=62)


        # Upload File: Label
        self.upload_label = Label(self.framer_3, text="", state=DISABLED)
        self.upload_label.place(bordermode=OUTSIDE, x=515, y=17)

        # Check Button: Skip Line
        self.checkbutton_skipLine = Checkbutton(self.framer_3, text='Skip to line # ', variable=self.isSkip, onvalue="y", offvalue="n", command=self.useSkip, state=DISABLED)
        self.checkbutton_skipLine.place(bordermode=OUTSIDE, x=435, y=60)
        self.checkbutton_skipLine.deselect()

        # TEXT: Skip Line
        self.text_skipLine = Entry(self.framer_3, width=10, state=DISABLED)
        self.text_skipLine.pack()
        self.text_skipLine.place(bordermode=OUTSIDE, x=540, y=60)
        
        ############################# FRAMER 4 ###########################
        
        self.currentConf = Label(tab_main, text="", fg="gray40")
        # Codes Header
        self.displayCodes_headr = Label(self.framer_4, text="Selected Response Codes")
        self.displayCodes_headr.place(bordermode=OUTSIDE, x=10, y=20)
        # Types Header
        self.displayTypes_headr = Label(self.framer_4, text="File Types:")
        self.displayTypes_headr.place(bordermode=OUTSIDE, x=205, y=20)
        # Strings Header
        self.displayStrings_headr = Label(self.framer_4, text="Find strings in Response:")
        self.displayStrings_headr.place(bordermode=OUTSIDE, x=377, y=20)
        
        # Codes Frame
        self.miniframer_1 = Frame(self.framer_4, relief=GROOVE, bd=2)
        self.miniframer_1.place(bordermode=OUTSIDE, x=12, y=40)
        # Types Frame
        self.miniframer_2 = Frame(self.framer_4, relief=GROOVE, bd=2)
        self.miniframer_2.place(bordermode=OUTSIDE, x=208, y=40)
        # Strings Frame
        self.miniframer_3 = Frame(self.framer_4, relief=GROOVE, width=191, height=76, bd=2)
        self.miniframer_3.place(bordermode=OUTSIDE, x=380, y=40)

        # Modify Codes 
        self.buttonModifyCodes = Button(self.framer_4, text="Modify", command=self.modifyCodes)
        self.buttonModifyCodes.place(bordermode=OUTSIDE, x=135, y=92)
        # Modify File Types 
        self.buttonModifyTypes = Button(self.framer_4, text="Modify", command=self.modifyTypes)
        self.buttonModifyTypes.place(bordermode=OUTSIDE, x=307, y=92)
        # Modify Strings 
        self.buttonModifyStrings = Button(self.framer_4, text="Modify", command=self.modifyStrings)
        self.buttonModifyStrings.place(bordermode=OUTSIDE, x=570, y=92)

        # Scroll Bar Code
        self.DcodeScrollBar = Scrollbar(self.miniframer_1)
        self.DcodeScrollBar.pack(side=RIGHT, fill=Y)
        # Scroll Bar File Types
        self.DtypesScrollBar = Scrollbar(self.miniframer_2)
        self.DtypesScrollBar.pack(side=RIGHT, fill=Y)
        # Scroll Bar Strings
        self.DstringsScrollBar = Scrollbar(self.miniframer_3, orient=HORIZONTAL)
        self.DstringsScrollBar.place(bordermode=OUTSIDE, x=138, y=3)
        self.DstringsScrollBar2 = Scrollbar(self.miniframer_3, orient=HORIZONTAL)
        self.DstringsScrollBar2.place(bordermode=OUTSIDE, x=138, y=40)
        
        # List of HTTP STATUS CODES (Current)
        self.Dlistbox_codes = Listbox(self.miniframer_1, width=17, height=5, yscrollcommand=self.DcodeScrollBar.set)
        self.Dlistbox_codes.pack(fill=X)
        # List of File Types (Current)
        self.Dlistbox_types = Listbox(self.miniframer_2, width=13, height=5, yscrollcommand=self.DtypesScrollBar.set)
        self.Dlistbox_types.pack(fill=X)
        # Strings
        self.isIgnoreString = Checkbutton(self.miniframer_3, state=DISABLED)
        self.isIgnoreString.place(bordermode=OUTSIDE, x=50, y=1)
        
        self.ignoreString = Label(self.miniframer_3, text="Ignore: ", fg="gray45")
        self.ignoreString.place(bordermode=OUTSIDE, x=70, y=1)
        
        self.ignoreText = Entry(self.miniframer_3, state=DISABLED, width=30, xscrollcommand=self.DstringsScrollBar.set)
        self.ignoreText.place(bordermode=OUTSIDE, x=1, y=20)


        self.isAcceptString = Checkbutton(self.miniframer_3, state=DISABLED)
        self.isAcceptString.place(bordermode=OUTSIDE, x=50, y=37)
        
        self.acceptString = Label(self.miniframer_3, text="Find: ", fg="gray45")
        self.acceptString.place(bordermode=OUTSIDE, x=70, y=37)
        
        self.acceptText = Entry(self.miniframer_3, state=DISABLED, width=30, xscrollcommand=self.DstringsScrollBar2.set)
        self.acceptText.place(bordermode=OUTSIDE, x=1, y=56)
        

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
        self.about_label = Label(tab_about, text="Path Traverser v1.4")
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

        #contact 
        self.about_label_5 = Label(tab_about, text="Tal Melamed | pt@appsec.it")
        self.about_label_5.pack()


        #######################
        ##      Main TAB:    ## 
        #######################


        ########## Main Buttons ###########
        # Status bars     
        self.text_status = Text(tab_main, state=NORMAL, width=92, height=10, background="#DDDDDD", foreground="#990000")
        self.text_status.insert(INSERT, "Status")
        self.text_status.pack()
        self.text_status.configure(state=DISABLED)
        self.text_status.place(bordermode=OUTSIDE, x=0, y=490)

        # Progress bar
        self.progress = ttk.Progressbar(tab_main, orient="horizontal", length=648, mode="determinate")
        self.progress.place(bordermode=OUTSIDE, x=1, y=528)



        ######################
        #    Results TAB:    #
        ######################

        self.results_text = Text(tab_res, width=90, height=39, state=DISABLED)
        self.results_text.bind("<Double-Button-1>", self.hyperlinkURL)
        self.results_text.bind("<ButtonRelease-1>", self.copyLink)
        self.results_text.bind("<Motion>", self.hyperlinkCurser)
        self.results_text.bind("<Enter>", self.hyperlinkCurser)
        self.results_text.place(bordermode=OUTSIDE, x=5, y=5)

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

        # Scroll Bar
        self.logScrollBar = Scrollbar(tab_log)
        self.logScrollBar.pack(side=RIGHT, fill=Y)
        self.logScrollBar.configure(command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=self.logScrollBar.set)
        


        ######################
        #   Sessions TAB:    #
        ######################

        # Sessions frame
        self.sessionsFrame = Frame(tab_sessions)
        self.sessionsFrame.place(bordermode=OUTSIDE, x=10, y=20)

        # Scroll Bar
        self.sessionsScrollBar = Scrollbar(self.sessionsFrame)
        self.sessionsScrollBar.pack(side=RIGHT, fill=Y)

        # List of Saved sessoins
        self.listbox_savedSessions = Listbox(self.sessionsFrame, width=50, height=15, exportselection=0,
                                             yscrollcommand=self.sessionsScrollBar.set)
        self.listbox_savedSessions.bind("<<ListboxSelect>>", self.modifySession)
        
        self.listbox_savedSessions.pack()
        self.listbox_savedSessions.select_set(2)
        self.sessionsScrollBar.configure(command=self.listbox_savedSessions.yview)

        # load / default / delete buttons
        
        self.button_LoadSession = Button(tab_sessions, text='        Load       ', command=self.loadSession)
        self.button_LoadSession.place(bordermode=OUTSIDE, x=350, y=50)      

        self.button_newSession = Button(tab_sessions, text='        New       ', command=self.addNewSession)
        self.button_newSession.place(bordermode=OUTSIDE, x=350, y=20)      

        self.button_deleteSession = Button(tab_sessions, text='      Delete      ', command=self.deleteSession)
        self.button_deleteSession.place(bordermode=OUTSIDE, x=350, y=80)      

        

        self.tabs.select(self.tabs.tabs()[0])
        self.withMainTab()



## ============================================================================================================================= ##
## ======================================================  FUNCTUIONS  ========================================================= ##
## ============================================================================================================================= ##
    
    def openAboutPopup(self):
        #helpPopup = tkMessageBox.showinfo("ABOUT US...")
        self.tabs.select(self.tabs.tabs()[5])
        
    # Highlight and de-highlight Frames in the Main Tab when Mouse Enters/ Leaves frame
    def sinkFramer_1(self, event):
        self.framer_1.configure(relief=GROOVE, bd=2)
    def flatFramer_1(self, event):
        self.framer_1.configure(relief=RAISED, bd=1)

    def sinkFramer_2(self, event):
        self.framer_2.configure(relief=GROOVE, bd=2)
    def flatFramer_2(self, event):
        self.framer_2.configure(relief=RAISED, bd=1)
        
    def sinkFramer_3(self, event):
        self.framer_3.configure(relief=GROOVE, bd=2)
    def flatFramer_3(self, event):
        self.framer_3.configure(relief=RAISED, bd=1)

    def sinkFramer_4(self, event):
        self.currentConf.configure(text="[ Current Configuration ]")
        self.currentConf.place(x=262, y=340)
        self.framer_4.configure(relief=GROOVE, bd=2)
    def flatFramer_4(self, event):
        self.framer_4.configure(relief=RAISED, bd=1)
        self.currentConf.configure(text="")

    # run everytime Demo Tab (will be replaced with Main) is focused or entered
    def DemoTabSelected(self, event):
        self.withMainTab()

    # run everytime the Main Tab is selected.
    # generates current configurations
    def withMainTab(self):
        self.DlistofCodes = ['x']
        try:
            self.DlistofCodes = self.getCodeSelection()
        except:
            self.DlistofCodes = ["200"]
       
        self.Dlistbox_codes.configure(state=NORMAL)
        self.Dlistbox_codes.delete(0, END)
        for item in self.DlistofCodes:
            self.Dlistbox_codes.insert(END, item)

        self.DcodeScrollBar.configure(command=self.Dlistbox_codes.yview)
        self.Dlistbox_codes.configure(state=DISABLED, bd=0)
        
        if self.fileTypes.get() == '1':
            header = 'Excluding File Types'
            self.listofTypes = ['.gif', '.png', '.jpg', '.js', '.bmp', '.css']
        else: #manual
            flag = self.useListofFileTypes()
            if flag == "y":
                header = 'Uses only File Types'
                self.listofTypes = self.onlyTypes
            else:
                header = 'Excluding File Types'
                self.listofTypes = self.excludeTypes

        self.displayTypes_headr.configure(text=header)
        self.Dlistbox_types.configure(state=NORMAL)
        self.Dlistbox_types.delete(0, END)
        for item in self.listofTypes:
            self.Dlistbox_types.insert(END, item)
            
        self.DtypesScrollBar.configure(command=self.Dlistbox_types.yview)
        self.Dlistbox_types.configure(state=DISABLED, bd=0)

        if self.isErrMsg.get() == "y":
            self.ignoreText.configure(state=NORMAL)
            self.ignoreText.delete(0, END)
            self.ignoreText.insert(0, self.text_errMsg.get())
            self.DstringsScrollBar.configure(command=self.ignoreText.xview)
            self.ignoreText.configure(state=DISABLED)
            self.isIgnoreString.select()
        else:
            self.isIgnoreString.deselect()

        if self.isFindMsg.get() == "y":
            self.acceptText.configure(state=NORMAL)
            self.acceptText.delete(0, END)
            self.acceptText.insert(0, self.text_findMsg.get())
            self.DstringsScrollBar2.configure(command=self.acceptText.xview)
            self.acceptText.configure(state=DISABLED)
            self.isAcceptString.select()
        else:
            self.isAcceptString.deselect()
        
    # Modify Strings selected from Main Tab
    # redirect to Configuration Tab and expend the Strings Configuration
    def modifyStrings(self):
        self.tabs.select(self.tabs.tabs()[1])
        self.expandConfiguration_4()

    # Modify Codes selected from Main Tab
    # redirect to Configuration Tab and expend the Codes Configuration
    def modifyCodes(self):
        self.tabs.select(self.tabs.tabs()[1])
        self.expandConfiguration_3()

    # Modify File Types selected from Main Tab
    # redirect to Configuration Tab and expend the Types Configuration
    def modifyTypes(self):
        self.tabs.select(self.tabs.tabs()[1])
        if self.fileTypes.get() == '1':
            self.enableTypes()
        self.expandConfiguration_1()

   # Expend configuration 1: File Types
    def expandConfiguration_1(self):
        self.collapseConfiguration_2()
        self.collapseConfiguration_3()
        self.collapseConfiguration_4()
        self.demo_1.configure(text=" -", command=self.collapseConfiguration_1)
        self.miniframe_1.place(bordermode=OUTSIDE, x=10, y=55)
        self.miniframe_1.configure(relief=SUNKEN, bd=2)
        self.conf_2.place(bordermode=OUTSIDE, x=35, y=385)
        self.demo_2.place(bordermode=OUTSIDE, x=10, y=385)
        self.conf_3.place(bordermode=OUTSIDE, x=35, y=420)
        self.demo_3.place(bordermode=OUTSIDE, x=10, y=420)
        self.conf_4.place(bordermode=OUTSIDE, x=35, y=455)
        self.demo_4.place(bordermode=OUTSIDE, x=10, y=455)

    # Collapse configuration 1: File Types
    def collapseConfiguration_1(self):
        self.miniframe_1.place_forget()
        self.demo_1.configure(text="+", command=self.expandConfiguration_1)
        self.conf_2.place(bordermode=OUTSIDE, x=35, y=60)
        self.demo_2.place(bordermode=OUTSIDE, x=10, y=60)
        self.conf_3.place(bordermode=OUTSIDE, x=35, y=95)
        self.demo_3.place(bordermode=OUTSIDE, x=10, y=95)
        self.conf_4.place(bordermode=OUTSIDE, x=35, y=130)
        self.demo_4.place(bordermode=OUTSIDE, x=10, y=130)
        self.miniframe_1.configure(bd=0)


    # Expend configuration 2: find file/directory
    def expandConfiguration_2(self):
        self.collapseConfiguration_1()
        self.collapseConfiguration_3()
        self.collapseConfiguration_4()
        self.demo_2.configure(text=" -", command=self.collapseConfiguration_2)
        self.miniframe_2.place(bordermode=OUTSIDE, x=10, y=90)
        self.miniframe_2.configure(relief=SUNKEN, bd=2)
        self.checkbox_header.select()
        self.findIt()
        self.conf_1.place(bordermode=OUTSIDE, x=35, y=25)
        self.demo_1.place(bordermode=OUTSIDE, x=10, y=25)
        self.conf_3.place(bordermode=OUTSIDE, x=35, y=400)
        self.demo_3.place(bordermode=OUTSIDE, x=10, y=400)
        self.conf_4.place(bordermode=OUTSIDE, x=35, y=435)
        self.demo_4.place(bordermode=OUTSIDE, x=10, y=435)

    # Collapse configuration 2: find file/directory   
    def collapseConfiguration_2(self):
        self.miniframe_2.place_forget()
        self.demo_2.configure(text="+", command=self.expandConfiguration_2)
        self.conf_2.place(bordermode=OUTSIDE, x=35, y=60)
        self.demo_2.place(bordermode=OUTSIDE, x=10, y=60)
        self.conf_3.place(bordermode=OUTSIDE, x=35, y=95)
        self.demo_3.place(bordermode=OUTSIDE, x=10, y=95)
        self.conf_4.place(bordermode=OUTSIDE, x=35, y=130)
        self.demo_4.place(bordermode=OUTSIDE, x=10, y=130)
        self.checkbox_header.configure(state=NORMAL)
        self.checkbox_header.deselect()
        self.checkbox_header.configure(state=DISABLED)
        self.miniframe_2.configure(bd=0)


    # Expend configuration 3: Http Status Codes    
    def expandConfiguration_3(self):
        self.collapseConfiguration_1()
        self.collapseConfiguration_2()
        self.collapseConfiguration_4()
        self.demo_3.configure(text=" -", command=self.collapseConfiguration_3)
        self.miniframe_3.place(bordermode=OUTSIDE, x=10, y=125)
        self.miniframe_3.configure(relief=SUNKEN, bd=2)
        self.conf_1.place(bordermode=OUTSIDE, x=35, y=25)
        self.demo_1.place(bordermode=OUTSIDE, x=10, y=25)
        self.conf_2.place(bordermode=OUTSIDE, x=35, y=60)
        self.demo_2.place(bordermode=OUTSIDE, x=10, y=60)
        self.conf_4.place(bordermode=OUTSIDE, x=35, y=435)
        self.demo_4.place(bordermode=OUTSIDE, x=10, y=435)
        
    # Collapse configuration 3: Http Status Codes    
    def collapseConfiguration_3(self):
        self.miniframe_3.place_forget()
        self.demo_3.configure(text="+", command=self.expandConfiguration_3)
        self.conf_1.place(bordermode=OUTSIDE, x=35, y=25)
        self.demo_1.place(bordermode=OUTSIDE, x=10, y=25)
        self.conf_2.place(bordermode=OUTSIDE, x=35, y=60)
        self.demo_2.place(bordermode=OUTSIDE, x=10, y=60)
        self.conf_4.place(bordermode=OUTSIDE, x=35, y=130)
        self.demo_4.place(bordermode=OUTSIDE, x=10, y=130)
        self.miniframe_3.configure(bd=0)


    # Expend configuration 4: find/ignore strings
    def expandConfiguration_4(self):
        self.collapseConfiguration_1()
        self.collapseConfiguration_2()
        self.collapseConfiguration_3()
        self.demo_4.configure(text=" -", command=self.collapseConfiguration_4)
        self.miniframe_4.place(bordermode=OUTSIDE, x=10, y=160)
        self.miniframe_4.configure(relief=SUNKEN, bd=2)
        self.conf_1.place(bordermode=OUTSIDE, x=35, y=25)
        self.demo_1.place(bordermode=OUTSIDE, x=10, y=25)
        self.conf_2.place(bordermode=OUTSIDE, x=35, y=60)
        self.demo_2.place(bordermode=OUTSIDE, x=10, y=60)
        self.conf_3.place(bordermode=OUTSIDE, x=35, y=95)
        self.demo_3.place(bordermode=OUTSIDE, x=10, y=95)
        
    # Collapse configuration 4: find/ignore strings   
    def collapseConfiguration_4(self):
        self.miniframe_4.place_forget()
        self.demo_4.configure(text="+", command=self.expandConfiguration_4)
        self.conf_1.place(bordermode=OUTSIDE, x=35, y=25)
        self.demo_1.place(bordermode=OUTSIDE, x=10, y=25)
        self.conf_2.place(bordermode=OUTSIDE, x=35, y=60)
        self.demo_2.place(bordermode=OUTSIDE, x=10, y=60)
        self.conf_3.place(bordermode=OUTSIDE, x=35, y=95)
        self.demo_3.place(bordermode=OUTSIDE, x=10, y=95)
        self.miniframe_4.configure(bd=0)

    # Set session as default session - to be selected from main Tab (NOT AVAILABLE)
    def addNewSession(self):
        self.tabs.select(self.tabs.tabs()[0])
        popup = tkMessageBox.showinfo("New Session", "Enter application URL (other data is optional)\n\n Click 'Options' --> 'Save Session' when done.")
        if self.xMode.get() == "1":
            self.findIfMissing()
        else:
            self.removeStar(self.label_host)
            self.removeStar(self.label_user)
            try:
                tmpFile = open(self.selectedFileName, 'r')
                self.removeStar(self.upload_button)

            except:
                isMissing = 1
                self.addStar(self.upload_button)
        
    # Modify selected Session (NOT AVAILABLE)
    def modifySession(self, event):
        pass

    # Application Files Or Path Traversal? (for type for directory listing (../) 
    def noPathTraversal(self):
        if self.isTraversal.get() == "n":
            self.directoryTraversalEncoding_1.configure(state=DISABLED)
            self.directoryTraversalEncoding_2.configure(state=DISABLED)
            self.directoryTraversalEncoding_3.configure(state=DISABLED)
        else:
            self.directoryTraversalEncoding_1.configure(state=NORMAL)
            self.directoryTraversalEncoding_2.configure(state=NORMAL)
            self.directoryTraversalEncoding_3.configure(state=NORMAL)
            

    # load saved sessions into list of available sessions
    def SessionTabSelected(self, event):
        self.listofSessions = []
        self.listbox_savedSessions.delete(0, END)
        new = 0
        lines = open('pt.ini', 'r').read().split('\n')
        for line in lines:
            if line == '[new_session]':
                new = 1
            else:
                if new == 1:
                    self.listofSessions.append(line[5:])
                    new =0
                    
        for item in self.listofSessions:
            self.listbox_savedSessions.insert(END, item)

        self.selectDefaultSession()

    # Select the defaulted session
    def selectDefaultSession(self):
        self.listbox_savedSessions.select_set(0)
        
    # saves current state into a file
    def executeSave(self):
        if len(self.text_url.get()) > 1:
            try:
                file = open(self.savedFileName, 'r')
                content = file.read()
                file.close()
            except:
                content = ""

            self.URLfromHost = self.getHostfromURL()
            if self.URLfromHost == "":
                return 0

            if content.find('host=' +self.URLfromHost +'\n') == -1:
                self.newWrite(self.savedFileName)
                self.editStatus('Saved session: ' +self.URLfromHost, 3)
                
            else:
                # DID find the Host in the file (should replace)
                popup = tkMessageBox.askyesno("Overwrite Session?", self.URLfromHost +" - already exists. would you like to overwrite?")
                if popup == True:
                    # read pt.ini file
                    file = open(self.savedFileName, 'r')
                    text = file.read()
                    file.close()
                    # find location of current host in pt.ini file
                    startpoint = text.find('host=' +self.URLfromHost +'\n')
                    # did not find (write new)
                    if startpoint == -1:
                        self.newWrite(self.savedFileName)
                        return 1
                    else:
                        tmptext = text[startpoint:]
                        endpoint = tmptext.find('[new_session]')
                        if endpoint == -1:
                            spectext = text[startpoint-14:]
                        else:
                            spectext = text[startpoint-14:endpoint+startpoint]
                            
                    tmpfile = self.savedFileName +'.tmp'
                    # write saved data into tmp file
                    while not self.newWrite(tmpfile):
                        pass
                    # read/remove tmp file
                    newtextfile = open(tmpfile, 'r')
                    newtext = newtextfile.read()
                    newtextfile.close()
                    os.remove(tmpfile)
                    # replace text with new text(from tmpfile)
                    mytext = text.replace(spectext, newtext)
                    file = open(self.savedFileName, 'w')
                    file.write(mytext)
                    self.editStatus('Saved session: ' +self.URLfromHost, 3)
                    file.close()
        else:
            self.editStatus('Could not save. Missing URL...', 1)
            self.addStar(self.label_url)
            return 0

    #write data into given file                     
    def newWrite(self, xfile):
        verifyPath = os.path.join(os.getcwd()) + '\\' +xfile
        file = open(xfile, 'a')
        file.write('[new_session]\n')
        file.write('host=' +self.URLfromHost +'\n')
        file.write('port=' +self.entry_port.get() +'\n')
        file.write('user=' +self.entry_user.get() +'\n')
        file.write('url=' +self.text_url.get() +'\n')
        file.write('homedir=' +self.text_homeDir.get()+ '\n')

        if self.isErrMsg.get() == "y":
            file.write('errmsg=' +self.text_errMsg.get() +'\n')
        else:
            file.write('errmsg=\n')

        if self.isAuth.get() == 'y':
            file.write('cookie=' +self.text_cookie.get()+'\n')
        else:
            file.write('cookie=\n')

        if self.xMode.get() == '1':
            file.write('mode=1\n')
            file.write('file=\n')
        else:
            try:
                tmpFile = open(self.selectedFileName, 'r')
                file.write('mode=2\n')
                file.write('file=' +self.selectedFileName +'\n')
            except:
                file.write('mode=1\n')
                file.write('file=\n')
                self.editStatus('Could not save - please select a file and try again...', 3)
                return 1
        if self.isTraversal.get() == "n":
            file.write("attack=fb\n")
        else:
            file.write("attack=pt\n")
            
        file.close()
        return 1

    # Delete selected Session from the Session Tab
    def deleteSession(self):
        for i in range(len(self.listofSessions)):
            if self.listbox_savedSessions.select_includes(i) == True:
                myHost = self.listofSessions[i]
                break
            else:
                pass
            
        file = open(self.savedFileName, 'r')
        text = file.read()
        file.close()
        startpoint = text.find('host=' +myHost +'\n')
        if startpoint == -1:
            self.editStatus('Could not delete selected host, corrupted file?', 3)
            return 0
        else:
            file2 = open(self.savedFileName, 'w')
            tmptext = text[startpoint:]
            endpoint = tmptext.find('[new_session]')
            # not another session after
            if endpoint == -1:
                # only session
                if startpoint == 14:
                    pass
                # last session
                else:
                    text=text[:startpoint-14]
                    file2.write(text)
            else:
                text_before = text[:startpoint-14]
                text_after  = text[endpoint+startpoint:]
                file2.write(text_before+'\n'+text_after)

            file2.close()
            self.SessionTabSelected(event=None)

    # Load session from Sessions Tab
    def loadSession(self):
        verifyPath = os.path.join(os.getcwd()) +'\\' +self.savedFileName
        if os.path.exists(verifyPath) != True:
            self.editStatus('could not find pt.ini, no stored sessions...', 1)
            self.tabs.select(self.tabs.tabs()[0])
            return 0
        else:
            for i in range(len(self.listofSessions)):
                if self.listbox_savedSessions.select_includes(i) == True:
                    myHost = self.listofSessions[i]
                    break
                else:
                    pass

            self.cleanContent()
            file = open(self.savedFileName, 'r')
            text = file.read()
            file.close()
            startpoint = text.find('host=' +myHost +'\n')
                # did not find (write new)
            if startpoint == -1:
                self.editStatus('Could not find selected host, corrupted file?', 3)
                return 0
            else:
                tmptext = text[startpoint:]
                endpoint = tmptext.find('[new_session]')
                if endpoint == -1:
                    spectext = text[startpoint:]
                else:
                    spectext = text[startpoint:endpoint+startpoint]

            lines = spectext.split('\n')
            if len(lines) != 11:
                self.editStatus('Corrupted session file... could not load', 3)
                return 0
            
            self.text_url.insert(0, lines[3][4:])
            self.text_homeDir.insert(0, lines[4][8:])
            
            if len(lines[5]) > 7:
                self.checkbutton_errMsg.select()
                self.text_errMsg.configure(state=NORMAL)
                self.text_errMsg.insert(0, lines[4][7:])
                
            if len(lines[6]) > 7:
                self.checkbutton_auth.select()
                self.text_cookie.configure(state=NORMAL)
                self.text_cookie.insert(0, lines[5][7:])
                
            if lines[7][5:] == '2':
                self.xMode.set('2')
                self.setFileMode()
                self.selectedFileName = lines[7][5:]
                selectedFileLength = len(self.selectedFileName)
                if selectedFileLength > 39:
                    displayedFileName = '...' +self.selectedFileName[selectedFileLength-36:]
                else:
                    displayedFileName = self.selectedFileName
                self.upload_label.configure(state=NORMAL, text='Selected file: %s' %displayedFileName, foreground="darkblue")
                self.radiobutton_uploadFile.select()
            else:
                self.xMode.set('1')
                self.setFileMode()
                self.entry_host.delete(0, END)
                self.entry_user.delete(0, END)
                self.entry_host.insert(0, lines[0][5:])
                self.entry_port.insert(0, lines[1][5:])
                self.entry_user.insert(0, lines[2][5:])

            if lines[9][7:] == 'pt':
                self.isTraversal.set("y")
                self.noPathTraversal()
            else:
                self.isTraversal.set("n")
                self.noPathTraversal()
            
            self.tabs.select(self.tabs.tabs()[0])
            self.editStatus("Loaded '" +lines[0][5:] +"' details...", 3)
            file.close()

    # clean all content before loading
    def cleanContent(self):
        self.entry_host.delete(0, END)
        self.entry_port.delete(0, END)
        self.entry_port.delete(0, END)
        self.entry_user.delete(0, END)
        self.text_url.delete(0, END)
        self.text_homeDir.delete(0, END)
        self.text_errMsg.delete(0, END)
        self.text_cookie.delete(0, END)
        self.checkbutton_auth.deselect()
        
    # Load button was pressed from Main Tab (NOT AVAILABLE)        
    def executeLoad(self):
        print "x"
        
    # get HOST from URL entry
    def getHostfromURL(self):
        isHTTP = self.text_url.get().find('https://')
        #HTTPS
        if isHTTP == 0:
            loc = 8
        #HTTP
        elif isHTTP == -1 and self.text_url.get().find('http://') == 0:
            loc = 7
        # Invalid URL
        else:
             self.editStatus('Could not save. Invalid URL (missing http/s?)', 3)
             return ""

        length = self.text_url.get()[loc:].find(':')
        if length == -1:
            # no PORT
            length = self.text_url.get()[loc:].find('/')
            if length != -1:
                self.URLfromHost = self.text_url.get()[loc:length+loc]
                return self.URLfromHost
            else:
                self.URLfromHost = self.text_url.get()[loc:]
                return self.URLfromHost
        else:
            self.URLfromHost = self.text_url.get()[loc:length+loc]
            return self.URLfromHost

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
        #if self.startPressed == 1:
            #self.pausePressed()
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
            pass

    # redirect to find file in env.
    def askHomeDir(self):    
        self.tabs.select(self.tabs.tabs()[1])
        self.expandConfiguration_2()
        self.findIt()

    def findIt(self):
        self.button_findFile.configure(state=NORMAL)
        self.text_findFile.configure(state=NORMAL)
        self.listboxFind.configure(state=NORMAL)
        self.radio_findLibrary.configure(state=NORMAL)
        self.radio_findFile.configure(state=NORMAL)
        #self.label_header.configure(foreground="black")
        self.getFileFromHost = 1
        
    # Enables all relevant widgets to find a file or a directory in host server under configuration tab
    '''
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
            '''

    # serach in host enviroment for entered file
    ############################################# SECURITY NOTE #############################################
    ## SECURITY NOTE: since in order to run the search, you should have the user/pw to the host server -   ##
    ## no input validation is performed on file/ folder name. Feel free to destroy your own environment :) ##
    #########################################################################################################
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
        self.collapseConfiguration_2()
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
               # self.enableFindFile()
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

    def useFindMsg(self):
        if self.isFindMsg.get() == 'y':
            self.text_findMsg.configure(state=NORMAL)
        else:
            self.text_findMsg.configure(state=DISABLED)
        
    # use cookie for requests
    def useCookie(self):
        if self.isAuth.get() == 'y':
            self.text_cookie.configure(state=NORMAL)
        else:
            self.text_cookie.configure(state=DISABLED)

    # if = 1: get file from HOST, else: use uploaded file
    def setFileMode(self):
        if self.xMode.get() == '1':
            self.upload_label.configure(text="")
            self.upload_button.configure(state=DISABLED)
            self.checkbutton_skipLine.configure(state=DISABLED)
            self.entry_host.configure(state=NORMAL)
            if len(self.text_url.get()) > 2:
                self.entry_host.delete(0, END)
                self.entry_host.insert(0, self.getHostfromURL())
            self.entry_user.configure(state=NORMAL)
            self.entry_pw.configure(state=NORMAL)
            self.entry_port.configure(state=NORMAL)
        else:
            self.checkbutton_skipLine.configure(state=NORMAL)
            self.upload_button.configure(state=NORMAL)
            self.entry_host.configure(state=DISABLED)
            self.entry_user.configure(state=DISABLED)
            self.entry_pw.configure(state=DISABLED)
            self.entry_port.configure(state=DISABLED)

    # manual selection of files types is selected
    def enableTypes(self):
        if self.isEnabled == 0:
            self.isEnabled = 1
            self.setFileTypes()
            self.radiobutton_fileTypeEnable.configure(text="Disable")
        else:
            self.isEnabled = 0
            self.setFileTypes()
            self.radiobutton_fileTypeEnable.configure(text="Enable")


    # in default all selections of File Types are disabled
    # enables when choosed
    def setFileTypes(self):
        if self.fileTypes.get() == '1':
            self.button_conf_default.configure(state=DISABLED)
            self.radiobutton_excludeTypes.configure(state=DISABLED)
            self.radiobutton_useOnlyTypes.configure(state=DISABLED)
            self.cb_graphics.configure(state=DISABLED)
            self.cb_documents.configure(state=DISABLED)
            self.cb_archive.configure(state=DISABLED)
            self.cb_web.configure(state=DISABLED)
            self.cb_java.configure(state=DISABLED)
            self.cb_freeText.configure(state=DISABLED)
            self.cb_documents2.configure(state=DISABLED)
            self.cb_archive2.configure(state=DISABLED)
            self.cb_web2.configure(state=DISABLED)
            self.cb_java2.configure(state=DISABLED)
            self.cb_freeText2.configure(state=DISABLED)
            self.fileTypes.set('2')
        else:
            self.button_conf_default.configure(state=NORMAL)
            self.restoreDefaultConfiguration()
            self.fileTypes.set('1')

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
        
        self.cb_documents2.configure(state=DISABLED)
        self.cb_archive2.configure(state=DISABLED)
        self.cb_web2.configure(state=DISABLED)
        self.cb_java2.configure(state=DISABLED)
        self.cb_freeText2.configure(state=DISABLED)
        self.only_freeText.configure(state=DISABLED)  
        
        self.cb_graphics.select()
        self.cb_documents.deselect()
        self.cb_archive.deselect()
        self.cb_web.select()
        self.cb_java.deselect()
        self.cb_freeText.deselect()
        self.cb_documents2.select()
        self.cb_archive2.select()
        self.cb_web2.deselect()
        self.cb_java2.select()
        self.cb_freeText2.deselect()
        
    # exclude/use-only File Types
    def useFileTypes(self):
        if self.useTypes.get() == '2': #use only
            self.cb_documents2.configure(state=NORMAL)
            self.cb_archive2.configure(state=NORMAL)
            self.cb_web2.configure(state=NORMAL)
            self.cb_java2.configure(state=NORMAL)
            self.cb_freeText2.configure(state=NORMAL)

            self.cb_graphics.configure(state=DISABLED)
            self.cb_documents.configure(state=DISABLED)
            self.cb_archive.configure(state=DISABLED)
            self.cb_web.configure(state=DISABLED)
            self.cb_java.configure(state=DISABLED)
            self.cb_freeText.configure(state=DISABLED)
                
        else: #exclude
            self.cb_graphics.configure(state=NORMAL)
            self.cb_documents.configure(state=NORMAL)
            self.cb_archive.configure(state=NORMAL)
            self.cb_web.configure(state=NORMAL)
            self.cb_java.configure(state=NORMAL)
            self.cb_freeText.configure(state=NORMAL)
        
            self.cb_documents2.configure(state=DISABLED)
            self.cb_archive2.configure(state=DISABLED)
            self.cb_web2.configure(state=DISABLED)
            self.cb_java2.configure(state=DISABLED)
            self.cb_freeText2.configure(state=DISABLED)

    # clears all inserted inputs
    def clearData(self):
        self.text_url.delete(0, END)
        self.text_homeDir.delete(0, END)
        self.radiobutton_traversal.select()
        self.directoryTraversalEncoding_1.configure(state=NORMAL)
        self.directoryTraversalEncoding_2.configure(state=NORMAL)
        self.directoryTraversalEncoding_3.configure(state=NORMAL)
        self.directoryTraversalEncoding_1.select()
        self.text_cookie.configure(state=NORMAL)
        self.text_cookie.delete(0, END)
        self.text_cookie.configure(state=DISABLED)
        self.checkbutton_auth.deselect()
        self.upload_label.configure(text="")
        self.text_skipLine.configure(state=NORMAL)
        self.text_skipLine.delete(0, END)
        self.text_skipLine.configure(state=DISABLED)
        self.checkbutton_skipLine.deselect()
        self.xMode.set('1')
        self.setFileMode()
        self.entry_host.delete(0, END)
        self.entry_user.delete(0, END)
        self.entry_pw.delete(0, END)
        
    # Browse file system to get file to use for requests
    def browseFile(self):
        self.selectedFileName = tkFileDialog.askopenfilename(filetypes = ( ("Text files", "*.txt"), ("All files", "*.*") ))
        try:
            tmpFile = open(self.selectedFileName, 'r')
            self.editStatus('opened: %s' %self.selectedFileName, 3)
            tmpFile.close()
            selectedFileLength = len(self.selectedFileName)
            if selectedFileLength > 39:
                displayedFileName = '...' +self.selectedFileName[selectedFileLength -36:]
            else:
                displayedFileName = self.selectedFileName
                
            self.upload_label.configure(state=NORMAL, text='Selected file:  %s' %displayedFileName, foreground="darkblue")
            self.xMode.set('2')
            self.setFileMode()
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

    def pause_continue(self):
        if (self.startPressed == 1):
            if ( self.p_c == "c" ):
                self.p_c = "p"
                self.stopThread = 1
                self.lastLocation = self.lineCounter
                self.editStatus('-- Paused @ line: ' +str(self.lastLocation), 3)
            else:
                self.p_c = "c"
                self.stopThread = 0
                self.editStatus('-- Resume @ line: ' +str(self.lastLocation), 3)
                self.isContinue = 1
                self.progress["value"] = (self.lastLocation / float(self.totalLines)) * 100
                
                self.lineCounter = self.lastLocation
                self.executeRun()
        else:
            pass

    def stopPressed(self):
        #self.startPressed = 0
        self.filemenu.entryconfig("Run", state="normal")
        self.filemenu.entryconfig("Stop", state="disabled")
        self.filemenu.entryconfig("Pause / Continue", state="disabled")
        self.stopThread = 1
        if self.lineCounter > 1:
            current = self.lineCounter -1
            self.editStatus('Stopped @ line: %d' %current, 3)
            time.sleep(1)
            self.lineCounter = 0
        self.terminator()


############################################################################################################################################
        ############################################################ RUN #########################################################
                ############################################################################################################

    def executeRun(self):
        self.startPressed = 1
        self.editStatus("Initializing! please wait...", 1)
        if self.isContinue == 0:
            self.progress["value"] = 0
            # print Date to Results Tab
            self.lastTime = "\n\n*************************** [ %s ]***************************\n" %str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.progress["value"] = 3
            isMissing = 0
            self.onlyTypes = []
            self.excludeTypes = []

            # Connect to hose to get file
            if self.xMode.get() == "1":
                isMissing = self.findIfMissing()
                if isMissing == 1:
                    self.editStatus("Missing data. Please fill in and try again.", 1)
                    self.terminator()
                    return 0

                else:
                    self.editStatus('Connecting to host: %s,  please wait...' %self.entry_host.get(), 3)
                    self.progress["value"] = 10
                    self.getFileFromHost = 0
                    if self.sshHost() == 1:
                        self.progress["value"] = 25
                        self.editStatus('File transferred!', 3)
                    else:
                        self.editStatus('could not connect to host: %s.\nPlease try again or upload file manualy' %self.entry_host.get(), 3)
                        self.terminator()
                        return 0

            # using uploaded file if self.xMode.get() == "2":
            else:
                try:
                    tmpFile = open(self.selectedFileName, 'r')
                    self.removeStar(self.upload_button)

                except:
                    isMissing = 1

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
                    self.headers = { 'Cookie' : self.text_cookie.get() }
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
    # Check if mendatory fields are missing, if so - colors in Red
    def findIfMissing(self):
        isMissing = 0
        # is URL missing?
        self.URL_TEXT = self.text_url.get().strip()
        if len(self.URL_TEXT) < 1:
            isMissing = 1
            
        # is HOME DIR missing?
        self.homeDir_TEXT = self.text_homeDir.get().strip()
        if len(self.homeDir_TEXT) < 1:
            isMissing = 1 
                
        #is HOST missing
        self.host_TEXT = self.entry_host.get().strip()
        if len(self.host_TEXT) < 1:
            isMissing = 1 

        #is USER missing               
        self.user_TEXT = self.entry_user.get().strip()
        if len(self.user_TEXT) < 1:
            isMissing = 1

        #is PW missing
        self.pw_TEXT =  self.entry_pw.get().strip()
        if len(self.pw_TEXT) < 1:
            isMissing = 1

        return isMissing

    # find in "200 OK" is within selected response codes
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
        self.filemenu.entryconfig("Run", state="disabled")
        self.filemenu.entryconfig("Stop", state="normal")
        self.filemenu.entryconfig("Pause / Continue", state="normal")
        self.runIn200Mode = self.loc200()
        for word in self.word_list:
            if self.stopThread == 1:
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
                    res_html = myResponse.read()
                    myResponse.close()

                    if myResponse.getcode() == 200 and self.runIn200Mode != -1:
                        if ( self.isErrMsg.get() == 'n' or
                                    (self.isErrMsg.get() == 'y' and self.findErrorMessage(res_html) == 0) or
                                            (self.isFindMsg.get() == 'y' and self.findAccceptMessage(res_html) == 1) ):
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
                    self.terminator()


                except Exception as e:
                    if str(e) == "unknown url type: ":
                        pass

        if self.lineCounter == self.totalLines or self.lineCounter -1 == self.totalLines:
            self.finito()
            return 1
        
        else:
            self.editStatus('errrr... something went wrong!', 3)
            self.terminator()

    # gran finale!
    def finito(self):
        self.startPressed = 0
        self.lineCounter = 0
        for file in self.filesToClose:
            file.close()
        self.editStatus('                 ', 2)
        self.editStatus('** !!! Mission accomplished !!! **', 3)
        self.editStatus('Completed! You can view the results in the Results tab', 1)
        self.filemenu.entryconfig("Run", state="normal")
        self.filemenu.entryconfig("Stop", state="disabled")
        self.filemenu.entryconfig("Pause / Continue", state="disabled")  
        self.terminator()


    # execution is done with something wrong...
    def terminator(self):
        self.startPressed = 0
        self.progress["value"] = 0
        self.isContinue = 0
        self.lastLocation = 0
        self.lineCounter = 0
        for file in self.filesToClose:
            file.close()
        self.filemenu.entryconfig("Run", state="normal")
        self.filemenu.entryconfig("Stop", state="disabled")
        self.filemenu.entryconfig("Pause / Continue", state="disabled")   

    # returns list of  HTTP Status Codes selected by the user
    def getCodeSelection(self):
        i = 1
        selectedCodesList = []
        tmpList = self.listbox_codes.get(0, END)
        listLength = len(tmpList)
        for i in range(listLength):
            if self.listbox_codes.select_includes(i) == True:
                code = tmpList[i][0:3]
                selectedCodesList.append(code)
        if self.DlistofCodes != ['x']:
            self.editStatus('Using codes: ' +'; '.join(selectedCodesList), 3)
        return selectedCodesList

    # SSH to Host
    def sshHost(self):
        _fileName = 'locationOptions.txt'
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.entry_host.get() , port=int(self.entry_port.get()), username=self.entry_user.get(), password=self.entry_pw.get())
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
                self.ssh.exec_command('ls -R > ' +self.targetFile +'\n')
            
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

        dir = self.text_homeDir.get() +'/'
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
            newFile.write(self.URL_TEXT +'/../../../../../../../../../../../../../etc/passwd\n')

            # Creating list of home directories
            origDepth = dir.count('/')
            self.depth = origDepth -1
            myDirList = self.homeDir_TEXT.split('/')
            listLen = len(myDirList)
            tmpFolder = ''
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
            self.onlyTypes = []
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
                self.excludeTypes = []
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
        tmpTXT = self.pathEncoding.get()
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

    # receives a message and a string
    # returns:
    # 0 - if did not find string in message
    # 1 - if found
    def findAcceptMessage(self, str):
        if str.find(self.text_findMsg.get()) == -1:
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

    # 'Quit' button clicked
    def executeQuit(event=None):
        root.destroy()


#################### MAIN()  ####################
root = Tk()
root.title("Path Traverser v1.4")
# use ico (top-left)
ico_encoded = "AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAAMMOAADDDgAAAAAAAAAAAADulDn/7pQ5/+6UOf+srt7/OT2o/2Bbvf+MjtP/t7zj/+6UOf/ulDn/7pQ5/+6UOf/ulDn/7pQ5/+6UOf/ulDn/7pQ5/+6UOf/ulDn/7pQ5/2ZmvP8PEJn/FBKe/yYnp/9CQbL/amzA/52c1P/Fw+T/7pQ5/+6UOf/ulDn/7pQ5/+6UOf/ulDn/7pQ5/+6UOf/ulDn/NDOp/xIUoP8UEp//EhGd/xENnP8YFZz/JCOm/4N9w//ulDn/7pQ5/+6UOf/ulDn/7pQ5/+6UOf+Zl9b/7pQ5/5GQ0f8XGZ3/FhWf/xcXn/8XF57/FRSg/xAPnP+Cg8v/7pQ5/+6UOf/ulDn/7pQ5/+6UOf/ulDn/LjKn/+6UOf/ulDn/VFW1/xQTm/8XFp7/FxWe/xYVn/8fHKD/qqvY/+6UOf8WFp7/eHnF/+6UOf/ulDn/7pQ5/yckov9JTK7/7pQ5/6yw4P8iJKL/FRSe/xYUoP8SE53/Pz6r/+6UOf+ys97/tbLZ/xYWnv/ulDn/7pQ5/+6UOf8nJ6H/S0u1/+6UOf/ulDn/cHLC/xYVnv8UFZ3/GRme/5KW1f/ulDn/7pQ5/xYWnv+GhMn/7pQ5/+6UOf/ulDn/KCal/zMzrP+GiMv/hojQ/0hKtP8REZ3/Ghqe/3+CzP/ulDn/7pQ5/+6UOf/ulDn/ub3k/+6UOf/ulDn/7pQ5/zMup/8ZFZz/FxSb/xcUnf8hH6H/TlC0/6am2f/0nW//g4PM/42Tz/8WFp7/7pQ5/+6UOf/ulDn/7pQ5/+6UOf/ulDn/7pQ5/+6UOf/ulDn/7pQ5/+6UOf/ulDn/Zme+/+6UOf+/vOH/rqvb/7q74f/ulDn/7pQ5/+6UOf/ulDn/oKjX/6mp2f+fpdX/k5LR/3l3yf9bXr//bWjC/7i04P/ulDn/7pQ5/x0doP93dsT/7pQ5/+6UOf/ulDn/Y1+6/xkYn/9LSK//V1u6/2xkwP+Jic3/Fhae/+6UOf+Jjs3/Fhae/+6UOf/ulDn/Fhae/+6UOf/ulDn/mZfW/xgZnv9LULj/qKXa/4mCzf/ulDn/jpHO/xYWnv/ulDn/T1W3/xwXnv+Rkcr/7pQ5/+6UOf/ulDn/vrzl/y80q/8VFZ3/o6ba/4B/yv87Oq7/7pQ5/25xwv8WFp7/7pQ5/+6UOf9DRrP/sK7c/+6UOf/ulDn/7pQ5/4F1yP8gHaH/S0y0/+6UOf9MU7T/JySn/+6UOf/ulDn/Gxig/2lnwP/ulDn/7pQ5/+6UOf/ulDn/7pQ5/+6UOf8WFp7/Fhae/+6UOf/ulDn/aWfA/1NVt/9pZ8D/7pQ5/+6UOf/ulDn/7pQ5/+6UOf/ulDn/7pQ5/+6UOf/ulDn/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=="
ico_decoded = base64.b64decode(ico_encoded)
temp_file = "pt.ico"
fout = open(temp_file,"wb")
fout.write(ico_decoded)
fout.close()
root.wm_iconbitmap(temp_file)
os.remove(temp_file)
app = App(root)
root.mainloop()
