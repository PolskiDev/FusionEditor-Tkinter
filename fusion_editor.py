#!/usr/bin/env python3
from tkinter import *
from collections import deque
import dictionary
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
from tkinter.messagebox import *
import sys
import os


IDE_NAME = "Fusion Editor - Beta 1.0"
CodeEditorFont = "\"Courier New\" 16"
DefaultIDEFont = "\"Arial\" 12"
BoldIDEFont = "\"Arial\" 12 bold"

global CodeEditorText
CodeEditorText = ''

class Window:
    def __init__(self, master): 
        self.master = master
        self.master.option_add("*Font", CodeEditorFont)
 
        self.Main = Frame(self.master)
 
        self.stack = deque(maxlen = 10)
        self.stackcursor = 0
 
        #self.L1 = Label(self.Main, text = IDE_NAME, font = BoldIDEFont)
        #self.L1.pack(padx = 5, pady = 5)
 
 
        #---------
 
        self.T1 = Text(self.Main, width = 200, height = 45)
        CodeEditorText = self.T1

        # Create token-color relation - see more at: "dictionary.py": line 3
        self.T1.tag_configure("orange", foreground = "orange", font = CodeEditorFont)
        self.T1.tag_configure("#0cc", foreground = "#0cc", font = CodeEditorFont)
        self.T1.tag_configure("#e69b00", foreground = "#e69b00", font = CodeEditorFont)
        self.T1.tag_configure("#449e48", foreground = "#449e48", font = CodeEditorFont)
        self.T1.tag_configure("#ff00ff", foreground = "#ff00ff", font = CodeEditorFont)
        self.T1.configure(background = '#222')          # Default background color (gray)
        self.T1.configure(foreground = "#fff")          # Default character color (white)
        self.T1.configure(insertbackground='white')     # White mouse cursor


        dictionary.Dictionary(self)

        self.T1.bind("<Return>", lambda event: self.indent(event.widget))
         
        self.T1.pack(padx = 5, pady = 5)
 
        #---------
 
        self.menu = Menu(self.Main)
        self.menu.add_command(label = "Open", command = self.open_file, font=DefaultIDEFont)
        self.menu.add_command(label = "Save As", command = self.save_file, font=DefaultIDEFont)
        self.menu.add_command(label = "Save Now", command = self.autosave_file, font=DefaultIDEFont)
        self.menu.add_command(label = "Undo", command = self.undo, font=DefaultIDEFont)
        self.menu.add_command(label = "Redo", command = self.redo, font=DefaultIDEFont)
        self.menu.add_command(label = "Build", command = self.build_file, font=DefaultIDEFont)
 
        self.master.config(menu = self.menu)
 
        #self.B1 = Button(self.Main, text = "Open", width = 8, command = self.open_file)
        #self.B1.pack(padx = 5, pady = 5, side = LEFT)
 
        #self.B2 = Button(self.Main, text = "Clear", width = 8, command = self.clear)
        #self.B2.pack(padx = 5, pady = 5, side = LEFT)
 
        #self.B3 = Button(self.Main, text = "Undo", width = 8, command = self.undo)
        #self.B3.pack(padx = 5, pady = 5, side = LEFT)
 
        #self.B4 = Button(self.Main, text = "Redo", width = 8, command = self.redo)
        #self.B4.pack(padx = 5, pady = 5, side = LEFT)
 
        self.Main.pack(padx = 5, pady = 5)
 
 
    def tagHighlight(self):
        start = "1.0"
        end = "end"
         
        for mylist in self.wordlist:
            num = int(self.wordlist.index(mylist))
 
            for word in mylist:
                self.T1.mark_set("matchStart", start)
                self.T1.mark_set("matchEnd", start)
                self.T1.mark_set("SearchLimit", end)
 
                mycount = IntVar()
                 
                while True:
                    index= self.T1.search(word,"matchEnd","SearchLimit", count=mycount, regexp = False)
 
                    if index == "": break
                    if mycount.get() == 0: break
 
                    self.T1.mark_set("matchStart", index)
                    self.T1.mark_set("matchEnd", "%s+%sc" % (index, mycount.get()))
 
                    preIndex = "%s-%sc" % (index, 1)
                    postIndex = "%s+%sc" % (index, mycount.get())
                     
                    if self.check(index, preIndex, postIndex):
                        self.T1.tag_add(self.tags[num], "matchStart", "matchEnd")
                         
 
    def check(self, index, pre, post):
        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
                   "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
 
        if self.T1.get(pre) == self.T1.get(index):
            pre = index
        else:
            if self.T1.get(pre) in letters:
                return 0
 
        if self.T1.get(post) in letters:
            return 0
 
        return 1
 
 
    def scan(self):
        start = "1.0"
        end = "end"
        mycount = IntVar()
 
        regex_patterns = [r'".*"', r'#.*']
 
        for pattern in regex_patterns:
            self.T1.mark_set("start", start)
            self.T1.mark_set("end", end)
 
            num = int(regex_patterns.index(pattern))
 
            while True:
                index = self.T1.search(pattern, "start", "end", count=mycount, regexp = True)
 
                if index == "": break
 
                if (num == 1):
                    self.T1.tag_add(self.tags[4], index, index + " lineend")
                elif (num == 0):
                    self.T1.tag_add(self.tags[3], index, "%s+%sc" % (index, mycount.get()))
 
                self.T1.mark_set("start", "%s+%sc" % (index, mycount.get()))
 
 
    def indent(self, widget):
 
        index1 = widget.index("insert")
        index2 = "%s-%sc" % (index1, 1)
        prevIndex = widget.get(index2, index1)
 
        prevIndentLine = widget.index(index1 + "linestart")
        print("prevIndentLine ",prevIndentLine)
        prevIndent = self.getIndex(prevIndentLine)
        print("prevIndent ", prevIndent)
 
 
        if prevIndex == ":":
            widget.insert("insert", "\n" + "     ")
            widget.mark_set("insert", "insert + 1 line + 5char")
 
            while widget.compare(prevIndent, ">", prevIndentLine):
                widget.insert("insert", "     ")
                widget.mark_set("insert", "insert + 5 chars")
                prevIndentLine += "+5c"
            return "break"
         
        elif prevIndent != prevIndentLine:
            widget.insert("insert", "\n")
            widget.mark_set("insert", "insert + 1 line")
 
            while widget.compare(prevIndent, ">", prevIndentLine):
                widget.insert("insert", "     ")
                widget.mark_set("insert", "insert + 5 chars")
                prevIndentLine += "+5c"
            return "break"
 
 
    def getIndex(self, index):
        while True:
            if self.T1.get(index) == " ":
                index = "%s+%sc" % (index, 1)
            else:
                return self.T1.index(index)
            
                    
    def update(self):
        self.stackify()
        self.tagHighlight()
        self.scan()
 
    def display(self):
        print(self.T1.get("1.0", "end"))     
 

    def open_file(self):
        """Open a file for editing."""
        filepath = askopenfilename(
            filetypes=[("Fusion Language Files", "*.fusion"), ("All Files", "*.*")])
        if not filepath:
            return
        self.T1.delete(1.0, tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.read()
            self.T1.insert(tk.INSERT, text)
        #window.title(f"{DialogTitle} - {filepath}")

    global filepath
    filepath = ''
    def save_file(self):
        """Save the current file as a new file."""
        filepath = asksaveasfilename(
            defaultextension="fusion",
            filetypes=[("Fusion Language Files", "*.fusion"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = self.T1.get(1.0, tk.END)
            output_file.write(text)
        
        savePath = open('.storm.swp','w')
        savePath.write(f"{filepath}")
        savePath.close()
        #window.title(f"{DialogTitle} - {filepath}")

    def autosave_file(self):
        """Save the current file as a new file."""
        getPath = open('.storm.swp','r').readline()
        print("Save: "+getPath)
        with open(getPath, "w") as output_file:
            text = self.T1.get(1.0, tk.END)
            output_file.write(text)
            showinfo(title="Saved file", message="Source successfully saved!")
        
    # Need be fixed
    def build_file(self):
        """Save the current file as a new file."""
        projpath = askdirectory()
        print(f"make all -C \"{projpath}\"")
        showinfo(title="Built File", message=f"Project {projpath} was built!")
        



    def clear(self):
        self.T1.delete("1.0", "end")
 
    def stackify(self):
        self.stack.append(self.T1.get("1.0", "end - 1c"))
        if self.stackcursor < 9: self.stackcursor += 1
 
    def undo(self):
        if self.stackcursor != 0:
            self.clear()
            if self.stackcursor > 0: self.stackcursor -= 1
            self.T1.insert("0.0", self.stack[self.stackcursor])
 
    def redo(self):
        if len(self.stack) > self.stackcursor + 1:
            self.clear()
            if self.stackcursor < 9: self.stackcursor += 1
            self.T1.insert("0.0", self.stack[self.stackcursor])
 
    def print_stack(self):
        i = 0
        for stack in self.stack:
            print(str(i) + " " + stack)
            i += 1
 
    
root = Tk()
root.title(IDE_NAME)

window = Window(root)
root.bind("<Key>", lambda event: window.update())
root.mainloop()
