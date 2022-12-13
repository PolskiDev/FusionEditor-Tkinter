def Dictionary(self):
    # Create token-color relation - see more at: "sublime.py": line 33
    self.tags = [
    "orange",   
    "#0cc",
    "#e69b00",
    "#449e48",
    "#ff00ff"
    ]

    # Create color relation to show on the screen - Set all tokens here
    self.wordlist = [   ['function','Scanner','print','println'], # Orange

                        ["@com",'int','float','String','bool','none','void',
                        'Int','Float','Bool','expression'], # Cyan
                        
                        ['@import','package'], # Gold
                        
                        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"], #Green
                        
                        ['if','elseif','else','do','end','while','for','times',
                        'call','return','and','or','is','not','isnot','in',
                        'namespace','args','endnamespace']  # Magenta
                    ]   
 
