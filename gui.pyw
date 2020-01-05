import tkinter
from .methods import TeamCity


class MainWindow:
    def __init__(self, parent):
        self.parent = parent
        self.vars = {}

        self.branch = tkinter.StringVar()
        self.message = tkinter.StringVar()
        self.message.set('Choose service and branch')

        frame = tkinter.Frame(self.parent)

        row = 1
        tooltip_label = tkinter.Label(frame, text="Select services and branch", underline=0)
        tooltip_label.grid(row=row, column=0, padx=2, pady=2, sticky=tkinter.W)
        row += 1

        row = self.init_services_checkboxes(frame, row)
        branch_label = tkinter.Label(frame, text="Branch", underline=0)
        branch_label.grid(row=row, column=0, padx=2, pady=2, sticky=tkinter.W)
        branch_entry = tkinter.Entry(frame, width=50, textvariable=self.branch)
        branch_entry.grid(row=row, column=1, columnspan=2, padx=2, pady=2, sticky=tkinter.EW)
        branch_button = tkinter.Button(frame, text="Get", command=self.get_branches, width=10)
        branch_button.grid(row=row, column=3, sticky=tkinter.W)
        row += 1

        start_button = tkinter.Button(frame, text="Start", command=self.start)
        start_button.grid(row=row, column=0, columnspan=4, padx=2, pady=2, sticky=tkinter.NSEW)
        row += 1

        self.message_label = tkinter.Label(frame, relief=tkinter.GROOVE, anchor=tkinter.W,
                                           bg="white", textvariable=self.message)
        self.message_label.grid(row=row, column=0, columnspan=4, padx=2,
                                pady=2, sticky=tkinter.NSEW)

        frame.grid(row=0, column=0, sticky=tkinter.NSEW)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=999)
        frame.columnconfigure(2, weight=999)

        window = self.parent.winfo_toplevel()
        window.columnconfigure(0, weight=1)

        parent.bind("<Control-q>", self.quit)
        parent.bind("<Escape>", self.quit)
        parent.title("Teamcity utils")

    def start(self):
        services = [k for k, v in self.vars.items() if v.get()]
        if not services:
            self.message.set('Choose service')
            self.message_label.config({'fg': 'white', 'bg': 'red'})
            return
        if not self.branch.get():
            self.message.set('Choose branch')
            self.message_label.config({'fg': 'white', 'bg': 'red'})
            return

        self.message.set('Sending requests')
        self.message_label.config({'fg': 'black', 'bg': 'white'})
        # main()

    def get_branches(self):
        service = None
        for k, v in self.vars.items():
            if v.get():
                service = k
                break
        if service is None:
            self.message.set('Choose service')
            self.message_label.config({'fg': 'white', 'bg': 'red'})
            return
        ok, branches = tc.get_branches(service)
        return branches

    def quit(self, event=None):
        self.parent.destroy()

    def init_services_checkboxes(self, frame, row):
        ok, services = tc.get_services()
        if not ok:
            self.message.set('Unable to get services')
            self.message_label.config({'fg': 'white', 'bg': 'red'})
            return

        for key, name in services:
            var = tkinter.BooleanVar()
            tkinter.Checkbutton(frame, text=name, variable=var).grid(row=row, sticky=tkinter.W)
            self.vars[key] = var
            row += 1
        return row


if __name__ == '__main__':
    application = tkinter.Tk()
    window = MainWindow(application)
    application.protocol("WM_DELETE_WINDOW", window.quit)
    tc = TeamCity()
    application.mainloop()