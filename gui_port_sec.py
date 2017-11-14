from tkinter import *
import Portsec


class Application(Frame):
    """docstring for Application"""

    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid(row=5, column=5)
        self.create_widgets()

    def create_widgets(self):
        self.lbl_path_utc = Label(self, text='mac адресс ')
        self.lbl_path_utc.grid(row=2, column=0, columnspan=4, sticky=W)
        self.mac = Entry(self, width=55)
        self.mac.grid(row=3, column=0, columnspan=2, sticky=W)

        self.ip_com = Label(self, text='ip комутатора:')
        self.ip_com.grid(row=4, column=0, columnspan=4, sticky=W)
        self.ip_com = Entry(self, width=55)
        self.ip_com.grid(row=5, column=0, columnspan=2, sticky=W)

        self.login = Label(self, text='login')
        self.login.grid(row=6, column=0, columnspan=4, sticky=W)
        self.login = Entry(self, width=55)
        self.login.grid(row=7, column=0, columnspan=2, sticky=W)

        self.pwd = Label(self, text='password')
        self.pwd.grid(row=8, column=0, columnspan=4, sticky=W)
        self.pwd = Entry(self, width=55)
        self.pwd.grid(row=9, column=0, columnspan=2, sticky=W)

        self.ok_bttn = Button(self, text="Start", command= self.clear_port)
        self.ok_bttn.grid(row=10, column=0, sticky=W)

        self.ok_bttn = Button(self, text="Save", command= '')
        self.ok_bttn.grid(row=10, column=1, sticky=W)


    def clear_port(self):
        Portsec.clr_port(self.mac.get(),
                         self.ip_com.get(),
                         self.login.get(),
                         self.pwd.get())


root = Tk()
root.title("Clear interface")
root.geometry("350x300")
app = Application(root)
root.mainloop()