from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
import random
import math

class LogicGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Initialize game state
        self.level = 1
        self.score = 0
        self.attempts = 0
        self.max_attempts = 10
        self.target_number = random.randint(1, 100)
        self.game_over = False
        self.won = False
        
        # Create UI elements
        self.title = Label(
            text='Advanced Logic Game',
            size_hint_y=None,
            height=50,
            font_size='24sp'
        )
        
        self.info_label = Label(
            text=f'Level: {self.level} | Score: {self.score}',
            size_hint_y=None,
            height=40,
            font_size='18sp'
        )
        
        self.message_label = Label(
            text=f'Guess a number between 1 and 100!\nAttempts: {self.attempts}/{self.max_attempts}',
            size_hint_y=None,
            height=100,
            font_size='18sp',
            text_size=(Window.width - 20, None)
        )
        
        self.input_box = TextInput(
            multiline=False,
            size_hint_y=None,
            height=50,
            font_size='20sp'
        )
        
        self.submit_button = Button(
            text='Submit Guess',
            size_hint_y=None,
            height=50,
            font_size='20sp'
        )
        
        self.reset_button = Button(
            text='Reset Game',
            size_hint_y=None,
            height=50,
            font_size='20sp'
        )
        
        # Add widgets to layout
        self.add_widget(self.title)
        self.add_widget(self.info_label)
        self.add_widget(self.message_label)
        self.add_widget(self.input_box)
        self.add_widget(self.submit_button)
        self.add_widget(self.reset_button)
        
        # Bind buttons
        self.submit_button.bind(on_press=self.handle_guess)
        self.reset_button.bind(on_press=self.reset_game)
        
        # Generate hints
        self.hints = self.generate_hints()
        self.current_hint = 0

    def generate_hints(self):
        hints = []
        
        # Basic hints
        hints.append("The number is " + ("even" if self.target_number % 2 == 0 else "odd"))
        hints.append("The number is " + ("greater" if self.target_number > 50 else "less") + " than 50")
        
        # Level 2 hints
        if self.level >= 2:
            hints.append("The number is " + ("prime" if self.is_prime(self.target_number) else "composite"))
            hints.append("The number is " + ("divisible by 3" if self.target_number % 3 == 0 else "not divisible by 3"))
        
        # Level 3 hints
        if self.level >= 3:
            hints.append("The number is " + ("a perfect square" if self.is_perfect_square(self.target_number) else "not a perfect square"))
            hints.append("The number is " + ("divisible by 4" if self.target_number % 4 == 0 else "not divisible by 4"))
        
        # Level 4 hints
        if self.level >= 4:
            hints.append("The number is " + ("divisible by 5" if self.target_number % 5 == 0 else "not divisible by 5"))
            hints.append("The number is " + ("divisible by 6" if self.target_number % 6 == 0 else "not divisible by 6"))
        
        return hints

    def is_prime(self, n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    def is_perfect_square(self, n):
        return int(math.sqrt(n)) ** 2 == n

    def handle_guess(self, instance):
        try:
            guess = int(self.input_box.text)
            self.attempts += 1
            
            if guess == self.target_number:
                self.score += (self.max_attempts - self.attempts + 1) * 10
                self.message_label.text = f'Congratulations! You won in {self.attempts} attempts!\nScore: {self.score}'
                self.game_over = True
                self.won = True
                
                # Level up after winning
                if self.won and not self.game_over:
                    self.level += 1
                    self.start_new_level()
            elif self.attempts >= self.max_attempts:
                self.message_label.text = f'Game Over! The number was {self.target_number}\nFinal Score: {self.score}'
                self.game_over = True
            else:
                if guess < self.target_number:
                    self.message_label.text = 'Too low! Try again!'
                else:
                    self.message_label.text = 'Too high! Try again!'
                
                if self.attempts % 3 == 0 and self.current_hint < len(self.hints):
                    self.message_label.text += f'\nHint: {self.hints[self.current_hint]}'
                    self.current_hint += 1
            
            self.input_box.text = ''
            self.info_label.text = f'Level: {self.level} | Score: {self.score}'
            self.message_label.text += f'\nAttempts: {self.attempts}/{self.max_attempts}'
            
        except ValueError:
            self.message_label.text = 'Please enter a valid number!'

    def start_new_level(self):
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        self.max_attempts = 10 - (self.level - 1)
        self.game_over = False
        self.won = False
        self.input_box.text = ''
        self.current_hint = 0
        
        # Generate new hints
        self.hints = self.generate_hints()
        
        # Update UI
        self.message_label.text = f'Level {self.level}: Guess a number between 1 and 100!\nAttempts: {self.attempts}/{self.max_attempts}'
        self.info_label.text = f'Level: {self.level} | Score: {self.score}'

    def reset_game(self, instance):
        self.level = 1
        self.score = 0
        self.start_new_level()

class LogicGameApp(App):
    def build(self):
        return LogicGame()

if __name__ == '__main__':
    LogicGameApp().run() 