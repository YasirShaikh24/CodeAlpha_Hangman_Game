import random
import tkinter as tk
from tkinter import messagebox, font as tkfont

# Expanded word list
WORD_LIST = [
    # Animals
    'cat', 'dog', 'bird', 'fish', 'horse', 'cow', 'pig', 'sheep', 'codealpha',
    # Fruits and Vegetables
    'apple', 'banana', 'orange', 'grape', 'carrot', 'potato', 'tomato', 
    # Colors
    'red', 'blue', 'green', 'yellow', 'purple', 'orange', 
    # Simple Nouns
    'book', 'house', 'chair', 'table', 'phone', 'computer', 'shoe', 
    # Family
    'mom', 'dad', 'baby', 'sister', 'brother', 
    # Basic Actions
    'run', 'walk', 'jump', 'swim', 'dance'
]

class HangmanGame:
    def __init__(self, master):
        self.master = master
        
        # Configure main window
        master.title("Hangman Game")
        master.geometry("600x800")
        master.resizable(False, False)
        master.configure(bg='#1b1f3b')  # Dark blue galaxy background

        # Color scheme
        self.colors = {
            'background': '#1b1f3b',  # Dark blue
            'text_primary': '#ffffff',  # White
            'text_secondary': '#d1d4e0',  # Light grey
            'button_bg': '#3a3f77',  # Medium blue
            'button_hover': '#5c5fb1',  # Lighter glowing blue
            'button_disabled': '#4a4a5e',  # Muted grey-blue
            'letter_bg': '#2b2f55',  # Dark button background
            'letter_active': '#5fc9e8',  # Bright aqua for correct guesses
            'letter_used': '#f05454'  # Bright red for used letters
        }

        # Custom fonts
        self.title_font = tkfont.Font(family="Helvetica", size=22, weight="bold")
        self.label_font = tkfont.Font(family="Arial", size=16)
        self.button_font = tkfont.Font(family="Arial", size=12, weight="bold")

        # Game variables
        self.word = self.choose_word()
        self.guessed_letters = set()
        self.incorrect_guesses = 0
        self.max_incorrect_guesses = 6
        self.score = 0
        self.best_score = 0

        # Hangman drawing stages
        self.hangman_stages = [
            '''
            +---+
            |   |
                |
                |
                |
                |
            =========''',
            '''
            +---+
            |   |
            O   |
                |
                |
                |
            =========''',
            '''
            +---+
            |   |
            O   |
            |   |
                |
                |
            =========''',
            '''
            +---+
            |   |
            O   |
           /|   |
                |
                |
            =========''',
            '''
            +---+
            |   |
            O   |
           /|\\  |
                |
                |
            =========''',
            '''
            +---+
            |   |
            O   |
           /|\\  |
           /    |
                |
            =========''',
            '''
            +---+
            |   |
            O   |
           /|\\  |
           / \\  |
                |
            ========='''
        ]

        # Alphabet for letter buttons
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title_label = tk.Label(
            self.master, 
            text="Hangman Game", 
            font=self.title_font, 
            bg=self.colors['background'], 
            fg=self.colors['text_primary']
        )
        self.title_label.pack(pady=20)

        # Score Display
        self.score_label = tk.Label(
            self.master, 
            text=f"Score: {self.score}", 
            font=self.label_font, 
            bg=self.colors['background'], 
            fg=self.colors['text_secondary']
        )
        self.score_label.pack(pady=5)

        # Best Score Display
        self.best_score_label = tk.Label(
            self.master, 
            text=f"Best Score: {self.best_score}", 
            font=self.label_font, 
            bg=self.colors['background'], 
            fg=self.colors['text_secondary']
        )
        self.best_score_label.pack(pady=5)

        # Hangman display
        self.hangman_display = tk.Label(
            self.master, 
            text=self.hangman_stages[0], 
            font=('Courier', 12), 
            bg=self.colors['background'], 
            fg=self.colors['text_primary']
        )
        self.hangman_display.pack(pady=15)

        # Word display
        self.word_label = tk.Label(
            self.master, 
            text=self.display_word(), 
            font=self.title_font, 
            bg=self.colors['background'], 
            fg=self.colors['text_primary']
        )
        self.word_label.pack(pady=15)

        # Guessed letters display
        self.guessed_label = tk.Label(
            self.master, 
            text="Guessed Letters: ", 
            font=self.label_font, 
            bg=self.colors['background'], 
            fg=self.colors['text_secondary']
        )
        self.guessed_label.pack(pady=5)

        # Letter buttons frame
        self.letter_frame = tk.Frame(self.master, bg=self.colors['background'])
        self.letter_frame.pack(pady=10)

        # Create letter buttons
        self.letter_buttons = {}
        for i, letter in enumerate(self.alphabet):
            btn = tk.Button(
                self.letter_frame, 
                text=letter.upper(), 
                width=3, 
                height=2, 
                font=self.button_font, 
                bg=self.colors['letter_bg'], 
                fg=self.colors['text_primary'], 
                relief=tk.RAISED,
                command=lambda l=letter: self.check_guess(l)
            )
            btn.grid(row=i // 9, column=i % 9, padx=5, pady=5)
            self.letter_buttons[letter] = btn

            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: self.on_letter_enter(b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_letter_leave(b))

    def on_letter_enter(self, button):
        """Hover effect for letter buttons"""
        if button['state'] == tk.NORMAL:
            button.configure(bg=self.colors['button_hover'])

    def on_letter_leave(self, button):
        """Restore button color after hover"""
        if button['state'] == tk.NORMAL:
            button.configure(bg=self.colors['letter_bg'])

    def choose_word(self):
        """Select a random word. use 'codealpha' for testing."""
        debug_mode = True  # Change to False for normal random selection
        return "codealpha"
        return random.choice(WORD_LIST)

    def display_word(self):
        """Display the word with guessed letters."""
        return ' '.join([letter if letter in self.guessed_letters else '_' for letter in self.word])

    def check_guess(self, guess):
        """Process player's guess."""
        self.letter_buttons[guess].configure(state=tk.DISABLED, bg=self.colors['letter_used'])
        self.guessed_letters.add(guess)
        self.guessed_label.config(text=f"Guessed Letters: {', '.join(sorted(self.guessed_letters))}")
        
        if guess in self.word:
            if set(self.word).issubset(self.guessed_letters):
                self.score += 10
                if self.score > self.best_score:
                    self.best_score = self.score
                messagebox.showinfo("Congratulations!", f"You guessed the word: {self.word}\nScore: +10")
                self.reset_game()
        else:
            self.incorrect_guesses += 1
            self.hangman_display.config(text=self.hangman_stages[self.incorrect_guesses])
            if self.incorrect_guesses >= self.max_incorrect_guesses:
                messagebox.showerror("Game Over", f"The word was: {self.word}\nFinal Score: {self.score}")
                self.reset_game()

        self.word_label.config(text=self.display_word())
        self.score_label.config(text=f"Score: {self.score}")
        self.best_score_label.config(text=f"Best Score: {self.best_score}")

    def reset_game(self):
        """Reset game state."""
        self.word = self.choose_word()
        self.guessed_letters = set()
        self.incorrect_guesses = 0
        self.word_label.config(text=self.display_word())
        self.guessed_label.config(text="Guessed Letters: ")
        self.hangman_display.config(text=self.hangman_stages[0])
        for button in self.letter_buttons.values():
            button.configure(state=tk.NORMAL, bg=self.colors['letter_bg'])

def main():
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
