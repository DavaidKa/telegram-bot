from PIL import Image, ImageDraw, ImageFont
import io
import random
from typing import Tuple


class MemeGenerator:
    """Генератор мемов"""
    
    TEMPLATES = {
        "drake": {
            "size": (600, 600),
            "texts": [
                {"pos": (320, 150), "max_width": 250},
                {"pos": (320, 450), "max_width": 250}
            ]
        },
        "distracted": {
            "size": (800, 450),
            "texts": [
                {"pos": (150, 50), "max_width": 200},
                {"pos": (400, 50), "max_width": 200},
                {"pos": (650, 50), "max_width": 200}
            ]
        },
        "brain": {
            "size": (600, 800),
            "texts": [
                {"pos": (300, 100), "max_width": 250},
                {"pos": (300, 300), "max_width": 250},
                {"pos": (300, 500), "max_width": 250},
                {"pos": (300, 700), "max_width": 250}
            ]
        }
    }
    
    @staticmethod
    def create_simple_meme(text_top: str, text_bottom: str = "") -> bytes:
        """Создать простой мем с текстом"""
        # Создаем изображение
        width, height = 600, 400
        colors = [
            (255, 107, 107),  # Красный
            (78, 205, 196),   # Бирюзовый
            (255, 195, 0),    # Желтый
            (199, 121, 208),  # Фиолетовый
            (116, 185, 255)   # Голубой
        ]
        
        bg_color = random.choice(colors)
        img = Image.new('RGB', (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Пытаемся загрузить шрифт
        try:
            font_large = ImageFont.truetype("arial.ttf", 48)
            font_small = ImageFont.truetype("arial.ttf", 36)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Рисуем текст сверху
        if text_top:
            MemeGenerator._draw_text_with_outline(
                draw, text_top, (width // 2, 60), font_large
            )
        
        # Рисуем текст снизу
        if text_bottom:
            MemeGenerator._draw_text_with_outline(
                draw, text_bottom, (width // 2, height - 60), font_small
            )
        
        # Добавляем водяной знак
        watermark = "Created with @YourBot"
        try:
            font_watermark = ImageFont.truetype("arial.ttf", 16)
        except:
            font_watermark = ImageFont.load_default()
        
        draw.text(
            (width - 200, height - 20),
            watermark,
            fill=(255, 255, 255, 128),
            font=font_watermark
        )
        
        # Конвертируем в bytes
        bio = io.BytesIO()
        img.save(bio, 'PNG')
        bio.seek(0)
        return bio.getvalue()
    
    @staticmethod
    def _draw_text_with_outline(draw, text: str, position: Tuple[int, int], font):
        """Рисует текст с обводкой"""
        x, y = position
        
        # Обводка (черная)
        for adj_x in range(-2, 3):
            for adj_y in range(-2, 3):
                draw.text(
                    (x + adj_x, y + adj_y),
                    text,
                    font=font,
                    fill=(0, 0, 0),
                    anchor="mm"
                )
        
        # Основной текст (белый)
        draw.text(
            (x, y),
            text,
            font=font,
            fill=(255, 255, 255),
            anchor="mm"
        )
    
    @staticmethod
    def create_motivational_quote() -> Tuple[str, bytes]:
        """Создать мотивационную цитату"""
        quotes = [
            "Начни сегодня, не жди завтра",
            "Ты сильнее, чем думаешь",
            "Каждый день - новая возможность",
            "Верь в себя",
            "Мечты сбываются",
            "Будь лучшей версией себя",
            "Никогда не сдавайся",
            "Ты можешь больше"
        ]
        
        quote = random.choice(quotes)
        image = MemeGenerator.create_simple_meme(quote)
        return quote, image
    
    @staticmethod
    def create_random_meme() -> bytes:
        """Создать случайный мем"""
        templates = [
            ("Когда понедельник", "Но ты готов"),
            ("Я:", "Мои проблемы:"),
            ("План", "Реальность"),
            ("Ожидание", "Реальность"),
            ("Я в зеркале", "Я на фото"),
        ]
        
        top, bottom = random.choice(templates)
        return MemeGenerator.create_simple_meme(top, bottom)


meme_gen = MemeGenerator()
