# This file will include GUI & handle the display of the Trivia game.

import pygame
import sys
import random
import textwrap
from TriviaApp import fetch_question, TriviaQuestion

# Initializing the game & setting up the display
pygame.init()
screen = pygame.display.set_mode((900, 500))    # (width, height)

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
# (choosing the difficulty as "medium" for beginner purposes)
player_points = 0
difficulty = "medium"
valid_letters = ["A", "B", "C", "D"]
message = ""
showing_result = False
is_correct = False

# Load CORRECT & WRONG image into pygame
correct_img = pygame.image.load("that's correct.gif")
wrong_img = pygame.image.load("that's wrong.gif")


def quit_game() -> None:
    """Quits the game."""

    # Print the final amount of points
    screen.fill(BLACK)
    closing_text = big_font.render(f"You ended with {player_points} points!", True, YELLOW)
    screen.blit(closing_text, (30, 20))

    # Display an image
    farewell_img = pygame.image.load("sad_to_leave.jpg")
    screen.blit(farewell_img, (250, 120))

    # Update the display and wait for a few seconds
    pygame.display.update()
    pygame.time.wait(2000)

    # Exit the game
    end_program()


def end_program() -> None:
    """Ends the program."""
    pygame.quit()
    sys.exit()


def display_question(ques: TriviaQuestion, topic: str) -> None:
    """Helper function to visually print the question"""

    # Breaking the question into chunks of 50 characters, while preserving whole words
    question_text = textwrap.wrap(f"{topic.upper()} - {ques.question}", width=50)
    for i, line in enumerate(question_text):
        line_surface = big_font.render(line, True, WHITE)
        screen.blit(line_surface, (30, 90 + i * 50))  # Stacking the lines 50 pixels apart vertically


def display_options(choices_list: list[str]) -> None:
    """Helper function to visually print the MC options"""

    start_y = 240

    for i, option in enumerate(choices_list):
        label = f"{valid_letters[i]}. {option}"
        options_text = small_font.render(label, True, BLUE)
        pygame.draw.rect(screen, RED, (50, start_y + i * 70, 800, 50), 2)  # Draw rectangle around each option
        screen.blit(options_text, (60, start_y + i * 70 + 10))


def get_new_question(level: str) -> tuple:
    """Fetching a new question & returning """

    topic = random.choice(["sports", "celebrities", "art", "animals", "history"])
    ques = fetch_question(level, topic)
    choices_list = ques.options

    # Randomize the order of the options
    random.shuffle(choices_list)

    return ques, topic, choices_list


def draw_quit_button() -> None:
    """Drawing the quit button to end the game."""

    # Creating a rect. object (in theory) & initializing the position & size of the "quit" button
    # Parameters: (x, y, width, height)
    quit_button = pygame.Rect(725, 425, 150, 50)

    # DRAWING the "quit" button onto the screen
    pygame.draw.rect(screen, RED, quit_button)

    # Printing "QUIT" as text
    quit_label = bold_font.render("QUIT", True, WHITE)
    screen.blit(quit_label, (765, 425))


def draw_continue_button() -> None:
    """Allowing the user to CONTINUE the game."""

    # Creating a rectangle object for the button
    continue_button = pygame.Rect(500, 425, 175, 50)
    pygame.draw.rect(screen, GREEN, continue_button)

    # Printing "CONTINUE" as text
    continue_label = bold_font.render("CONTINUE", True, WHITE)
    screen.blit(continue_label, (525, 425))


# Fetch first question
question, category, choices = get_new_question(difficulty)

# GAME LOOP
running = True
while running:

    screen.fill(BLACK)

    # DRAWING BLOCK
    # Handles the display of the RESULT SCREEN
    if showing_result:

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
            screen.blit(correct_img, (250, 100))
        else:
            screen.blit(wrong_img, (250, 100))

        # Giving the user an option to CONTINUE or QUIT the game
        draw_continue_button()
        draw_quit_button()

        pygame.display.update()

    # Handles the display of the QUESTION SCREEN
    else:

        # Display SCORE
        score_text = big_font.render(f"Score: {player_points}", True, YELLOW)
        screen.blit(score_text, (30, 20))  # Parameters: (screen, position)

        # Display QUESTION
        display_question(question, category)

        # Display ANSWER OPTIONS
        display_options(choices)

        pygame.display.update()

    # Handles USER INPUT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If the user clicks on the mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_x, click_y = pygame.mouse.get_pos()   # Track (x,y) position of user's mouse click

            # Handles the case where the user clicks on "CONTINUE" or "QUIT"
            if showing_result:

                # Check if the user clicks on "QUIT"
                if 725 <= click_x <= 875 and 425 <= click_y <= 475:
                    quit_game()
                    showing_result = False

                # Check if the user clicks on "CONTINUE"
                elif 500 <= click_x <= 675 and 425 <= click_y <= 475:

                    # Fetch next question
                    question, category, choices = get_new_question(difficulty)
                    showing_result = False  # Proceed to next question, hence we're no longer displaying the result

            # Handles the case where the user clicks on an option
            else:

                for i in range(len(choices)):
                    button_y = 240 + i * 70     # Represents the top of the current option box

                    # Check whether the user clicked on the CURRENT option box
                    if 50 < click_x < 850 and button_y < click_y < button_y + 50:
                        user_answer = choices[i]

                        # Check user's answer
                        is_correct, message, player_points = question.check_answer(player_points, user_answer)

                        pygame.display.update()

                        showing_result = True   # Move to RESULT SCREEN now

# Quit Pygame
end_program()

# ----------------
# ISSUE:
# - Make the user click on either CONTINUE or EXIT each time
#   https://chatgpt.com/c/68718d78-1294-800e-9379-82f982bd586c

# Instructions:
# - Create MAIN MENU
