from tkinter import *
import main
class Generator:

    def __init__(self, master):
        self.master = master
        master.title("Natural Language Generator")

        self.entered_number = ""

        self.input = Listbox(selectmode=SINGLE, width=130, height=20)
        self.index = 0

        self.lexicon_input = Listbox(selectmode=SINGLE, width=130, height=20)
        self.lexicon_index = 0

        self.lexicon_input_text = StringVar()

        self.lexicon_label = Label(master, text="Lexicon Input: bspw. Subject('m', \"hund\", known=True),"
                                                " for Attributes: Attribute(\"<object>\", \"value\", known=True)")

        self.total_label_text = StringVar()

        self.label = Label(master, text="Input: bspw. {\"proposition: \"subject\", \"subject\": \"hund\"}")

        vcmd_lexicon = master.register(self.validate)
        self.lexicon_entry = Entry(master, validate="key", validatecommand=(vcmd_lexicon, '%P'))

        vcmd = master.register(self.validate) # we have to wrap the command
        self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

        def enter_lexicon(event):
            self.update_lexicon("add")

        def enter(event):
            self.update("add")

        self.lexicon_entry.bind('<Return>', enter_lexicon)
        self.entry.bind('<Return>', enter)

        self.add_button = Button(master, text="+", command=lambda: self.update("add"))
        self.subtract_button = Button(master, text="-", command=lambda: self.update("subtract"))
        self.reset_button = Button(master, text="Reset", command=lambda: self.update("reset"))
        self.generate_button = Button(master, text="Generate", command=self.generate)
        self.edit_button = Button(master, text="Edit", command=lambda: self.update("edit"))

        self.add_button_lexicon = Button(master, text="+", command=lambda: self.update_lexicon("add"))
        self.subtract_button_lexicon = Button(master, text="-", command=lambda: self.update_lexicon("subtract"))
        self.reset_button_lexicon = Button(master, text="Reset", command=lambda: self.update_lexicon("reset"))
        self.edit_button_lexicon = Button(master, text="Edit", command=lambda: self.update_lexicon("edit"))

        # LAYOUT

        self.label.grid(row=0, column=0, columnspan=5, sticky=W)

        self.entry.grid(row=1, column=0, columnspan=5, sticky=W+E)
        self.input.grid(row=2, column=0, columnspan=5)

        self.add_button.grid(row=3, column=0, sticky=W)
        self.subtract_button.grid(row=3, column=1, sticky=W)
        self.edit_button.grid(row=3, column=2, sticky=W)
        self.reset_button.grid(row=3, column=3, sticky=W)
        self.generate_button.grid(row=3, column=4, sticky=W)

        self.lexicon_label.grid(row=5, column=0, columnspan=5, sticky=W)

        self.lexicon_entry.grid(row=6, column=0, columnspan=5, sticky=W+E)
        self.lexicon_input.grid(row=7, column=0, columnspan=5)

        self.add_button_lexicon.grid(row=8, column=0, sticky=W)
        self.subtract_button_lexicon.grid(row=8, column=1, sticky=W)
        self.edit_button_lexicon.grid(row=8, column=2, sticky=W)
        self.reset_button_lexicon.grid(row=8, column=3, sticky=W)


    def validate(self, new_text):
        if not new_text: # the field is being cleared
            self.entered_number = ""
            return True

        try:
            self.entered_number = new_text
            return True
        except ValueError:
            return False

    def update(self, method):
        if method == "add":
            if self.entered_number != "":
                self.index += 1
                self.input.insert(self.index, self.entered_number)
                self.entry.delete(0, END)

        elif method == "subtract":
            self.input.delete(self.input.curselection())
            self.entry.delete(0, END)

        elif method == "edit":
            self.entry.insert(0, self.input.get(self.input.curselection()))

        else: # reset
            self.input.delete(0, self.input.size())
            self.entry.delete(0, END)

    def update_lexicon(self, method):
        if method == "add":
            if self.entered_number != "":
                self.lexicon_index += 1
                self.lexicon_input.insert(self.lexicon_index, self.entered_number)
                self.lexicon_entry.delete(0, END)

        elif method == "subtract":
            self.lexicon_input.delete(self.lexicon_input.curselection())
            self.lexicon_entry.delete(0, END)

        elif method == "edit":
            self.lexicon_entry.insert(0, self.lexicon_input.get(self.lexicon_input.curselection()))

        else: # reset
            self.lexicon_input.delete(0, self.lexicon_input.size())
            self.lexicon_entry.delete(0, END)
    def generate(self):
        main.main(self.input.get(0, self.input.size()), self.lexicon_input.get(0, self.lexicon_input.size()))

root = Tk()
root.geometry("800x800")

my_gui = Generator(root)
root.mainloop()
