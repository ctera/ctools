import status
from status import run_status
from login import login
from unlock import unlock,start_ssh
from run_cmd import run_cmd
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from cterasdk import *
import logging
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
font_sty='Times New Roman'
color='#4e5be7'
fgcolor='White'



class Menu():
    def __init__(self,**kwargs):
        self.root=Tk()
        #self.root.geometry('500x420')
        Menu.center_window(self,self.root)
        self.root.configure(bg=color)
        self.root.title('CTools')
        self.root.after(1000,self.root.focus_force)
        self.help='''
        Have Feedback?
        Email mukeshj@ctera.com / todd@ctera.com
        '''
        Top_frame=Frame(self.root, bg=color)
        Top_frame.pack(fill='x',pady=10)
        Label(Top_frame, text='CTools', font=(font_sty, 28, 'bold'),
                    fg=fgcolor, bg=color).pack(side=LEFT, anchor=NW, padx=10)
        Button(Top_frame, text='Help?', font=(font_sty, 12, 'bold'), bd=0,
                    width=5,fg=fgcolor, bg=color,
               command= lambda: messagebox.showinfo("Help", self.help) ).pack(side=RIGHT, anchor=NE, padx=0)

        Select_frame=LabelFrame(self.root, text="Select one option", font=(font_sty, 16, 'bold'),
                                fg=color, bg=fgcolor, padx=20, pady=40)
        Select_frame.pack(side=TOP,anchor=CENTER, pady=30)
        # Combo box
        Selected_Option = ttk.Combobox(Select_frame, width=60, font=(font_sty, 14), justify='center', state="readonly")
        Selected_Option['values'] = ('Record status details of all connected Edge Filers',
                                     'Run a specified command on all connected Edge Filers',
                                     'Enable telnet on an Edge Filer, Virtual, or C-Series Gateway',
                                     'Enable SSH on an Edge Filer')
        Selected_Option.current(0)
        Selected_Option.pack(side=TOP)

        Button(self.root, text='Next',
               width=10, font=(font_sty, 18, 'bold'), bd=2, bg='lightgray', #fg='White',
               command= lambda: Menu.proceed(self,Selected_Option)).pack(side=BOTTOM, pady=50)
        self.root.mainloop()
    def proceed(self, Selected_Option):
        if Selected_Option.current() == 0:
            print('run_status')
            Menu.First_window(self)
        elif Selected_Option.current() == 1:
            print("second")
            Menu.Second_window(self)
        elif Selected_Option.current() == 2:
            print("third")
            Menu.Third_window(self)
        elif Selected_Option.current() == 3:
            Menu.Fourth_window(self)

    def First_window(self):
        self.root.withdraw()
        f_window=Toplevel(self.root)
        f_window.geometry(f'{width}''x'f'{height}''+'f'{x_cord}''+'f'{y_cord}')
        f_window.configure(bg=color)
        f_window.title('CTools')
        F_1=LabelFrame(f_window,text='Enter Output Filename', font=(font_sty, 16, 'bold')
                       ,bg=color, fg=fgcolor, padx=10, pady=10)
        F_1.pack(pady=10, padx=10, fill='x')
        Label(F_1, text='Make sure extension is csv:', font=(font_sty, 14, 'bold'),
              bg=color, fg=fgcolor).pack(side=LEFT, anchor=NW, padx=4)
        global File_name
        File_name=Entry(F_1, font=(font_sty, 14), bd=3 )
        File_name.pack(side=LEFT, anchor=NW, padx=7)

        Menu.Portal(self,f_window,1)
        f_window.wait_window()
        self.root.deiconify()

    def Second_window(self):
        self.root.withdraw()
        f_window=Toplevel(self.root)
        f_window.geometry(f'{width}''x'f'{height}''+'f'{x_cord}''+'f'{y_cord}')
        f_window.configure(bg=color)
        f_window.title('CTools')
        F_1=LabelFrame(f_window,text='Enter Information', font=(font_sty, 16, 'bold')
                       ,bg=color, fg=fgcolor, padx=10, pady=10)
        F_1.pack(pady=10, padx=10, fill='x')
        device_label=Label(F_1, text='Enter device name:', font=(font_sty, 14, 'bold'),
              bg=color, fg=fgcolor, justify=LEFT)
        device_label.grid(sticky=W,row=0, column=0, padx=3, pady=3)
        global Device_name, tenant_p, Unlock_code
        Device_name=Entry(F_1, font=(font_sty, 14), bd=3)
        Device_name.grid(row=0, column=1, padx=3, pady=3)

        Label(F_1, text='Enter tenant portal:', font=(font_sty, 14, 'bold'), justify=LEFT,
              bg=color, fg=fgcolor).grid(sticky=W, row=1, column=0, padx=3, pady=3)
        tenant_p=Entry(F_1, font=(font_sty, 14), bd=3)
        tenant_p.grid(row=1, column=1, padx=3, pady=3)

        Label(F_1, text='Enter Unlock Code:', font=(font_sty, 14, 'bold'), justify=LEFT,
              bg=color, fg=fgcolor).grid(sticky=W, row=2, column=0, padx=3, pady=3)
        Unlock_code=Entry(F_1, font=(font_sty, 14), bd=3)
        Unlock_code.grid(row=2, column=1, padx=3, pady=3)
        Menu.Portal(self,f_window, 2)
        f_window.wait_window()
        self.root.deiconify()

    def Third_window(self):
        self.root.withdraw()
        f_window=Toplevel(self.root)
        f_window.geometry(f'{width}''x'f'{height}''+'f'{x_cord}''+'f'{y_cord}')
        f_window.configure(bg=color)
        f_window.title('CTools')

        F_1=LabelFrame(f_window,text='Command Info', font=(font_sty, 16, 'bold')
                       ,bg=color, fg=fgcolor, padx=10, pady=10)
        F_1.pack(pady=10, padx=10, fill='x')
        Label(F_1, text='Enter command to run:', font=(font_sty, 14, 'bold'),
              bg=color, fg=fgcolor).pack(side=LEFT, anchor=NW, padx=4)
        global command_run
        command_run = Entry(F_1, font=(font_sty, 14), bd=3, width=30)
        command_run.pack(side=LEFT, anchor=NW, padx=2)
        Menu.Portal(self,f_window, 3)
        f_window.wait_window()
        self.root.deiconify()

    def Fourth_window(self):
        self.root.withdraw()
        f_window=Toplevel(self.root)
        f_window.geometry(f'{width}''x'f'{height}''+'f'{x_cord}''+'f'{y_cord}')
        f_window.configure(bg=color)
        f_window.title('CTools')

        F_1=LabelFrame(f_window,text='Start_ssh', font=(font_sty, 16, 'bold')
                       ,bg=color, fg=fgcolor, padx=10, pady=10)
        F_1.pack(pady=10, padx=10, fill='x')
        Label(F_1, text='Enter the public key:', font=(font_sty, 14, 'bold'),
              bg=color, fg=fgcolor).pack(side=LEFT, anchor=NW, padx=4)
        global pubkey
        pubkey = Entry(F_1, font=(font_sty, 14), bd=3, width=30)
        pubkey.pack(side=LEFT, anchor=NW, padx=2)
        Menu.Portal(self,f_window, 3)
        f_window.wait_window()
        self.root.deiconify()


    def Portal(self,window_name, screen):
        Frame_1 = LabelFrame(window_name, text='Portal Info', font=(font_sty, 16, 'bold')
                         , bg=color, fg=fgcolor, padx=10, pady=10)
        Frame_1.pack(pady=10, padx=10, fill='x')
        Label(Frame_1, text='(IP/Hostname/FQDN):', font=(font_sty, 14, 'bold'), justify=LEFT,
              bg=color, fg=fgcolor).grid(sticky=W, row=0, column=0, padx=5, pady=3)
        portal_name = Entry(Frame_1, font=(font_sty, 14), bd=3)
        portal_name.grid(row=0, column=1, padx=3,  pady=3)
        Label(Frame_1, text='Admin Username:', font=(font_sty, 14, 'bold'), justify=LEFT,
              bg=color, fg=fgcolor).grid(sticky=W, row=1, column=0, padx=5, pady=3)
        Admin_name = Entry(Frame_1, font=(font_sty, 14), bd=3)
        Admin_name.grid(row=1, column=1, padx=3, pady=3)
        Label(Frame_1, text='Password:', font=(font_sty, 14, 'bold'),
              bg=color, fg=fgcolor).grid(sticky=W, row=2, column=0, padx=5, pady=3)
        Password = Entry(Frame_1, font=(font_sty, 14), bd=3, show='*')
        Password.grid(row=2, column=1, padx=3,  pady=3)
        Btn_frame = Frame(window_name, bg=color)
        Btn_frame.pack(side=BOTTOM, pady=10)
        Button(Btn_frame, text='Back',
               width=10, font=(font_sty, 18, 'bold'), bd=3, bg='lightgray',# fg='',
               command=lambda: window_name.destroy()
               ).pack(side=LEFT, padx=10)
        Button(Btn_frame, text='Next',
               width=10, font=(font_sty, 18, 'bold'), bd=3, bg='lightgray',# fg='',
               command=lambda: Menu.operation(None,window_name,screen, portal_name,Admin_name, Password)
               ).pack(side=LEFT, padx=10)

    def operation(self,window,screen, portal_name,Admin_name, Password):
        if screen == 1:
            run_status('G', File_name.get(), portal_name.get(), Admin_name.get(), Password.get())
            window.destroy()
        elif screen == 2:
            unlock('G', portal_name.get(), Admin_name.get(), Password.get(),Device_name, tenant_p, Unlock_code)
            window.destroy()
        elif screen == 3:
            run_cmd('G', portal_name.get(), Admin_name.get(), Password.get(), command_run)
            window.destroy()
        else:
            start_ssh('G', portal_name.get(), Admin_name.get(), Password.get(), pubkey)
            window.destroy()

    def center_window(self, window):
        global x_cord, y_cord, width, height
        width, height = 700, 420  # 500 x 420
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_cord = int((screen_width / 2) - (width / 2))
        y_cord = int((screen_height / 2.6) - (height / 2.6))
        self.root.geometry("{}x{}+{}+{}".format(width,
                                                height,
                                                x_cord,
                                                y_cord))

