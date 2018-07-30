import curses
from browser import folder

class ncurses_state:
    def __init__( self, screen, handlers ):
        self.screen = screen
        self.handlers = handlers
        self.folder_count = 0
        self.file_count = 0
        self.entry_count = 0
        self.selected_row = -1
        self.lines = []
        self.set_active_folder( folder("/") )
        self.display_active_folder()
        
    def set_active_folder( self, f ):
        self.active_folder = f
        self.active_folder.fetch_contents()

    def set_folder_count( self, f ):
        self.folder_count = f

    def set_entry_count(self, c):
        self.entry_count = c
        self.num_files = self.entry_count - self.folder_count

    def display_active_folder(self):
        self.screen.erase()
        row = 0
        self.lines = []
        for name in self.active_folder.subfolders():
            self.lines += [ name + "/" ]
            self.screen.addstr(row, 0, self.lines[-1])
            row += 1
        self.folder_count = row
        for name in self.active_folder.file_names():
            self.lines += [name]
            self.screen.addstr(row, 0, self.lines[-1])
            row += 1
        self.entry_count = row
        self.selected_row = 0
        self.highlight_current_row()

    def unhighlight_current_row(self):
        self.screen.addstr(self.selected_row, 0,
                           self.lines[self.selected_row],
                           curses.A_NORMAL )

    def highlight_current_row(self):
        if len(self.lines) > 0:
            self.screen.addstr(self.selected_row, 0,
                               self.lines[self.selected_row],
                               curses.A_REVERSE )
        
    def next_row(self):
        if self.selected_row + 1 < self.entry_count:
            self.unhighlight_current_row()
            self.selected_row += 1
            self.highlight_current_row()

    def prev_row(self):
        if self.selected_row > 0:
            self.unhighlight_current_row()
            self.selected_row = 0
            self.highlight_current_row()

    def select(self):
        if self.selected_row < self.folder_count:
            child = self.active_folder.children[self.selected_row]
            self.set_active_folder( child )
            self.display_active_folder()
            return

        if self.selected_row < self.entry_count:
            idx = self.selected_row - self.folder_count
            entity = self.active_folder.files[idx]
            if entity.is_video():
                self.handlers['video'].play( entity.lookup_url() )
            if entity.is_audio():
                self.handlers['audio'].play( entity.lookup_url() )
                
    def backtrack(self):
        if self.active_folder.parent is not None:
            self.set_active_folder( self.active_folder.parent )
            self.display_active_folder()
        
def curses_main( stdscr, handlers ):
    state = ncurses_state(stdscr, handlers)
    while True:
        state.screen.refresh()
        c = stdscr.getch()
        if c == curses.KEY_RIGHT:
            state.select()
        if c == curses.KEY_LEFT:
            state.backtrack()
        if c == curses.KEY_UP:
            state.prev_row()
        if c == curses.KEY_DOWN:
            state.next_row()
        if c == ord('q'):
            break

def launch( handlers ):
    curses.wrapper( curses_main, handlers )
