
import requests
import html


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
