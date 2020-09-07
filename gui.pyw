import tkinter as tk
from methods import TeamCity


class MainWindow:
    def __init__(self, parent):
        self.parent = parent
        self.vars = {}

        self.branch = tk.StringVar()
        self.personal = tk.BooleanVar()
        self.message = tk.StringVar()
        self.message.set('Choose service and branch')

        frame = tk.Frame(self.parent)
        row = 1

        tooltip_label = tk.Label(frame, text='Select services and branch', underline=0)
        tooltip_label.grid(row=row, column=0, padx=2, pady=2, sticky=tk.W)
        row += 1

        row = self.init_services_checkboxes(frame, row)
        row += 1
        branch_label = tk.Label(frame, text='Branch', underline=0)
        branch_label.grid(row=row, column=0, padx=2, pady=2, sticky=tk.W)
        branch_entry = tk.Entry(frame, width=50, textvariable=self.branch)
        branch_entry.grid(row=row, column=1, columnspan=2, padx=2, pady=2, sticky=tk.EW)
        branch_button = tk.Button(frame, text='Get', command=self.get_branches, width=10)
        branch_button.grid(row=row, column=3, sticky=tk.W)
        row += 1

        self.branches_list = tk.Listbox(frame, height=0, selectmode=tk.SINGLE)
        self.branches_list.grid(row=row, column=0, padx=2, pady=2, sticky=tk.W)
        self.branches_list.bind('<<ListboxSelect>>', self.branches_list_select)
        row += 1

        tk.Checkbutton(frame, text='Personal build', variable=self.personal).grid(row=row, sticky=tk.W)
        row += 1

        start_button = tk.Button(frame, text='Start', command=self.start)
        start_button.grid(row=row, column=0, columnspan=4, padx=2, pady=2, sticky=tk.NSEW)
        row += 1

        self.message_label = tk.Label(frame, relief=tk.GROOVE, anchor=tk.W, bg='white',
                                      textvariable=self.message)
        self.message_label.grid(row=row, column=0, columnspan=4, padx=2, pady=2, sticky=tk.NSEW)

        frame.grid(row=0, column=0, sticky=tk.NSEW)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=999)
        frame.columnconfigure(2, weight=999)

        window = self.parent.winfo_toplevel()
        window.columnconfigure(0, weight=1)

        parent.bind('<Control-q>', self.quit)
        parent.bind('<Escape>', self.quit)
        parent.title('Teamcity utils')

    def start(self):
        services = [k for k, v in self.vars.items() if v.get()]
        if not services:
            self.show_error('Choose service')
            return

        branch = self.branch.get()
        if not branch:
            self.show_error('Choose branch')
            return

        self.show_info('Sending requests')
        personal = self.personal.get()
        all_ok = True
        msgs = []
        for s in services:
            ok, msg = tc.run_build(s, branch, personal)
            if not ok:
                all_ok = False
                msgs.append(msg)
        if all_ok:
            self.show_success()
        else:
            self.show_error(';\t'.join(msgs))

    def get_branches(self):
        service = None
        for k, v in self.vars.items():
            if v.get():
                service = k
                break
        if service is None:
            self.show_error('Choose service')
            return

        ok, branches = tc.get_branches(service)
        if ok:
            self.branches_list.insert(0, *branches)
            self.show_info('Branches fetched')
        else:
            self.show_error('An error occurred while executing the request ({})'.format(branches))
        return branches

    def init_services_checkboxes(self, frame, row):
        ok, services = tc.get_services()
        if not ok:
            self.show_error('Unable to get services')
            return

        col = 0
        cb_in_col = 3
        for key, name in services:
            var = tk.BooleanVar()
            tk.Checkbutton(frame, text=name, variable=var).grid(row=row, column=col, sticky=tk.W)
            self.vars[key] = var
            col += 1
            if col == cb_in_col:
                col = 0
                row += 1
        return row

    def branches_list_select(self, event):
        widget = event.widget
        selection = widget.curselection()
        if not selection:
            return
        selection_value = widget.get(selection[0])
        self.branch.set(selection_value)

    def show_error(self, text):
        self.message.set(text)
        self.message_label.config({'fg': 'black', 'bg': 'red'})

    def show_info(self, text):
        self.message.set(text)
        self.message_label.config({'fg': 'black', 'bg': 'white'})

    def show_success(self, text='Done!'):
        self.message.set(text)
        self.message_label.config({'fg': 'black', 'bg': 'green'})

    def quit(self):
        self.parent.destroy()


if __name__ == '__main__':
    tc = TeamCity()
    application = tk.Tk()
    window = MainWindow(application)
    application.protocol('WM_DELETE_WINDOW', window.quit)
    application.mainloop()
