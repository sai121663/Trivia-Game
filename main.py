# This file will include GUI & handle the display of the Trivia game.

import pygame
import sys
import random
import textwrap
from TriviaApp import fetch_question

# Initializing the game & setting up the display
pygame.init()
WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Fonts & Colours
small_font = pygame.font.SysFont("comic sans", 24)
big_font = pygame.font.SysFont("comic sans", 32)
bold_font = pygame.font.SysFont("impact", 32)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
GREEN = (34, 139, 34)
RED = (200, 50, 50)
BLUE = (30, 144, 255)
YELLOW = (255, 215, 0)
BLACK = (0, 0, 0)

# Variables for game loop
# (choosing the difficulty as "medium" & category as "sports" for beginner purposes)
player_points = 0
difficulty = "medium"
valid_letters = ["A", "B", "C", "D"]
message = ""

# Fetch first question
category = random.choice(["sports", "celebrities", "art", "animals", "history"])
question = fetch_question(difficulty, category)
choices = question.options
random.shuffle(choices)
correct_answer = question.correct_ans

# Load CORRECT & WRONG image into pygame
correct_img = pygame.image.load("that's correct.gif")
wrong_img = pygame.image.load("that's wrong.gif")


def quit_game() -> None:
    """Quits the game."""

    # Print the final amount of points
    screen.fill(BLACK)
    closing_text = big_font.render(f"You ended with {player_points}!", True, YELLOW)
    screen.blit(closing_text, (30, 20))

    # Update the display and wait for a few seconds
    pygame.display.update()
    pygame.time.wait(2000)

    # Exit the game
    pygame.quit()
    sys.exit()


# UNFINISHED Game Loop
running = True
while running:

    screen.fill(BLACK)

    # Display SCORE
    score_text = big_font.render(f"Score: {player_points}", True, YELLOW)
    screen.blit(score_text, (30, 20))  # Parameters: (screen, position)

    # Display QUESTION
    # Breaking the question into chunks of 50 characters, while preserving whole words
    question_text = textwrap.wrap(f"{category.upper()} - {question.question}", width=50)
    for i, line in enumerate(question_text):
        line_surface = big_font.render(line, True, WHITE)
        screen.blit(line_surface, (30, 90 + i * 50))   # Stacking the lines 50 pixels apart vertically

    # Display ANSWER OPTIONS
    start_y = 150 + len(question_text) * 30
    for i, option in enumerate(choices):
        label = f"{valid_letters[i]}. {option}"
        options_text = small_font.render(label, True, BLUE)
        pygame.draw.rect(screen, RED, (50, start_y + i * 70, 800, 50), 2)  # Draw rectangle around each option
        screen.blit(options_text, (60, start_y + i * 70 + 10))

    pygame.display.update()

    # Implement mouse events (allow user to CLICK on buttons)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If the user clicks on an option
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_x, click_y = pygame.mouse.get_pos()   # Track x/y position of user's mouse click

            for i in range(len(choices)):
                button_y = start_y + i * 70     # Represents the top of the current option box

                # Check whether the user clicked on the CURRENT option box
                if 50 < click_x < 850 and button_y < click_y < button_y + 50:
                    user_answer = choices[i]

                    # Check user's answer
                    is_correct, message, player_points = question.check_answer(player_points, user_answer)

                    screen.fill(BLACK)

                    # Display result message
                    message_text = textwrap.wrap(message, width=50)
                    for k, line in enumerate(message_text):

                        # Message is printed in GREEN if the user's answer is CORRECT, and vice versa.
                        if is_correct:
                            message_line = big_font.render(line, True, GREEN)
                        else:
                            message_line = big_font.render(line, True, RED)

                        screen.blit(message_line, (30, 30 + k * 50))

                    # Displaying an image telling the user whether they were CORRECT/WRONG
                    if is_correct:
                        screen.blit(correct_img, (250, 120))
                    else:
                        screen.blit(wrong_img, (250, 120))

                    # Giving the user an option to QUIT the game
                    # Parameters: surface, colour, (x, y, width, height)
                    pygame.draw.rect(screen, GREY, (725, 425, 150, 50))

                    quit_button = pygame.Rect(100, 100, 200, 50)
                    quit_label = bold_font.render("QUIT", True, RED)
                    screen.blit(quit_label, (765, 425))

                    pygame.display.update()
                    pygame.time.wait(2000)

                    # Make this only run when the user clicks on "QUIT" button
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        quit_game()

                    # Fetch next question
                    category = random.choice(["sports", "celebrities", "art", "animals", "history"])
                    question = fetch_question(difficulty, category)
                    choices = question.options
                    random.shuffle(choices)
                    correct_answer = question.correct_ans


# Quit Pygame
pygame.quit()
sys.exit()

# ----------------

# Instructions:
# - Enable user to click on "QUIT" button that closes the game:
#   https://chatgpt.com/c/68704ab0-bf14-800e-a104-27d77138a468

# - Split code into helper functions (e.g. get_new_question, draw_question, draw_options)
