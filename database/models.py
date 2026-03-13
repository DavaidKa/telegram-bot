from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timedelta

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(255))
    first_name = Column(String(255))
    language_code = Column(String(10), default="ru")
    
    is_vip = Column(Boolean, default=False)
    vip_until = Column(DateTime, nullable=True)
    
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    referral_count = Column(Integer, default=0)
    
    daily_usage = Column(Integer, default=0)
    last_usage_date = Column(DateTime, default=datetime.utcnow)
    
    total_generated = Column(Integer, default=0)
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    referrals = relationship("User", backref="referrer", remote_side=[id])
    payments = relationship("Payment", back_populates="user")
    content = relationship("GeneratedContent", back_populates="user")
    
    def is_vip_active(self) -> bool:
        if not self.is_vip:
            return False
        if self.vip_until and self.vip_until < datetime.utcnow():
            return False
        return True
    
    def can_generate(self, free_limit: int = 5) -> bool:
        if self.is_vip_active():
            return True
        
        # Сброс счетчика если новый день
        if self.last_usage_date.date() < datetime.utcnow().date():
            return True
            
        return self.daily_usage < free_limit
    
    def add_experience(self, amount: int = 10):
        self.experience += amount
        # Каждые 100 опыта = новый уровень
        new_level = (self.experience // 100) + 1
        if new_level > self.level:
            self.level = new_level
            return True  # Level up!
        return False


class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    payment_system = Column(String(50))  # paypal, yoomoney, qiwi
    transaction_id = Column(String(255), unique=True)
    
    status = Column(String(50), default="pending")  # pending, completed, failed
    payment_type = Column(String(50))  # vip, donation
    
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="payments")


class GeneratedContent(Base):
    __tablename__ = "generated_content"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    content_type = Column(String(50))  # meme, ai_image, quiz, game
    prompt = Column(Text, nullable=True)
    result_data = Column(Text, nullable=True)
    
    shared = Column(Boolean, default=False)
    likes = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="content")


class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    
    questions_data = Column(Text, nullable=False)  # JSON
    difficulty = Column(String(20), default="medium")
    
    plays_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_daily = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)


class QuizResult(Base):
    __tablename__ = "quiz_results"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    
    score = Column(Integer, nullable=False)
    max_score = Column(Integer, nullable=False)
    time_spent = Column(Integer)  # seconds
    
    created_at = Column(DateTime, default=datetime.utcnow)


class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    achievement_type = Column(String(100))  # first_meme, 10_referrals, level_5, etc
    title = Column(String(255))
    description = Column(Text)
    
    unlocked_at = Column(DateTime, default=datetime.utcnow)
