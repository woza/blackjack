import curses
from browser import folder


# The ncurses_state class is used to keep track of what is being displayed, in
# order to display a highlight bar as the appropriate place.  Since we're
# already tracking this, we'll leverage it to handle scrolling as well.
#
# The class works as follows: when navigation by the user enters a new folder,
# that folder's contents are fetched from the server - this is done within
# set_active_folder().  We build a list of the contents and save it in
# self.lines.  We save two pointers to various reference points within this
# array:
#
#  self.selected_row is the row which should be highlighted and which will be
#  invoked if the user presses the right arrow.
#
#  self.first_line is the first line which is going to be displayed.
#
#  The function display_active_folder() will draw the lines from
#  [self.first_line:screen_height] onto the screen.

class ncurses_state:
    def __init__( self, screen, config ):
        self.screen = screen
        self.config = config
        self.folder_count = 0
        self.file_count = 0
        self.entry_count = 0
        self.selected_row = -1
        self.lines = []
        self.set_active_folder( folder("/", config) )
        self.display_active_folder()
        self.highlight_current_row()
        
    def set_active_folder( self, f ):
        self.active_folder = f
        self.active_folder.fetch_contents()
        self.lines = []
        row = 0
        for name in self.active_folder.subfolders():
            self.lines += [ name + "/" ]
            row += 1
        self.folder_count = row
        for name in self.active_folder.file_names():
            self.lines += [name]
            row += 1
        self.entry_count = row
        self.selected_row = 0
        self.first_line = 0
#        self.screen.update_lines_cols()
        height,_ = self.screen.getmaxyx()
 
    def set_folder_count( self, f ):
        self.folder_count = f

    def set_entry_count(self, c):
        self.entry_count = c
        self.num_files = self.entry_count - self.folder_count

    def display_active_folder(self):
        self.screen.erase()
        row = 0
        height,_ = self.screen.getmaxyx()
        num_to_draw = len(self.lines) - self.first_line
        if num_to_draw > height:
            num_to_draw = height
        for i in range(num_to_draw):
            self.screen.addstr(row, 0, self.lines[self.first_line + i])
            row += 1

    def redraw_current_row(self, mode):
        if len(self.lines) > 0:
            # Calculate mapping from index into lines array to screen row.
            screen_row = self.selected_row - self.first_line
            self.screen.addstr(screen_row, 0,
                               self.lines[self.selected_row], mode )
            
    def unhighlight_current_row(self):
        self.redraw_current_row(curses.A_NORMAL)

    def highlight_current_row(self):
        self.redraw_current_row(curses.A_REVERSE)

    def scroll_down_if_required(self):
        # self.selected_row has just increased.  If we have moved beyond the
        # region displayable in a single screen, then refresh the contents of
        # the screen from the backing array to reflect this.
        height,_ = self.screen.getmaxyx()
        if self.selected_row >= height:
            self.first_line += 1
            self.display_active_folder()
            
    def scroll_up_if_required(self):
        height,_ = self.screen.getmaxyx()

        # If the user has pressed up, the newly selected row is before those
        #items displayed on the screen, then scroll up.
        if self.selected_row < self.first_line:
            self.first_line -= 1
            self.display_active_folder()
            
    def next_row(self):
        if self.selected_row + 1 < self.entry_count:
            self.unhighlight_current_row()
            self.selected_row += 1
            self.scroll_down_if_required()
            self.highlight_current_row()

    def prev_row(self):
        if self.selected_row > 0:
            self.unhighlight_current_row()
            self.selected_row -= 1
            self.scroll_up_if_required()
            self.highlight_current_row()

    def select(self):
        if self.selected_row < self.folder_count:
            child = self.active_folder.children[self.selected_row]
            self.set_active_folder( child )
            self.display_active_folder()
            self.highlight_current_row()
            return

        if self.selected_row < self.entry_count:
            idx = self.selected_row - self.folder_count
            entity = self.active_folder.files[idx]
            if entity.is_video():
                self.config.handlers['video'].play( entity.lookup_url() )
            if entity.is_audio():
                self.config.handlers['audio'].play( entity.lookup_url() )
                
    def backtrack(self):
        if self.active_folder.parent is not None:
            self.set_active_folder( self.active_folder.parent )
            self.display_active_folder()
            self.highlight_current_row()
        
def curses_main( stdscr, config ):
    state = ncurses_state(stdscr, config)
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

def launch( config ):
    curses.wrapper( curses_main, config )
