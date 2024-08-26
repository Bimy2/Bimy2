import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Number Memory Test")

# Define colors
blue = (50, 130, 240)
white = (255, 255, 255)
dark_blue = (30, 80, 160)
yellow = (255, 204, 0)
black = (0, 0, 0)

# Load fonts
font = pygame.font.Font(None, 70)  # Large font for number display
small_font = pygame.font.Font(None, 48)  # Font for prompts and input

#level initialization
IQ = 100
level = 1

# Game state
user_input = ""

def verbal_memory_start_screen():
    while True:
        screen.fill(blue)

        # Display the title
        title_text = font.render("VERBAL MEMORY TEST", True, white)
        title_rect = title_text.get_rect(center=(screen_width/2, screen_height/2 - 100))
        screen.blit(title_text, title_rect)

        # Display instructions
        instructions_text = small_font.render("You will be shown words, one at a time.", True, white)
        instructions_text2 = small_font.render("If you've seen a word during the test, click SEEN.", True, white)
        instructions_text3 = small_font.render("If it's a new word, click NEW.", True, white)
        screen.blit(instructions_text, instructions_text.get_rect(center=(screen_width/2, screen_height/2)))
        screen.blit(instructions_text2, instructions_text2.get_rect(center=(screen_width/2, screen_height/2 + 40)))
        screen.blit(instructions_text3, instructions_text3.get_rect(center=(screen_width/2, screen_height/2 + 80)))

        # Display the "Start" button
        start_button_rect = pygame.Rect(screen_width/2 - 100, screen_height/2 + 150, 200, 50)
        pygame.draw.rect(screen, yellow, start_button_rect)
        start_text = small_font.render("Start", True, dark_blue)
        start_rect = start_text.get_rect(center=start_button_rect.center)
        screen.blit(start_text, start_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return  # Start the verbal memory game

        pygame.display.flip()

def load_words_from_file(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines()]

def get_random_word(word_list, used_words):
    if used_words and random.random() < 0.25:
        return random.choice(used_words)
    return random.choice(word_list)

def verbal_memory_game():
    lives = 3
    score = 0  # Initialize score counter
    seen_words = set()  # Set to store words that have been shown before
    word_list = load_words_from_file("DictionaryWordsForVerbalMemory.txt")
    used_words = []  # List to store the used words
    current_word = get_random_word(word_list, used_words)  # Start with a random word

    while lives > 0:
        screen.fill(blue)

        # Display lives counter
        lives_text = small_font.render(f"Lives: {lives}", True, white)
        screen.blit(lives_text, (screen_width - 150, 20))  # Top right corner
        
        # Display score counter
        score_text = small_font.render(f"Score: {score}", True, white)
        screen.blit(score_text, (20, 20))  # Top left corner
        
        # Display the word
        word_text = font.render(current_word, True, white)
        screen.blit(word_text, word_text.get_rect(center=(screen_width/2, screen_height/2 - 50)))

        # Display "Seen" and "New" buttons
        seen_button_rect = pygame.Rect(screen_width/2 - 200, screen_height/2 + 100, 150, 50)
        new_button_rect = pygame.Rect(screen_width/2 + 50, screen_height/2 + 100, 150, 50)
        pygame.draw.rect(screen, yellow, seen_button_rect)
        pygame.draw.rect(screen, yellow, new_button_rect)
        seen_text = small_font.render("Seen", True, dark_blue)
        new_text = small_font.render("New", True, dark_blue)
        screen.blit(seen_text, seen_text.get_rect(center=seen_button_rect.center))
        screen.blit(new_text, new_text.get_rect(center=new_button_rect.center))

        pygame.display.flip()

        word_selected = False  # Flag to track if the user has made a selection

        while not word_selected:  # Wait for the user to make a selection
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if seen_button_rect.collidepoint(event.pos):
                        if current_word in seen_words:
                            used_words.append(current_word)
                            score += 1  # Correct selection, increment score
                        else:
                            lives -= 1
                            used_words.append(current_word)
                        word_selected = True  # Word was selected
                    elif new_button_rect.collidepoint(event.pos):
                        if current_word in seen_words:
                            lives -= 1
                            used_words.append(current_word)
                        else:
                            seen_words.add(current_word)
                            used_words.append(current_word)
                            score += 1  # Correct selection, increment score
                        word_selected = True  # Word was selected

            # Check if the player lost all lives
            if lives <= 0:
                return score

        # Move to the next word after selection
        current_word = get_random_word(word_list, used_words)

        pygame.display.flip()




def main_menu():
    global level
    level = 1
    srtlevel = 7
    srtscore = 30
    while True:
        IQ = round(100 * ((srtlevel/7) * (srtscore/30)))
        screen.fill(blue)
        IQ_text = small_font.render(f'IQ: {IQ}', True, white)
        IQ_rect = IQ_text.get_rect(center=(screen_width/2, screen_height/4))
        screen.blit(IQ_text, IQ_rect)
        # Draw buttons
        number_memory_text = small_font.render('Number Memory Test', True, white)
        verbal_memory_text = small_font.render('Verbal Memory Test', True, white)
        number_memory_rect = number_memory_text.get_rect(center=(screen_width/2, screen_height/2 - 50))
        verbal_memory_rect = verbal_memory_text.get_rect(center=(screen_width/2, screen_height/2 + 50))

        pygame.draw.rect(screen, dark_blue, number_memory_rect.inflate(20, 20))
        pygame.draw.rect(screen, dark_blue, verbal_memory_rect.inflate(20, 20))
        screen.blit(number_memory_text, number_memory_rect)
        screen.blit(verbal_memory_text, verbal_memory_rect)

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if number_memory_rect.collidepoint(event.pos):
                    number_memory_start_screen()  # Show start screen for number memory game
                    number_memory_game()  # Start the number memory game
                elif verbal_memory_rect.collidepoint(event.pos):
                    verbal_memory_start_screen()  # Show start screen for verbal memory game
                    srtscore = verbal_memory_game()  # Start the verbal memory game
        
        pygame.display.flip()

def number_memory_start_screen():
    while True:
        screen.fill(blue)

        # Display the title
        title_text = font.render("NUMBER MEMORY TEST", True, white)
        title_rect = title_text.get_rect(center=(screen_width/2, screen_height/2 - 100))
        screen.blit(title_text, title_rect)

        # Display instructions
        instructions_text1 = small_font.render("The average person can remember 7 numbers.", True, white)
        instructions_text2 = small_font.render("Can you do more?", True, white)
        screen.blit(instructions_text1, instructions_text1.get_rect(center=(screen_width/2, screen_height/2)))
        screen.blit(instructions_text2, instructions_text2.get_rect(center=(screen_width/2, screen_height/2 + 40)))

        # Display the "Start" button
        start_button_rect = pygame.Rect(screen_width/2 - 100, screen_height/2 + 150, 200, 50)
        pygame.draw.rect(screen, yellow, start_button_rect)
        start_text = small_font.render("Start", True, dark_blue)
        start_rect = start_text.get_rect(center=start_button_rect.center)
        screen.blit(start_text, start_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return  # Start the number memory game

        pygame.display.flip()


def number_memory_game():
    global level, user_input

    while True:
        number = generate_number(level)
        user_input = ""
        show_number_screen(number)

        # After showing the number, render the level in the top right
        screen.fill(blue)
        
        # Display the current level
        level_text = small_font.render(f"Level: {level}", True, white)
        screen.blit(level_text, (screen_width - 150, 20))  # Top right corner

        if not get_user_input(number):
            return level
        else:
            level += 1


def get_user_input(correct_number):
    global user_input
    input_active = True

    while input_active:
        screen.fill(blue)

        level_text = small_font.render(f"Level: {level}", True, white)
        screen.blit(level_text, (screen_width - 150, 20))  # Top right corner

        # Prompt text at the top
        prompt_text = small_font.render("What was the number?", True, white)
        prompt_rect = prompt_text.get_rect(center=(screen_width/2, screen_height/2 - 100))
        screen.blit(prompt_text, prompt_rect)

        # Instructions for submission
        instruction_text = small_font.render("Press enter to submit", True, white)
        instruction_rect = instruction_text.get_rect(center=(screen_width/2, screen_height/2 - 50))
        screen.blit(instruction_text, instruction_rect)

        # Textbox-like area for user input
        pygame.draw.rect(screen, dark_blue, (screen_width/2 - 200, screen_height/2, 400, 80))
        input_text = small_font.render(user_input, True, white)
        screen.blit(input_text, (screen_width/2 - 190, screen_height/2 + 15))

        # Submit button
        submit_button_rect = pygame.Rect(screen_width/2 - 100, screen_height/2 + 150, 200, 50)
        pygame.draw.rect(screen, yellow, submit_button_rect)
        submit_text = small_font.render("Submit", True, dark_blue)
        submit_rect = submit_text.get_rect(center=submit_button_rect.center)
        screen.blit(submit_text, submit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input == correct_number:
                        return True  # Correct number entered
                    else:
                        return False  # Incorrect number entered
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    if len(user_input) < len(correct_number) and event.unicode.isdigit():
                        user_input += event.unicode

        pygame.display.flip()


def generate_number(length):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def show_number_screen(number):
    running = True
    while running:
        screen.fill(blue)

        level_text = small_font.render(f"Level: {level}", True, white)
        screen.blit(level_text, (screen_width - 150, 20))  # Top right corner
        
        # Display the number in the center of the screen
        number_text = font.render(number, True, white)
        screen.blit(number_text, number_text.get_rect(center=(screen_width/2, screen_height/2 - 50)))
        
        # Create a "Confirm" button
        confirm_button_rect = pygame.Rect(screen_width/2 - 100, screen_height/2 + 100, 200, 50)
        pygame.draw.rect(screen, yellow, confirm_button_rect)
        confirm_text = small_font.render("Confirm", True, dark_blue)
        screen.blit(confirm_text, confirm_text.get_rect(center=confirm_button_rect.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if confirm_button_rect.collidepoint(event.pos):
                    running = False  # Proceed to the input screen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False

        pygame.display.flip()

def return_to_menu():
    pygame.time.wait(1000)
    main_menu()

# Run the main menu
main_menu()
