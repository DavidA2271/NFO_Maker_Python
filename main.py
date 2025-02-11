import sys
from tkinter import *
import os
from tkinter.ttk import Notebook
from tvshow import TvShowWidget
from season import SeasonWidgetHolder


class MainScreen:
    def __init__(self, root: Tk):
        self.root = root
        self.root.configure(background='blue')
        self.frame = Frame(self.root, background='red')
        self.setup()

    def setup(self):
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid(row=0, column=0, sticky='nsew')

        self.tabControl = Notebook(self.frame)
        self.tabControl.bind("<<NotebookTabChanged>>", self.makeNewSeason)
        self.tabControl.bind('<Button-3>', self.delete_season)
        
        self.aw = TvShowWidget(self.tabControl)
        self.seasons: list[SeasonWidgetHolder] = []
        swh = SeasonWidgetHolder(self.tabControl)
        self.seasons.append(swh)
        plus = Frame(self.tabControl)

        self.tabControl.add(self.aw, text='TV Show', sticky='nsew', padding=(80,10,80,10))
        self.tabControl.add(swh, text='Season', sticky='nsew', padding=(20,20,20,10))
        self.tabControl.add(plus, text='+', sticky='nsew', padding=(20,20,20,10))
        self.tabControl.grid(row=0, column=0, sticky='nsew')

        self.nfo_button = Button(self.frame, text="Make NFO", command=self.make_nfo)
        self.nfo_button.grid(row=1, column=0, sticky='e')

    def makeNewSeason(self, event):
        if self.tabControl.select() == self.tabControl.tabs()[-1]:
            index = len(self.tabControl.tabs())-1
            frame = SeasonWidgetHolder(self.tabControl)
            self.seasons.append(frame)
            self.tabControl.insert(index, frame, text="Season", sticky='nsew', padding=(20,20,20,10))
            self.tabControl.select(index)

    def delete_season(self, event):
        if self.tabControl.select() == self.tabControl.tabs()[-2] and len(self.seasons) > 0:
            self.seasons.pop()
            self.tabControl.select(self.tabControl.tabs()[-3])
            for item in self.tabControl.winfo_children():
                if str(item)==self.tabControl.tabs()[-2]:
                    item.destroy()
                    break

    def make_nfo(self):
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        shows_path = os.path.join(application_path, 'Shows')
        if not os.path.exists(shows_path):
            os.mkdir(shows_path)

        if self.aw.title_entry.valid() and self.aw.plot_entry.valid():
            tv_path = self.aw.get_show_path(shows_path)
            if not os.path.exists(tv_path):
                os.mkdir(tv_path)
            tv_nfo_path = os.path.join(tv_path, 'tvshow.nfo')
            tv_lines = self.aw.get_nfo_lines()
            with open(tv_nfo_path, 'w') as f:
                for line in tv_lines:
                    f.write(f"{line}\n")

        for s in self.seasons:
            if s.season_entry.valid() and len(s.episodes) > 0:
                season_path = s.get_season_path(tv_path)
                if not os.path.exists(season_path):
                    os.mkdir(season_path)
                for e in s.episodes:
                    episode_file_path = s.get_file_path(season_path, self.aw.title_entry.get(), e)
                    ep_lines = s.get_nfo_lines(e)
                    with open(episode_file_path, 'w') as f:
                        for line in ep_lines:
                            f.write(f"{line}\n")        


class App(Tk):
    def __init__(self):
        super().__init__()
        self.setupRoot()
        ms = MainScreen(self)

    def setupRoot(self):
        self.minsize(600, 400)
        self.title("NFO Maker")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


if __name__ == '__main__':
    app = App()
    app.mainloop()
