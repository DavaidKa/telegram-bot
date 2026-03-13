import io
from typing import Optional
from PIL import Image
from utils.logger import logger
from services.ai_tutor import ai_tutor


class PhotoSolver:
    """Сервис для распознавания текста с фото и решения задач"""
    
    def __init__(self):
        # Инициализируем OCR для русского и английского языков
        self.reader = None
        self.ocr_available = True
    
    def _get_reader(self):
        """Ленивая инициализация OCR reader"""
        if self.reader is None:
            try:
                import easyocr
                self.reader = easyocr.Reader(['ru', 'en'], gpu=False)
                logger.info("EasyOCR initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize EasyOCR: {e}")
                self.ocr_available = False
                return None
        return self.reader
    
    async def extract_text_from_image(self, image_bytes: bytes) -> Optional[str]:
        """
        Извлечь текст из изображения
        
        Args:
            image_bytes: Байты изображения
        
        Returns:
            Распознанный текст или None при ошибке
        """
        if not self.ocr_available:
            return None
        
        try:
            # Открываем изображение
            image = Image.open(io.BytesIO(image_bytes))
            
            # Проверяем размер изображения
            max_size = 2048
            if image.width > max_size or image.height > max_size:
                # Уменьшаем изображение
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                logger.info(f"Image resized to {image.width}x{image.height}")
            
            # Конвертируем в RGB если нужно
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Сохраняем в байты
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Распознаем текст
            reader = self._get_reader()
            if not reader:
                return None
            
            results = reader.readtext(img_byte_arr)
            
            # Собираем текст
            if results:
                text = ' '.join([result[1] for result in results])
                logger.info(f"OCR extracted {len(text)} characters")
                return text.strip()
            
            return None
        
        except Exception as e:
            logger.error(f"Error extracting text from image: {e}")
            return None
    
    async def solve_from_photo(self, image_bytes: bytes) -> str:
        """
        Распознать задачу с фото и решить её
        
        Args:
            image_bytes: Байты изображения
        
        Returns:
            Форматированный ответ с решением
        """
        if not self.ocr_available:
            return (
                "❌ OCR сервис временно недоступен.\n\n"
                "💡 Попробуйте:\n"
                "• Отправить текст вопроса вместо фото\n"
                "• Использовать /homework для текстовых вопросов"
            )
        
        # Распознаем текст
        text = await self.extract_text_from_image(image_bytes)
        
        if not text:
            return (
                "❌ Не удалось распознать текст на фото.\n\n"
                "💡 Советы:\n"
                "• Сделайте фото четче\n"
                "• Убедитесь, что текст хорошо виден\n"
                "• Попробуйте лучшее освещение\n"
                "• Или отправьте текст вопроса: /homework"
            )
        
        # Отправляем в AI для решения
        solution = await ai_tutor.solve_homework(text)
        
        return f"📷 Распознанный текст:\n{text}\n\n{solution}"


# Глобальный экземпляр сервиса
photo_solver = PhotoSolver()
