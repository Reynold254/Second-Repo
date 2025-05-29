import json
import random
import os

class QuizApp:
    def __init__(self, question_file, score_file="high_scores.json"):
        self.questions = self.load_questions(question_file)
        self.score_file = score_file
        self.score = 0
        self.total_questions = 0
        self.difficulty = None
        self.difficulty_multipliers = {
            "easy": 1,
            "medium": 2,
            "hard": 3
        }
        self.user_name = None

    def load_questions(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data['questions']
        except FileNotFoundError:
            print("Error: Questions file not found!")
            return []
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in questions file!")
            return []

    def load_high_scores(self):
        if os.path.exists(self.score_file):
            try:
                with open(self.score_file, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("Error: Invalid high scores file format. Starting fresh.")
                return []
        return []

    def save_high_score(self):
        high_scores = self.load_high_scores()
        high_scores.append({
            "name": self.user_name,
            "score": self.score,
            "difficulty": self.difficulty,
            "questions_answered": self.total_questions
        })
        high_scores = sorted(high_scores, key=lambda x: x["score"], reverse=True)[:10]  # Keep top 10
        try:
            with open(self.score_file, 'w') as file:
                json.dump(high_scores, file, indent=4)
        except Exception as e:
            print(f"Error saving high scores: {e}")

    def display_high_scores(self):
        high_scores = self.load_high_scores()
        if not high_scores:
            print("\nNo high scores yet!")
            return
        print("\n=== High Scores ===")
        for i, entry in enumerate(high_scores, 1):
            print(f"{i}. {entry['name']} - Score: {entry['score']} ({entry['difficulty']}, {entry['questions_answered']} questions)")

    def get_questions_by_category_and_difficulty(self, category, difficulty):
        return [q for q in self.questions if q['category'].lower() == category.lower() and q['difficulty'].lower() == difficulty.lower()]

    def display_question(self, question):
        print(f"\nQuestion: {question['question']}")
        for i, option in enumerate(question['options'], 1):
            print(f"{i}. {option}")
        while True:
            try:
                answer = int(input("Enter your answer (1-4): "))
                if 1 <= answer <= 4:
                    return question['options'][answer - 1]
                else:
                    print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def run_quiz(self, category, difficulty, num_questions):
        questions = self.get_questions_by_category_and_difficulty(category, difficulty)
        if not questions:
            print(f"No questions found for {category} category and {difficulty} difficulty!")
            return

        # Shuffle and select questions
        random.shuffle(questions)
        questions = questions[:min(num_questions, len(questions))]
        self.total_questions = len(questions)
        self.difficulty = difficulty

        print(f"\nStarting {category} quiz ({difficulty} difficulty) with {self.total_questions} questions...")
        for question in questions:
            user_answer = self.display_question(question)
            if user_answer.lower() == question['correct_answer'].lower():
                points = self.difficulty_multipliers[difficulty.lower()]
                self.score += points
                print(f"Correct! +{points} points")
                print(f"Explanation: {question['explanation']}")
            else:
                print(f"Wrong! Correct answer was: {question['correct_answer']}")
                print(f"Explanation: {question['explanation']}")

        self.display_results()
        self.save_high_score()

    def display_results(self):
        print("\n=== Quiz Results ===")
        print(f"Total Score: {self.score}")
        print(f"Questions Answered: {self.total_questions}")
        if self.total_questions > 0:
            percentage = (self.score / (self.total_questions * self.difficulty_multipliers[self.difficulty.lower()])) * 100
            print(f"Percentage: {percentage:.2f}%")

def main():
    quiz = QuizApp("questions.json")
    print("Welcome to the Quiz App!")
    quiz.user_name = input("Enter your name: ").strip() or "Anonymous"

    while True:
        print("\nChoose a category:")
        print("1. History")
        print("2. Science")
        print("3. Literature")
        print("4. View High Scores")
        print("5. Exit")
        category_choice = input("Enter your choice (1-5): ")

        category_map = {
            "1": "History",
            "2": "Science",
            "3": "Literature",
            "4": "view_scores",
            "5": "exit"
        }

        if category_choice not in category_map:
            print("Invalid choice! Please select 1, 2, 3, 4, or 5.")
            continue

        if category_choice == "5":
            print("Thank you for playing!")
            break

        if category_choice == "4":
            quiz.display_high_scores()
            continue

        category = category_map[category_choice]

        print("\nChoose difficulty level:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        difficulty_choice = input("Enter your choice (1-3): ")

        difficulty_map = {
            "1": "easy",
            "2": "medium",
            "3": "hard"
        }

        if difficulty_choice not in difficulty_map:
            print("Invalid choice! Please select 1, 2, or 3.")
            continue

        difficulty = difficulty_map[difficulty_choice]

        while True:
            try:
                num_questions = int(input("How many questions would you like (1-10)? "))
                if 1 <= num_questions <= 10:
                    break
                else:
                    print("Please enter a number between 1 and 10.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        quiz.score = 0  # Reset score for new quiz
        quiz.run_quiz(category, difficulty, num_questions)

if __name__ == "__main__":
    main()