from tkinter import *
import tkinter as tk
from P2P.node import Node
from threading import Thread


class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self)
        self.controller = controller

        label = tk.Label(self, text="Введите имя:", width=70)
        label.grid(row=1, column=1, padx=0, pady=10)
        self.page1_inpt = tk.Entry(self, width=30)
        self.page1_inpt.grid(row=2, column=1)
        auth_btn = tk.Button(self, text='Войти', command=self.authentication, height=0)
        auth_btn.grid(row=3, column=1, padx=0, pady=20)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.name_value = ''
        self.old_value = ''

    def authentication(self):
        self.name_value = self.page1_inpt.get()
        self.page1_inpt.delete(0, 'end')
        print(self.name_value)

        self.controller.node = Node((5, 5))
        thr = Thread(target=self.controller.node.start_working)
        thr.start()
        # thr.join()

        if self.old_value != self.name_value:
            label = tk.Label(self.controller.frames[Page2], text=self.name_value, width=70)
            label.grid(row=2, column=1, padx=0, pady=20)
            self.old_value = self.name_value
        self.controller.frames[Page2].lift()


class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self)
        self.controller = controller
        self.value = ''

        auth_btn = tk.Button(self, text='Посмотреть список соединений', command=self.connections, height=0)
        auth_btn.grid(row=3, column=1, padx=0, pady=20)
        self.grid_columnconfigure(1, weight=1)

    def connections(self):
        print('djkf')
        print(self.controller.node.message_table)

        messages = self.controller.node.message_table

        list_msg = Listbox(self.controller.frames[Page2], height=len(messages) + 2, width=30)
        list_msg.delete(0, len(messages) + 2)
        list_msg.grid(row=4, column=1, padx=0, pady=20)
        for i in messages:
            list_msg.insert(0, i)


class Page3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self)
        self.controller = controller

        label = tk.Label(self, text="This is page 3")
        label.pack(side="top", fill="both")


class Controller(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        self.old_value = ''
        self.node = None

        for F in (Page1, Page2, Page3):
            frame = F(container, self)
            frame.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
            self.frames[F] = frame

        b1 = tk.Button(buttonframe, text="Авторизация", command=self.frames[Page1].lift)
        b2 = tk.Button(buttonframe, text="Личный кабинет", command=self.frames[Page2].lift)
        b3 = tk.Button(buttonframe, text="Page 3", command=self.frames[Page3].lift)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        self.show_frame(Page1)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_page(self, classname):
        for page in self.frames.values():
            if str(page.__class__.__name__) == classname:
                return page
        return None


if __name__ == "__main__":
    app = Controller()
    app.title('Blockchain')
    app.wm_geometry("600x700")
    app.mainloop()