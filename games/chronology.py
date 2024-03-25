import os
import string
import json
import random
import time


class Question:
    def __init__(self, term: str, year: str, president: str, answer_key: dict):
        self.question = term
        self.president = president
        self.answer = answer_key[president]
        self.year = year
        self.time_start = 0
        self.time = 0

    def start_question(self):
        self.time_start = time.time()

    def answer_question(self, answer: str):
        self.time = time.time() - self.time_start
        if answer:
            if answer.strip().lower() == self.answer:
                return True
        return False

    def __str__(self):
        return self.question


class ChronologyTest:
    def __init__(self, questions: dict):
        self.name = "Chronology"
        self.answer_key = self.generate_answer_key(questions)
        self.questions = self.generate_questions(questions, self.answer_key)
        self.unanswered_questions = self.questions.copy()
        self.correct_answered_questions = []
        self.incorrect_answered_questions = []
        self.total_time = 0
        self.streak = 0
        self.highest_streak = 0

    def print_game_state(self):
        answered = len(self.correct_answered_questions) + len(self.incorrect_answered_questions) + 1
        total = len(self.questions)
        print(f"{self.name}:")
        print(f"Question: {answered}/{total}  ", end="")
        print(f"Streak: {self.streak}  ", end="")
        print(f"Average time: {round(self.get_average_time(), 3)} seconds\n")

    def print_answer_key(self):
        for president, letter in self.answer_key.items():
            print(f"{letter}: {president}")

    def print_receipt(self):
        os.system("cls||clear")
        print("Chronology Results:")
        print(f"{len(self.correct_answered_questions)}/{len(self.questions)} questions answered correctly")
        print(f"Total time: {round(self.total_time, 3)}")
        print(f"{round(self.get_average_time(), 3)} seconds per question")
        print(f"Highest streak: {self.highest_streak}")
        print(f"Last streak: {self.streak}")
        if self.streak == len(self.questions):
            print("Perfect Score! :D\nYou've mastered these sets.")
        input()

    def get_average_time(self):
        self.total_time = 0
        if len(self.unanswered_questions) >= len(self.questions):
            return 0
        for question in self.questions:
            self.total_time += question.time
        return self.total_time/(len(self.correct_answered_questions)+len(self.incorrect_answered_questions))

    def start(self):
        playing = True
        while playing:
            os.system('color 7')
            os.system('cls||clear')
            self.print_game_state()
            self.print_answer_key()
            question = self.unanswered_questions[random.randint(0, len(self.unanswered_questions) - 1)]
            print(question)
            question.start_question()
            answer = input()
            if answer == 'end':
                break
            correct = question.answer_question(answer)
            if correct:
                if question.time > self.get_average_time():
                    os.system('color 2')
                else:
                    os.system('color 3')
                self.streak += 1
                self.highest_streak = max(self.streak, self.highest_streak)
                self.correct_answered_questions.append(question)
                print(f"{round(question.time, 3)} seconds")
                print("You've done it!'")
                time.sleep(1)
            else:
                os.system('color 4')
                self.streak = 0
                self.incorrect_answered_questions.append(question)
                print(f"{round(question.time, 3)} seconds")
                print(f"INCORRECT\nCorrect Answer: {question.president}")
                time.sleep(2)
            self.unanswered_questions.remove(question)
            if len(self.unanswered_questions) == 0:
                playing = False
        self.print_receipt()

    @staticmethod
    def generate_answer_key(questions: dict):
        alphabet = string.ascii_lowercase
        answers = [i for i in alphabet] + [i*2 for i in alphabet]
        answer_key = {}
        for i, president in enumerate(questions.keys()):
            answer_key[president] = answers[i]
        return answer_key

    @staticmethod
    def generate_questions(questions: dict, answer_key: dict) -> list:
        question_list = []
        for president, terms in questions.items():
            for term in terms:
                question_list.append(Question(term, '', president, answer_key))
        return question_list

    @classmethod
    def create_game(cls):
        # Get studyset
        sets = [i.removesuffix('.json') for i in os.listdir('data/chronology')]
        options = {president: False for president in sets}
        while True:
            os.system("cls||clear")
            for chrono, selected in options.items():
                if selected:
                    print("[*]", end="")
                else:
                    print("[ ]", end="")
                chrono = chrono.replace("_", " ")
                final = []
                for i, letter in enumerate(chrono):
                    if chrono[i-1] == " ":
                        final.append(letter.upper())
                    else:
                        final.append(letter)
                print("".join(final))
            choose = input("Choose a set to add.\nType 'end' to continue.\n").strip().lower()
            if choose == "end":
                break
            for option in options.keys():
                if choose == option[0]:
                    options[option] = not(options[option])
        final_dict = {}
        for file, active in options.items():
            if active:
                with open("data/chronology/" + file + '.json', 'r') as f:
                    file_dict = json.loads(f.read())
                final_dict = dict(final_dict, **file_dict)
        return cls(final_dict)
