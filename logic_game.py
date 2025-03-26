import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FONT_SIZE = 32
BUTTON_HEIGHT = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Advanced Logic Game")
font = pygame.font.Font(None, FONT_SIZE)

class LogicGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.level = 1
        self.score = 0
        self.start_new_level()

    def start_new_level(self):
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        self.max_attempts = 10 - (self.level - 1)  # Fewer attempts in higher levels
        self.message = f"Level {self.level}: Guess a number between 1 and 100!"
        self.game_over = False
        self.won = False
        self.input_text = ""
        self.current_hint = 0
        
        # Generate level-specific hints
        self.hints = self.generate_hints()
        
        # Add level-specific challenges
        if self.level >= 2:
            self.prime_factors = self.get_prime_factors(self.target_number)
            self.message += f"\nThe number has {len(self.prime_factors)} prime factors"
        
        if self.level >= 3:
            self.digits_sum = sum(int(d) for d in str(self.target_number))
            self.message += f"\nSum of digits is {self.digits_sum}"
        
        if self.level >= 4:
            self.binary = bin(self.target_number)[2:]
            self.message += f"\nBinary representation has {len(self.binary)} digits"

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

    def get_prime_factors(self, n):
        factors = []
        i = 2
        while i * i <= n:
            while n % i == 0:
                factors.append(i)
                n //= i
            i += 1
        if n > 1:
            factors.append(n)
        return factors

    def handle_guess(self):
        try:
            guess = int(self.input_text)
            self.attempts += 1
            
            if guess == self.target_number:
                self.score += (self.max_attempts - self.attempts + 1) * 10
                self.message = f"Congratulations! You won in {self.attempts} attempts!\nScore: {self.score}"
                self.game_over = True
                self.won = True
                
                # Level up after winning
                if self.won and not self.game_over:
                    self.level += 1
                    self.start_new_level()
            elif self.attempts >= self.max_attempts:
                self.message = f"Game Over! The number was {self.target_number}\nFinal Score: {self.score}"
                self.game_over = True
            else:
                if guess < self.target_number:
                    self.message = "Too low! Try again!"
                else:
                    self.message = "Too high! Try again!"
                
                if self.attempts % 3 == 0 and self.current_hint < len(self.hints):
                    self.message += f"\nHint: {self.hints[self.current_hint]}"
                    self.current_hint += 1
            
            self.input_text = ""
        except ValueError:
            self.message = "Please enter a valid number!"

    def draw(self):
        screen.fill(WHITE)
        
        # Draw title
        title = font.render("Advanced Logic Game", True, BLACK)
        screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 50))
        
        # Draw level and score
        level_text = font.render(f"Level: {self.level}", True, PURPLE)
        score_text = font.render(f"Score: {self.score}", True, PURPLE)
        screen.blit(level_text, (10, 10))
        screen.blit(score_text, (10, 50))
        
        # Draw message
        message_lines = self.message.split('\n')
        for i, line in enumerate(message_lines):
            message_text = font.render(line, True, BLACK)
            screen.blit(message_text, (WINDOW_WIDTH//2 - message_text.get_width()//2, 150 + i*40))
        
        # Draw input box
        input_box = pygame.Rect(WINDOW_WIDTH//2 - 100, 300, 200, BUTTON_HEIGHT)
        pygame.draw.rect(screen, BLACK, input_box, 2)
        
        input_surface = font.render(self.input_text, True, BLACK)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))
        
        # Draw attempts counter
        attempts_text = font.render(f"Attempts: {self.attempts}/{self.max_attempts}", True, BLACK)
        screen.blit(attempts_text, (WINDOW_WIDTH - 200, 10))
        
        # Draw reset button
        reset_button = pygame.Rect(WINDOW_WIDTH - 150, 50, 140, BUTTON_HEIGHT)
        pygame.draw.rect(screen, BLUE, reset_button)
        reset_text = font.render("Reset Game", True, WHITE)
        screen.blit(reset_text, (reset_button.x + 10, reset_button.y + 10))
        
        pygame.display.flip()

def main():
    game = LogicGame()
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if reset button is clicked
                if WINDOW_WIDTH - 150 <= event.pos[0] <= WINDOW_WIDTH - 10 and 50 <= event.pos[1] <= 100:
                    game.reset_game()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not game.game_over:
                    game.handle_guess()
                elif event.key == pygame.K_BACKSPACE:
                    game.input_text = game.input_text[:-1]
                else:
                    if event.unicode.isnumeric() and not game.game_over:
                        game.input_text += event.unicode
        
        game.draw()
        clock.tick(60)

if __name__ == "__main__":
    main() 