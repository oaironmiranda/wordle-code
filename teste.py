import pygame
import random
import urllib.request
import time

# Initialize Pygame
pygame.init()

# Set screen size
size = (640, 480)
screen = pygame.display.set_mode(size)

# Set colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Set font
font = pygame.font.Font(None, 36)

# Get words from website
url = "https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt"
response = urllib.request.urlopen(url)
long_txt = response.read().decode()
words = long_txt.splitlines()

def reset_game():
    # Choose a random 5-letter word
    word = random.choice([w for w in words if len(w) == 5])

    # Set initial values
    guesses = []
    attempts = 6
    previous_attempts = []
    game_over = False

    return word, guesses, attempts, previous_attempts, game_over

word, guesses, attempts, previous_attempts, game_over = reset_game()

# Game loop
done = False
while not done:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Check guess
                guess_str = "".join(guesses)
                if guess_str == word:
                    print("You win!")
                    game_over = True
                else:
                    attempts -= 1
                    if attempts == 0:
                        print("You lose! The word was:", word)
                        game_over = True
                    else:
                        previous_attempts.append(guesses[:])
                        guesses.clear()
            elif event.unicode.isalpha():
                guesses.append(event.unicode)
            elif event.key == pygame.K_BACKSPACE:
                if len(guesses) > 0:
                    guesses.pop()

    # Clear screen
    screen.fill(WHITE)

    if not game_over:
        # Draw word and guesses at the bottom of the screen.
        y_offset = size[1] - font.get_height() - 10

        for i in range(5):
            x = size[0] // 2 + (i - 2) * 40

            # Draw character background
            if len(guesses) > i:
                guess_c = guesses[i]
                if guess_c == word[i]:
                    color = GREEN
                elif guess_c in word:
                    color = YELLOW
                else:
                    color = RED

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    pygame.draw.rect(screen, color, (x - 18, y_offset - 18, 36, 36))

            # Draw character
            text_color = WHITE if len(guesses) > i and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN else (0,0,0)
            text = font.render(guesses[i].upper() if len(guesses) > i else "", True, text_color)
            screen.blit(text, (x - text.get_width() // 2, y_offset - text.get_height() // 2))

        # Display attempts left on the top-left of the screen.
        text_attempts_left = font.render(f'Attempts left: {attempts}', True, (0,0,0))
        screen.blit(text_attempts_left,(10,10))

        # Display previous word attempts with their feedback at the center of the screen.
        y_offset = size[1] // 2 - len(previous_attempts) * (font.get_linesize() + font.get_height()) // 2

        for attempt in previous_attempts:
            for i in range(5):
                x = size[0] // 2 + (i - 2) * 40

                # Draw character background
                if len(attempt) > i:
                    guess_c = attempt[i]
                    if guess_c == word[i]:
                        color = GREEN
                    elif guess_c in word:
                        color = YELLOW
                    else:
                        color = RED

                    pygame.draw.rect(screen, color, (x - 18, y_offset - 18, 36, 36))

                # Draw character
                text_previous_attempts = font.render(attempt[i].upper() if len(attempt) > i else "", True,
                                                    WHITE if len(attempt) > i else (0, 0, 0))
                screen.blit(text_previous_attempts,
                            (x - text_previous_attempts.get_width() // 2,
                             y_offset - text_previous_attempts.get_height() // 2))

            y_offset += font.get_linesize() + font.get_height()

    # Show the correct word on the screen when the game is over.
    if game_over:
        text_game_over = font.render(f'The word was: {word.upper()}', True, (0,0,0))
        screen.blit(text_game_over,(size[0]//2-text_game_over.get_width()//2, size[1]//2-text_game_over.get_height()//2))

        # Wait for 3 seconds after showing the correct word.
        pygame.display.flip()
        time.sleep(3)

        # Ask the player if they want to play again or close the game.
        text_play_again = font.render('Press Y to play again or Q to quit', True, (0,0,0))
        screen.blit(text_play_again,(size[0]//2-text_play_again.get_width()//2, size[1]//2+text_game_over.get_height()))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    word, guesses, attempts, previous_attempts, game_over = reset_game()
                elif event.key == pygame.K_q:
                    done = True

    # Update screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
