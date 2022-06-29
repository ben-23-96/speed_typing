from tkinter import DISABLED, Label, Entry, Button, messagebox
from word_handler import WordHandler
from database import HighscoreDatabase


class SpeedTypeGui():
    def __init__(self, window):
        self.window = window
        self.word_handler = WordHandler()
        self.highscore_db = HighscoreDatabase()
        self.game_active = False
        self.highscore_page_showing = False
        self.word_being_typed = ""
        self.timer_time = 60

    def load_gui(self):
        """configures the gui window and binds the keys"""
        self.window.title('Speed Type Test')
        self.window.geometry("600x300")
        self.window.configure(bg='lemon chiffon')
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            self.window.bind(letter, self.letter_key_pressed)
        self.window.bind('<space>', self.next_word)
        self.window.bind('<BackSpace>', self.do_backspace)
        self.load_game()

    def load_game(self):
        """creates all the widgets on the games opening screen"""
        self.instruction_label = Label(font=(
            'MS Sans Serif', 14), text='Start typing to start the 60 second timer and test your typing speed.', pady=15, bg='lemon chiffon', fg='dark slate gray')
        self.instruction_label.pack()
        self.words_to_type_label = Label(
            font=('MS Sans Serif', 25), bg='lemon chiffon', fg='dark slate gray')
        self.words_to_type_label.pack()
        self.word_being_typed_label = Label(
            font=('MS Sans Serif', 25), pady=15, bg='lemon chiffon')
        self.word_being_typed_label.pack()
        self.timer_label = Label(
            font=('MS Sans Serif', 25), pady=25, bg='lemon chiffon', fg='dark slate gray')
        self.timer_label.pack()
        self.show_highscores_button = Button(
            text='highscores', command=self.show_highscores)
        self.show_highscores_button.pack()
        self.word_handler.generate_word_list()
        self.display_words()

    def show_highscores(self):
        """produces a message box that contains the highscores from the database"""
        highscores = self.highscore_db.top_10_highscores()
        message = ""
        for index, highscore in enumerate(highscores):
            message = message + \
                f"{str(index+1)}. {highscore.name} :  {highscore.score}\n"
        messagebox.showinfo('Highscores', message)

    def display_words(self):
        """displays the words on the screen that are to be typed out"""
        words_to_be_displayed = self.word_handler.words_list[
            self.word_handler.current_word_index:self.word_handler.current_word_index+3]
        display = " ".join(words_to_be_displayed)
        self.words_to_type_label.config(text=display)

    def letter_key_pressed(self, event):
        """starts the game if not active. Displays the word the user is typing, changing colour from green to red depending on if correct"""
        if self.game_active == False and self.highscore_page_showing == False:
            self.start()
        if self.game_active:
            letter = event.keysym
            self.word_being_typed = self.word_being_typed + letter
            self.word_being_typed_label.config(text=self.word_being_typed)
            if self.word_handler.check_typing_word_correctly(self.word_being_typed):
                self.word_being_typed_label.config(fg='green')
            else:
                self.word_being_typed_label.config(fg='red')

    def start(self):
        """configures the game to active and starts the 60 second timer"""
        self.game_active = True
        self.timer()
        self.window.after(60000, self.timer_finished)
        self.instruction_label.config(text='')
        self.show_highscores_button.pack_forget()

    def timer(self):
        """displays the timer time on the screen"""
        if self.game_active:
            self.timer_label.config(text=str(self.timer_time))
            self.timer_time -= 1
            self.window.after(1000, self.timer)

    def timer_finished(self):
        self.reset_window()
        self.display_end_message()
        self.load_highscore_screen()

    def reset_window(self):
        """deactivates the game and removes all widgets from the game screen"""
        self.game_active = False
        self.timer_time = 60
        self.word_being_typed = ""
        for widget in self.window.winfo_children():
            widget.destroy()

    def display_end_message(self):
        """displays a messagebox with information relating to the users last game"""
        message = f"Congratulations you managed a type speed of {self.word_handler.correct_word_count} per minute."
        if self.word_handler.current_word_index > self.word_handler.correct_word_count:
            message = message + \
                f"\n\nIt would have been {self.word_handler.current_word_index} but you spelt some wrong.\n"
        for word in self.word_handler.incorrect_words_list:
            message = message + \
                f"\n{word['original word']} :  {word['typed word']}"
        messagebox.showinfo('Times up !', message)

    def load_highscore_screen(self):
        """creates the widgets for the screen where the user can enter their name to add to highscores"""
        self.highscore_page_showing = True
        self.highscore_screen_label = Label(font=(
            'MS Sans Serif', 25), text='Enter your name for Highscores.', pady=20, bg='lemon chiffon', fg='dark slate gray').pack()
        self.highscore_entry = Entry()
        self.highscore_entry.pack(pady=10)
        self.submit_highscore_button = Button(
            text='Submit', command=self.add_highscore).pack()

    def add_highscore(self):
        """add the users name and highscore to the highscores database, reloads the game screen"""
        name = self.highscore_entry.get()
        self.highscore_db.add_new_highscore(
            name=name, score=self.word_handler.correct_word_count)
        self.reset_window()
        self.load_game()
        self.highscore_page_showing = False

    def next_word(self, event=None):
        """clears the typed word froom the screen, sends the completed word to the word handler"""
        if self.game_active:
            self.word_handler.word_completed(self.word_being_typed)
            self.word_being_typed = ""
            self.word_being_typed_label.config(text="")
            self.display_words()

    def do_backspace(self, event=None):
        if self.game_active:
            if len(self.word_being_typed) > 0:
                self.word_being_typed = self.word_being_typed[:-1]
                self.word_being_typed_label.config(text=self.word_being_typed)
                if self.word_handler.check_typing_word_correctly(self.word_being_typed):
                    self.word_being_typed_label.config(fg='green')
                else:
                    self.word_being_typed_label.config(fg='red')
