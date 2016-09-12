
import sys
from dia_route_ctr import RouteCtr


import readline
import rlcompleter
if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")
    

COMMANDS = ['quit', 'transport', 'route', 'identity', 'up', 
            "--local ", "--remote ", "--dest ", "--peer ", "--record ", 
            "add ", "list", "modify ", "rm "]

def complete(text, state):
    for cmd in COMMANDS:
        if cmd.startswith(text):
            if not state:
                return cmd
            else:
                state -= 1

readline.parse_and_bind("tab: complete")
readline.set_completer(complete)


class CLI(object):
    def __init__(self):
        self.pwd_ = ["Diameter"]
        
    def pwd(self):
        return "-".join(self.pwd_)+"> "
    
    
    def sub_cli(self, CTR):
        ctr = CTR()
        while True:
            cmd = raw_input(self.pwd())
            
            if cmd == "up":
                self.pwd_= self.pwd_[:-1]
                break
            elif cmd == "quit":
                sys.exit(0)
            else:
                text = "--cmd " + cmd
                
                ctr.execute(text.split())

    def run(self):
        while True:
            cmd = raw_input(self.pwd())
            
            if cmd == "quit":
                break
            elif cmd == "route":
                self.pwd_.append(cmd)
                self.sub_cli(RouteCtr)

if __name__ == "__main__":
    cli = CLI()
    cli.run()
    