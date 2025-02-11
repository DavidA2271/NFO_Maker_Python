from tkinter import Frame
from custom_widgets import *
import os


class TvShowWidget(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure((0,1,2), weight=1)
        
        self.title_entry = DefaultEntry(self, 'Title...')
        self.title_entry.grid(row=0, column=0, pady=(20,5), columnspan=3)
        
        self.year_entry = DefaultEntry(self, 'YYYY-MM-DD')
        self.year_entry.grid(row=1, column=0, pady=5, columnspan=3)
        
        self.plot_entry = DefaultTextBox(self, 'Plot...', height=5, width=32)
        self.plot_entry.grid(row=2, column=0, padx=50, pady=(5, 10), columnspan=3)

        self.genres = []

        for i in range(0, 9):
            row = int(i/3) + 3
            column = i%3
            genre_entry = DefaultEntry(self, 'Genre...')
            self.genres.append(genre_entry)
            genre_entry.grid(row=row, column=column, sticky='ew')
        
        self.studio_entry = DefaultEntry(self, 'Studio...')
        self.studio_entry.grid(row=6, column=0, pady=5, columnspan=3)

    def get_nfo_lines(self):
        nfo_lines = [
            '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>',
            '<tvshow>',
            f'\t<title>{self.title_entry.get()}</title>',
            f'\t<premiered>{self.year_entry.get()}</premiered>',
            f'\t<plot>{self.plot_entry.get(1.0, "end").strip()}</plot>',
            '\t<uniqueid type="tmdb" default="true"></uniqueid>',
            '\t<status>Ended</status>'
        ]
        for g in self.genres:
            if g.valid():
                nfo_lines.append(f'\t<genre>{g.get()}</genre>')
        if self.studio_entry.valid():
            nfo_lines.append(f'\t<studio>{self.studio_entry.get()}</studio>')
        nfo_lines.append('</tvshow>')
        return nfo_lines
    
    def get_show_path(self, root_path):
        return os.path.join(root_path, self.title_entry.get())
    