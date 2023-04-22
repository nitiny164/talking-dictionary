from tkinter import *
import json
from difflib import get_close_matches
from tkinter import messagebox
import pyttsx3

class TalkingDictionary:
    def __init__(self):
        # initialize engine for text-to-speech
        self.engine = pyttsx3.init()
        self.voice = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voice[1].id)
        self.engine.setProperty('rate', 150)

        # initialize GUI
        self.root = Tk()
        self.root.geometry('1000x650')
        self.root.title('Talking Dictionary - Nitin')
        self.root.resizable(0, 0)

        # set background image
        self.bgimage = PhotoImage(file='p1.png')
        self.bglabel = Label(self.root, image=self.bgimage)
        self.bglabel.pack(expand=True, fill="both")

        # create widgets
        self.enterwordlabel = Label(self.root, text='ENTER WORD', font=('arial', 29, 'bold'), fg='#4E10C8', bg='white')
        self.enterwordlabel.place(x=575, y=40)

        self.enterwordentry = Entry(self.root, font=('arial', 20,), bd=8, relief=GROOVE, justify=CENTER, width=21)
        self.enterwordentry.place(x=550, y=95)

        self.searching = PhotoImage(file='search.png')
        self.searchingbutton = Button(self.root, image=self.searching, bg='white', bd=0, cursor="hand2",
                                      activebackground='white', command=self.search)
        self.searchingbutton.place(x=645, y=150)

        self.mic = PhotoImage(file='p2.png')
        self.micbutton = Button(self.root, image=self.mic, bg='white', bd=0, cursor="hand2", activebackground='white',
                                 command=self.enterwordaudio)
        self.micbutton.place(x=710, y=150)

        self.meaninglabel = Label(self.root, text='MEANING', font=('arial', 29, 'bold'), fg='#4E10C8', bg='white')
        self.meaninglabel.place(x=610, y=220)

        self.textarea = Text(self.root, width=29, height=12, font=('arial', 14), bd=8, relief=GROOVE, wrap='word')
        self.textarea.place(x=550, y=270)

        self.audioimage = PhotoImage(file='p2.png')
        self.audiobutton = Button(self.root, image=self.audioimage, bg='white', bd=0, cursor="hand2",
                                  activebackground='white', command=self.meaningaudio)
        self.audiobutton.place(x=625, y=560)

        self.clearimg = PhotoImage(file='close.png')
        self.clearimgbutton = Button(self.root, image=self.clearimg, bg='white', bd=0, cursor="hand2",
                                      activebackground='white', command=self.clear_func)
        self.clearimgbutton.place(x=677, y=560)

        self.exitimg = PhotoImage(file='exit.png')
        self.exitimgbutton = Button(self.root, image=self.exitimg, bg='white', bd=0, cursor="hand2",
                                    activebackground='white', command=self.exit_func)
        self.exitimgbutton.place(x=732, y=560)

        self.root.bind('<Return>', self.enter_func)

    def search(self):
        dict_words = json.load(open('data.json'))
        word = self.enterwordentry.get().lower()
        if word in dict_words:
            meaning = dict_words[word]
            self.textarea.delete(1.0,END)
            for item in meaning:
                self.textarea.insert(END,u'\u2022'f' {item}\n\n')
        elif len(get_close_matches(word,dict_words.keys()))>0:
            close_match = get_close_matches(word,dict_words.keys())[0]
            result = messagebox.askyesno('Confirm',f'Did you mean "{close_match}" instead?')
            if result == True:
                self.enterwordentry.delete(0,END)
                self.enterwordentry.insert(END,close_match)
                meaning=dict_words[close_match]
                self.textarea.delete(1.0,END)
                for item in meaning:
                    self.textarea.insert(END,u'\u2022'+f' {item}\n\n')
            else:
                messagebox.showerror('Error',"The word doesn't exist,please doublecheck the word")
                self.enterwordentry.delete(0,END)
                self.textarea.delete(1.0,END)
        else:
            messagebox.showinfo('Information',"The word doesn't exist")
            self.enterwordentry.delete(0,END)
            self.textarea.delete(1.0,END)

    def enter_func(self,event):
        self.searchingbutton.invoke()

    def clear_func(self,):
        self.enterwordentry.delete(0,END)
        self.textarea.delete(1.0,END)
        
    def exit_func(self):
        exit = messagebox.askyesno('Confirm','Do you want to exit?')
        if exit == True:
            self.root.destroy()

    def enterwordaudio(self):
        self.engine.say(self.enterwordentry.get())
        self.engine.runAndWait()

    def meaningaudio(self):
        self.engine.say(self.textarea.get(1.0,END))
        self.engine.runAndWait()
    
    def run(self):
        self.root.mainloop()
    
if __name__== "__main__":
    dictionary = TalkingDictionary()
    dictionary.run()