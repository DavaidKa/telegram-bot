import random
from typing import Dict


class GameService:
    """Сервис мини-игр"""
    
    @staticmethod
    def play_dice() -> Dict:
        """Игра в кости"""
        user_roll = random.randint(1, 6)
        bot_roll = random.randint(1, 6)
        
        if user_roll > bot_roll:
            result = "win"
            message = f"🎉 Ты выиграл! Твой бросок: {user_roll}, мой: {bot_roll}"
            exp = 20
        elif user_roll < bot_roll:
            result = "lose"
            message = f"😔 Я выиграл! Твой бросок: {user_roll}, мой: {bot_roll}"
            exp = 5
        else:
            result = "draw"
            message = f"🤝 Ничья! Оба выбросили: {user_roll}"
            exp = 10
        
        return {
            "result": result,
            "message": message,
            "user_roll": user_roll,
            "bot_roll": bot_roll,
            "exp": exp
        }
    
    @staticmethod
    def play_rps(user_choice: str) -> Dict:
        """Камень-ножницы-бумага"""
        choices = ["rock", "paper", "scissors"]
        bot_choice = random.choice(choices)
        
        emoji_map = {
            "rock": "🪨",
            "paper": "📄",
            "scissors": "✂️"
        }
        
        wins = {
            "rock": "scissors",
            "paper": "rock",
            "scissors": "paper"
        }
        
        if user_choice == bot_choice:
            result = "draw"
            message = f"🤝 Ничья! Оба выбрали {emoji_map[user_choice]}"
            exp = 10
        elif wins[user_choice] == bot_choice:
            result = "win"
            message = f"🎉 Ты выиграл! {emoji_map[user_choice]} побеждает {emoji_map[bot_choice]}"
            exp = 20
        else:
            result = "lose"
            message = f"😔 Я выиграл! {emoji_map[bot_choice]} побеждает {emoji_map[user_choice]}"
            exp = 5
        
        return {
            "result": result,
            "message": message,
            "user_choice": user_choice,
            "bot_choice": bot_choice,
            "exp": exp
        }
    
    @staticmethod
    def play_number_guess() -> Dict:
        """Угадай число от 1 до 10"""
        secret_number = random.randint(1, 10)
        
        return {
            "secret_number": secret_number,
            "message": "🎲 Я загадал число от 1 до 10. Угадай!"
        }
    
    @staticmethod
    def check_number_guess(secret: int, guess: int) -> Dict:
        """Проверить угаданное число"""
        if guess == secret:
            result = "win"
            message = f"🎉 Правильно! Это было число {secret}!"
            exp = 30
        elif abs(guess - secret) == 1:
            result = "close"
            message = f"🔥 Очень близко! Было число {secret}"
            exp = 15
        else:
            result = "lose"
            message = f"😔 Не угадал! Было число {secret}"
            exp = 5
        
        return {
            "result": result,
            "message": message,
            "exp": exp
        }
    
    @staticmethod
    def daily_fortune() -> str:
        """Предсказание дня"""
        fortunes = [
            "🌟 Сегодня твой день! Удача на твоей стороне!",
            "💫 Отличные возможности ждут тебя сегодня!",
            "🍀 Удача улыбнется тебе в неожиданный момент!",
            "✨ Сегодня хороший день для новых начинаний!",
            "🎯 Твои усилия принесут плоды!",
            "🌈 Позитивные перемены уже близко!",
            "💪 Ты справишься со всеми задачами!",
            "🎨 Креативность на пике - используй это!",
            "🚀 Время действовать смело!",
            "💝 Хороший день для общения с друзьями!"
        ]
        
        return random.choice(fortunes)


game_service = GameService()
