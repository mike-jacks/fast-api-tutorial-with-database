import requests
import models
import json
import random

def post_question(question_text: str, choices: list[tuple[str, bool]]):
    url = "http://127.0.0.1:8000/questions"
    data = {
        "question_text": question_text,
        "choices": [{"choice_text": choice[0], "is_correct": choice[1]} for choice in choices]
    }
    response = requests.post(url, json=data)
    print(response.json())
    return response.json()

def get_question(question_id: int):
    url = f"http://127.0.0.1:8000/questions/{question_id}"
    response = requests.get(url)
    print(response.json())
    return response.json()

def get_choices(question_id: int):
    url = f"http://127.0.0.1:8000/choices/{question_id}"
    response = requests.get(url)
    print(response.json())
    return response.json()

def create_question():
    while True:
        question_text = input("Enter the question text: ")
        choices = []
        while True:
            choice_text = input("Enter the choice text: ")
            is_correct = input("Is this choice correct? (y/n): ")
            choices.append((choice_text, is_correct == 'y'))
            if input("Do you want to add another choice? (y/n): ") != 'y':
                break
        post_question(question_text, choices)
        if input("Do you want to add another question? (y/n): ") != 'y':
            break

def update_question(question_id: int):
    question = get_question(question_id)
    question_text = input("Enter the question text: ")
    choices = []
    while True:
        choice_text = input("Enter the choice text: ")
        is_correct = input("Is this choice correct? (y/n): ")
        choices.append((choice_text, is_correct == 'y'))
        if input("Do you want to add another choice? (y/n): ") != 'y':
            break
    url = f"http://127.0.0.1:8000/questions/{question_id}"
    data = {
        "question_text": question_text,
        "choices": [{"choice_text": choice[0], "is_correct": choice[1]} for choice in choices]
    }
    response = requests.put(url, json=data)
    print(response.json())
    return response.json()

def delete_a_question(question_id: int):
    url = f"http://127.0.0.1:8000/questions/{question_id}"
    response = requests.delete(url)
    print(response.json())
    return response.json()

def answer_a_random_question():
    questions = requests.get("http://127.0.0.1:8000/questions").json()
    random_question = random.choice(questions)
    print(random_question['question_text'])
    for i, choice in enumerate(random_question['choices'], start=1):
        print(f"{i}. {choice['choice_text']}")
    correct_answer = [choice['choice_text'] for choice in random_question['choices'] if choice['is_correct']][0]
    while True:
        try:
            guessed_answer = int(input("Enter your answer: ")) - 1
            if guessed_answer < 0 or guessed_answer >= len(random_question['choices']):
                print("Invalid input")
                continue
            break
        except ValueError:
            print("Invalid input")
            continue
    print(f"You guessed: {random_question['choices'][guessed_answer]['choice_text']}")
    print(f"The correct answer is: {correct_answer}")
    if random_question['choices'][guessed_answer]['choice_text'] == correct_answer:
        print("Correct!")
    else:
        print("Incorrect!")

def main():
    while True:
        user_input = input("Do you want to create a question (1), get a question (2), get choices (3), answer a random question (4), update a question (5), delete a question (6), or exit (7)?: ")
        match user_input:
            case "1":
                create_question()
            case "2":
                question_id = int(input("Enter the question id: "))
                get_question(question_id)
            case "3":
                question_id = int(input("Enter the question id: "))
                get_choices(question_id)
            case "4":
                answer_a_random_question()
            case "5":
                question_id = int(input("Enter the question id: "))
                update_question(question_id)
            case "6":
                question_id = int(input("Enter the question id: "))
                delete_a_question(question_id)
            case "7":
                break
            case _:
                print("Invalid input")
    
    

if __name__ == '__main__':
    main()