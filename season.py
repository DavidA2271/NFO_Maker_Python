from tkinter import Button, Frame, Canvas, IntVar, Scrollbar, Label, Checkbutton
from custom_widgets import *
import os
import datetime


class SeasonWidgetHolder(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.rowconfigure(6, weight=1)
        
        self.season_entry = DefaultEntry(self, 'Season #')
        self.season_entry.grid(row=0, column=0, pady=5, columnspan=2)
        
        self.episode_entry = DefaultEntry(self, 'Episode #')
        self.episode_entry.grid(row=1, column=0, pady=5, columnspan=2)

        self.air_entry = DefaultEntry(self, 'Air Date...')
        self.air_entry.grid(row=2, column=0, pady=5, columnspan=2)

        self.runtime_entry = DefaultEntry(self, 'Runtime...')
        self.runtime_entry.grid(row=3, column=0, pady=5, columnspan=2)

        self.ova = IntVar()
        self.special = IntVar()
        ova_check = Checkbutton(self, text='OVA', variable=self.ova)
        special_check = Checkbutton(self, text='Special', variable=self.special)
        ova_check.grid(row=4, column=0, pady=5)
        special_check.grid(row=4, column=1, pady=5)

        ep_gen_btn = Button(self, text='Make Episodes', command=self.generate_episodes)
        ep_gen_btn.grid(row=5, column=0, pady=5, columnspan=2)

        extra_frame = Frame(self)
        extra_frame.grid(row=6, column=0, columnspan=2)

        self.episodes = []

        container = Frame(self, bg='red')
        container.grid(row=0, column=2, rowspan=7, sticky='nw')
        cv = Canvas(container, bg='blue', width=400,height=400)
        vbar=Scrollbar(container, orient='vertical', command=cv.yview)
        self.sf = Frame(cv, bg='pink')
        self.sf.columnconfigure(1, weight=1)

        self.sf.bind(
            "<Configure>",
            lambda e: cv.configure(
                scrollregion=cv.bbox("all")
            )
        )

        cv.create_window((0, 0), window=self.sf, anchor="nw")
        cv.config(yscrollcommand=vbar.set)

        cv.grid(row=0, column=0)
        vbar.grid(column=1, row=0, sticky='ns')

    def generate_episodes(self):
        eps_str = self.episode_entry.get()
        try:
            eps = int(eps_str)
        except Exception:
            return
        for i in range(0, eps):
            ep_num_label = Label(self.sf, text=f"Episode {i+1}.")
            title_entry = DefaultEntry(self.sf, 'Title...', width=32)
            plot_text = DefaultTextBox(self.sf, 'Plot...', height=5, width=48)
            self.episodes.append((title_entry, plot_text, i+1))
            ep_num_label.grid(row=i*2, column=0, sticky='nw', padx=10, pady=(5,2))
            title_entry.grid(row=i*2, column=1, sticky='nw', padx=(0,10), pady=(5,2))
            plot_text.grid(row=i*2+1, column=0, sticky='new', padx=10, pady=(0,2), columnspan=2)
    
    def get_nfo_lines(self, episode):
        day_passed = (int(episode[2]) - 1) * 7
        air_date = datetime.date.fromisoformat(self.air_entry.get())
        air_date += datetime.timedelta(days=day_passed)
        nfo_lines = [
            '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>',
            '<episodedetails>',
            f'\t<title>{episode[0].get()}</title>',
            f'\t<season>{self.season_entry.get()}</season>',
            f'\t<episode>{episode[2]}</episode>',
            f'\t<plot>{episode[1].get(1.0, "end").strip()}</plot>',
            '\t<uniqueid type="tmdb" default="true"></uniqueid>',
            f'\t<aired>{air_date}</aired>',
            '</episodedetails>'
        ]
        return nfo_lines

    def get_season_path(self, show_path):
        season = self.season_entry.get()
        if self.ova.get() == 1:
            season += '01'
        elif self.special.get() == 1:
            season += '02'
        return os.path.join(show_path, f'Season {season}')
    
    def get_file_path(self, season_path, show_title, episode):
        season = self.season_entry.get()
        if self.ova.get() == 1:
            season += '01'
        elif self.special.get() == 1:
            season += '02'
        season = 'S' + '{:02d}'.format(int(season))
        episode_number = 'E' + '{:02d}'.format(int(episode[2]))
        fn = show_title + ' - ' + season + episode_number + ' - ' + episode[0].get() + '.nfo'
        return os.path.join(season_path, fn)
