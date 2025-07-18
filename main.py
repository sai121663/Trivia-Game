# This file will include GUI & handle the display of the Trivia game.

import pygame
import sys
import random
import textwrap
from typing import Optional
from TriviaApp import fetch_question, TriviaQuestion

# Initializing the game & setting up the display
pygame.init()
screen = pygame.display.set_mode((900, 500))    # (width, height)

# Fonts & Colours
fonts = {'small_font': pygame.font.SysFont("comic sans", 24),
         'big_font': pygame.font.SysFont("comic sans", 32),
         'bold_font': pygame.font.SysFont("impact", 32),
         'title_font': pygame.font.SysFont("chelsea market", 64)}

colours = {'WHITE': (255, 255, 255), 'GREY': (128, 128, 128), 'GREEN': (34, 139, 34), 'RED': (200, 50, 50),
           'BLUE': (30, 144, 255), 'YELLOW': (255, 215, 0), 'BLACK': (0, 0, 0)}

# Variables for game loop
# (choosing the difficulty as "medium" for beginner purposes)
player_points = 0
difficulty = "medium"
categories = ["sports", "celebrities", "art", "animals", "history"]
valid_letters = ["A", "B", "C", "D"]
message = ""
showing_result = False
is_correct = False
game_state = "menu"
topic = None
clock = pygame.time.Clock()

# Load CORRECT & WRONG image into pygame
correct_img = pygame.image.load("that's correct.gif").convert()
wrong_img = pygame.image.load("that's wrong.gif").convert()


def quit_game() -> None:
    """Quits the game."""

    # Print the final amount of points
    screen.fill(colours['BLACK'])
    closing_text = fonts['big_font'].render(f"You ended with {player_points} points!", True, colours['YELLOW'])
    screen.blit(closing_text, (30, 20))

    # Display an image
    farewell_img = pygame.image.load("sad_to_leave.jpg").convert()
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
        line_surface = fonts['big_font'].render(line, True, colours['WHITE'])
        screen.blit(line_surface, (30, 90 + i * 50))  # Stacking the lines 50 pixels apart vertically


def display_options(choices_list: list[str]) -> None:
    """Helper function to visually print the MC options"""

    start_y = 240

    for i, option in enumerate(choices_list):
        options_text = fonts['small_font'].render(f"{valid_letters[i]}. {option}", True, colours['BLUE'])

        # Draw rectangle around each option
        pygame.draw.rect(screen, colours['RED'], (50, start_y + i * 70, 800, 50), 2)
        screen.blit(options_text, (60, start_y + i * 70 + 10))


def get_new_question(level: str) -> tuple:
    """Fetching a new question & returning """

    ques = fetch_question(level, topic)
    choices_list = ques.options

    # Randomize the order of the options
    random.shuffle(choices_list)

    return ques, choices_list


def draw_quit_button() -> None:
    """Drawing a QUIT button to end the game."""

    # Creating a rect. object (in theory) & initializing the position & size of the "quit" button
    # Parameters: (x, y, width, height)
    quit_button = pygame.Rect(725, 425, 150, 50)

    # DRAWING the "quit" button onto the screen
    pygame.draw.rect(screen, colours['RED'], quit_button)

    # Printing "QUIT" as text
    quit_label = fonts['bold_font'].render("QUIT", True, colours['WHITE'])
    screen.blit(quit_label, (765, 425))


def draw_continue_button() -> None:
    """Drawing a CONTINUE button to resume the game."""

    # Creating a rectangle object for the button
    continue_button = pygame.Rect(500, 425, 175, 50)
    pygame.draw.rect(screen, colours['GREEN'], continue_button)

    # Printing "CONTINUE" as text
    continue_label = fonts['bold_font'].render("CONTINUE", True, colours['WHITE'])
    screen.blit(continue_label, (525, 425))


def draw_categories() -> None:
    """Drawing buttons for the five categories."""

    for i, topic in enumerate(categories):

        # Since we need 3 boxes on the left & 2 on the right, we calculate different x/y positions for the latter
        # categories
        if i < 3:
            x = 50
            y = 200 + i * 100
        else:
            x = 500
            y = 200 + (i - 3) * 100

        # Drawing button rectangles
        # (screen, colour, (x, y, width, height))
        pygame.draw.rect(screen, colours['RED'], (x, y, 350, 70))

        # Drawing button labels
        label = fonts['big_font'].render(f"{topic.upper()}", True, colours['WHITE'])
        screen.blit(label, (x + 20, y + 10))


