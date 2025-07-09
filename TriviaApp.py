
import random
import requests
import html
import time
from colorama import Fore, Style

# ANSI colour codes
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


class TriviaQuestion:
    """Python Implementation of a Trivia Game."""

    question: str
    difficulty: str
    category: str
    correct_ans: str
    options: list[str]

    def __init__(self, ques_dict: dict):

        # html.unescape() translates special characters in HTML script into readable text
        self.question = html.unescape(ques_dict["question"])
        self.difficulty = html.unescape(ques_dict["difficulty"])
        self.category = html.unescape(ques_dict["category"])
        self.correct_ans = html.unescape(ques_dict["correct_answer"])
        self.options = [html.unescape(ans) for ans in ques_dict["incorrect_answers"]] + [self.correct_ans]

    def check_answer(self, points: int, user_response: str) -> tuple:
        """Print whether the user's answer is CORRECT or WRONG & update points accordingly"""

        if self.correct_ans.lower().strip() == user_response.lower().strip():

            is_correct = True
            message = "CORRECT!"

            if self.difficulty == "easy":
                points += 100
            elif self.difficulty == "medium":
                points += 200
            else:
                points += 300
        else:

            is_correct = False
            message = "WRONG!"
            points -= 50

        return is_correct, message, points


def fetch_question(difficulty: str, topic: str) -> TriviaQuestion:
    """Fetch a set of questions from Open Trivia DB website."""

    # Dictionary that maps the TOPIC to a NUMBER that appears in the URL
    categories = {"sports": 21, "celebrities": 26, "history": 23, "art": 25, "animals": 27}

    # Get one questions at a time for the corresponding CATEGORY & DIFFICULTY
    url = f"https://opentdb.com/api.php?amount=1&category={categories[topic]}&difficulty={difficulty}&type=multiple"

    # Asking for the data from the URL link & converting it to a Python dictionary
    raw_data = requests.get(url)
    clean_data = raw_data.json()

    # Returning the entire dictionary, including a list of dictionaries that contains the set of questions
    # (type, difficulty, category...)
    # If the response_code != 0, call the function again
    if clean_data["response_code"] == 0:
        return TriviaQuestion(clean_data["results"][0])
    else:
        return fetch_question(difficulty, topic)


# Game Loop
if __name__ == "__main__":

    player_points = 0

    # Creating a string of the alphabet (e.g. "ABCDEFG...")
    valid_letters = ["A", "B", "C", "D"]
    valid_difficulties = {"easy", "medium", "hard"}
    valid_categories = {"sports", "celebrities", "art", "animals", "history"}

    while True:

        print("\n----------")

        # Loop keeps running until user enters a VALID mode
        while True:

            mode = input(f"{BOLD}{UNDERLINE}Difficulty?{Style.RESET_ALL}:\n   -> EASY (😃)\n   -> MEDIUM "
                         f"(🙂)\n   -> HARD (😰)").lower().strip()

            if mode in valid_difficulties:
                break
            else:
                print("\n----------")
                print(f"Your answer was {BOLD}{Fore.RED}INVALID{Style.RESET_ALL}! 👎 \n\nTry again!")

        # Loop keeps running until user enters a VALID category
        while True:
            category = input(f"\n{BOLD}{UNDERLINE}Category?{Style.RESET_ALL}:\n" 
                             "   -> SPORTS (⚽)\n   -> CELEBRITIES  (🤩)\n   "
                             "-> ART (🎨)\n   -> ANIMALS (🐓)\n   -> HISTORY (📜)").lower().strip()

            if category in valid_categories:
                break
            else:
                print("\n----------")
                print(f"Your answer was {BOLD}{Fore.RED}INVALID{Style.RESET_ALL}! 👎 \n\nTry again!")

        trivia_ques = fetch_question(mode, category)

        # Shuffling the list of options for the question
        random.shuffle(trivia_ques.options)

        # Print the QUESTION & each OPTION individually
        print("\n----------")
        print(f"QUESTION: {BOLD}{trivia_ques.question}{Style.RESET_ALL}\n")
        for i in range(len(trivia_ques.options)):
            time.sleep(1)
            print(f"{valid_letters[i]}. {trivia_ques.options[i]}")

        time.sleep(1)

        while True:
            response = input("\nYour Answer: ").upper().strip()
            print("\n----------")

            if response in valid_letters:
                break
            else:
                # Print ERROR message
                print(f"Your answer was {BOLD}{Fore.RED}INVALID{Style.RESET_ALL}. 👎 \n\nTry again!")

        # Mapping the user's letter to corresponding answer option
        # .index returns the index that "letter" appears in the alphabet (e.g. If "letter" == "c, .index would return 2)
        user_answer = trivia_ques.options[valid_letters.index(response)]

        time.sleep(1)
        # Check whether the user's answer is CORRECT
        player_points = trivia_ques.check_answer(player_points, user_answer.lower())

        time.sleep(1)
        print(f"\nYou have {BOLD}{Fore.BLUE}{player_points} {Fore.RESET}points{Style.RESET_ALL}!")

        # Ask the user if they want to KEEP PLAYING
        print("\n----------")
        exit_or_no = input("Do you want to KEEP PLAYING? (enter \"yes\"):").lower().strip()

        if exit_or_no != "yes":
            print("\nThanks for playing!")
            break

# INSTRUCTIONS:
        # - Fix PRINT statement for categories
        # - Find a way to ELIMINATE USED questions
        # - ISSUE: 'sleep' method isn't working before points are displayed
        # - Improve UI + Front-End
        # ----------------

        # Ask ChatGPT (https://opentdb.com/api_token.php?command=request)


