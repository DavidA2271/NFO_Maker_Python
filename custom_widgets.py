from tkinter import Entry, Text


class DefaultEntry(Entry):
    def __init__(self, master, default_text, *args, **kwargs):
        super().__init__(master, bg='white', fg='grey', *args, **kwargs)
        self.default_text = default_text
        self.insert(0, default_text)
        self.bind("<FocusIn>", self.handle_focus_in)
        self.bind("<FocusOut>", self.handle_focus_out)

    def handle_focus_in(self, _):
        if self.get() == self.default_text:
            super().delete(0, 'end')
            super().config(fg='black')

    def handle_focus_out(self, _):
        if self.get() == "":
            super().delete(0, 'end')
            super().config(fg='grey')
            super().insert(0, self.default_text)

    def valid(self):
        if self.get() == self.default_text:
            return False
        elif self.get() == "":
            return False
        return True


class DefaultTextBox(Text):
    def __init__(self, master, default_text, *args, **kwargs):
        super().__init__(master, bg='white', fg='grey', *args, **kwargs)
        self.default_text = default_text
        self.insert(1.0, default_text)
        self.bind("<FocusIn>", self.handle_focus_in)
        self.bind("<FocusOut>", self.handle_focus_out)

    def handle_focus_in(self, _):
        if self.get(1.0, 'end').strip() == self.default_text:
            super().delete(1.0, 'end')
            super().config(fg='black')

    def handle_focus_out(self, _):
        if self.get(1.0, 'end').strip() == "":
            super().delete(1.0, 'end')
            super().config(fg='grey')
            super().insert(1.0, self.default_text)
    
    def valid(self):
        if self.get(1.0, 'end').strip() == self.default_text:
            return False
        elif self.get(1.0, 'end').strip() == "":
            return False
        return True