def main_menu() -> Optional[str]:
    """Displaying the MAIN MENU."""

    screen.fill(colours["BLACK"])

    pygame.draw.rect(screen, colours["YELLOW"], (0, 0, 900, 100))

    # Creating a SHADOW
    shadow = fonts['title_font'].render("BRAINFUSE", True, colours['BLACK'])
    screen.blit(shadow, (322, 30))

    # Printing the game's title
    game_title = fonts['title_font'].render("BRAINFUSE", True, colours['WHITE'])
    screen.blit(game_title, (325, 35))

    # Prompting user to select a CATEGORY
    select_category = fonts['big_font'].render("Select your CATEGORY:", True, colours['WHITE'])
    screen.blit(select_category, (40, 110))

    # Helper function to draw the categories
    draw_categories()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_program()

        # If the user clicks on the mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_x, click_y = pygame.mouse.get_pos()

            for k in range(len(categories)):
                if k < 3:
                    button_x = 50   # Starting X position of current option box
                    button_y = 200 + k * 100    # Starting Y position of current option box
                else:
                    button_x = 500
                    button_y = 200 + (k - 3) * 100

                if button_x <= click_x <= button_x + 350 and button_y <= click_y <= button_y + 70:
                    return categories[k]

    pygame.display.update()
    return None


def disclaimer() -> None:
    """Printing a disclaimer message, before the game starts, advising the user to avoid clicking too fast."""

    screen.fill(colours['BLACK'])

    # Displaying text & warning the user to click SLOWLY
    disclaimer1 = fonts['title_font'].render("GLITCHY:", True, colours['RED'])
    screen.blit(disclaimer1, (150, 200))
    disclaimer2 = fonts['big_font'].render("Please click SLOWLY!", True, colours['WHITE'])
    screen.blit(disclaimer2, (375, 200))
    press_enter_msg = fonts['small_font'].render("(ENTER to continue)", True, colours['GREEN'])
    screen.blit(press_enter_msg, (325, 275))

    # Image of a turtle
    turtle_img = pygame.image.load("turtle.png").convert()
    screen.blit(turtle_img, (650, 350))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_program()   # I have to manually call the "end_program" function here, whereas in the game loop,
                # "end_program" was called by default after exiting the while loop.

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:    # Checking if the user has pressed ENTER
                    return


# GAME LOOP
running = True
while running:

    # Displaying the MENU; game hasn't started
    if game_state == "menu":
        while not topic:
            topic = main_menu()

        disclaimer()

        # Fetch first question
        # Written before changing the game_state to "playing" for a more efficient runtime
        question, choices = get_new_question(difficulty)

        game_state = "playing"

    # Game has started
    elif game_state == "playing":

        screen.fill(colours['BLACK'])

        # DRAWING BLOCK
        # Handles the display of the RESULT SCREEN
        if showing_result:

            # Display result message
            message_text = textwrap.wrap(message, width=50)
            for k, line in enumerate(message_text):

                # Message is printed in GREEN if the user's answer is CORRECT, and vice versa.
                if is_correct:
                    message_line = fonts['big_font'].render(line, True, colours['GREEN'])
                else:
                    message_line = fonts['big_font'].render(line, True, colours['RED'])

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
            score_text = fonts['big_font'].render(f"Score: {player_points}", True, colours['YELLOW'])
            screen.blit(score_text, (30, 20))  # Parameters: (screen, position)

            # Display QUESTION
            display_question(question, topic)

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
                        question, choices = get_new_question(difficulty)
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

                            showing_result = True  # Move to RESULT SCREEN now

    clock.tick(60)      # Prevents glitches by ensuring the game runs at a reasonable speed

# Quit Pygame
end_program()

# ----------------
# Instructions:
# - Clean up TriviaApp.py
# https://chatgpt.com/c/68718d78-1294-800e-9379-82f982bd586c
