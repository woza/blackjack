
debug_log_path='/tmp/blackjack.debug'

def init():
    with open(debug_log_path, 'w') as unused:
        pass

def debug(msg):
    with open(debug_log_path, 'a') as dest:
        dest.write(msg + "\n")
        
        
