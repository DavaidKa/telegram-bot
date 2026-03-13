import random
from typing import List, Dict


class QuizService:
    """Сервис викторин"""
    
    QUIZZES = {
        "movies": [
            {
                "question": "Кто снял фильм 'Начало'?",
                "options": ["Кристофер Нолан", "Стивен Спилберг", "Квентин Тарантино", "Мартин Скорсезе"],
                "correct": 0
            },
            {
                "question": "В каком году вышел первый фильм 'Матрица'?",
                "options": ["1997", "1999", "2001", "2003"],
                "correct": 1
            },
            {
                "question": "Кто сыграл Железного человека?",
                "options": ["Крис Эванс", "Роберт Дауни мл.", "Крис Хемсворт", "Марк Руффало"],
                "correct": 1
            }
        ],
        "music": [
            {
                "question": "Кто исполнил песню 'Bohemian Rhapsody'?",
                "options": ["The Beatles", "Queen", "Led Zeppelin", "Pink Floyd"],
                "correct": 1
            },
            {
                "question": "Сколько струн у стандартной гитары?",
                "options": ["4", "5", "6", "7"],
                "correct": 2
            },
            {
                "question": "Кто известен как 'Король поп-музыки'?",
                "options": ["Элвис Пресли", "Майкл Джексон", "Принс", "Дэвид Боуи"],
                "correct": 1
            }
        ],
        "geo": [
            {
                "question": "Какая самая большая страна в мире?",
                "options": ["Канада", "Китай", "США", "Россия"],
                "correct": 3
            },
            {
                "question": "Столица Австралии?",
                "options": ["Сидней", "Мельбурн", "Канберра", "Брисбен"],
                "correct": 2
            },
            {
                "question": "Сколько континентов на Земле?",
                "options": ["5", "6", "7", "8"],
                "correct": 2
            }
        ],
        "science": [
            {
                "question": "Какая планета ближайшая к Солнцу?",
                "options": ["Венера", "Земля", "Меркурий", "Марс"],
                "correct": 2
            },
            {
                "question": "Сколько костей в теле взрослого человека?",
                "options": ["186", "206", "226", "246"],
                "correct": 1
            },
            {
                "question": "Что такое H2O?",
                "options": ["Кислород", "Водород", "Вода", "Перекись"],
                "correct": 2
            }
        ]
    }
    
    @staticmethod
    def get_quiz(category: str = "random", count: int = 5) -> List[Dict]:
        """Получить викторину"""
        if category == "random":
            all_questions = []
            for cat_questions in QuizService.QUIZZES.values():
                all_questions.extend(cat_questions)
            questions = random.sample(all_questions, min(count, len(all_questions)))
        else:
            cat_questions = QuizService.QUIZZES.get(category, [])
            questions = random.sample(cat_questions, min(count, len(cat_questions)))
        
        return questions
    
    @staticmethod
    def check_answer(question: Dict, answer_index: int) -> bool:
        """Проверить ответ"""
        return question["correct"] == answer_index
    
    @staticmethod
    def calculate_score(correct_answers: int, total_questions: int) -> Dict:
        """Рассчитать результат"""
        percentage = (correct_answers / total_questions) * 100
        
        if percentage >= 90:
            grade = "🏆 Отлично!"
            message = "Ты настоящий эксперт!"
        elif percentage >= 70:
            grade = "🎯 Хорошо!"
            message = "Отличный результат!"
        elif percentage >= 50:
            grade = "👍 Неплохо"
            message = "Можешь лучше!"
        else:
            grade = "📚 Учись дальше"
            message = "Попробуй еще раз!"
        
        return {
            "correct": correct_answers,
            "total": total_questions,
            "percentage": percentage,
            "grade": grade,
            "message": message
        }


quiz_service = QuizService()
