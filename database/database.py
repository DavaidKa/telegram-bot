from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from database.models import Base, User, Payment, GeneratedContent, Quiz, QuizResult, Achievement
from config import settings
from typing import Optional
from datetime import datetime, timedelta


engine = create_async_engine(settings.DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """Инициализация базы данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    """Получить сессию БД"""
    async with async_session_maker() as session:
        yield session


class Database:
    """Класс для работы с базой данных"""
    
    @staticmethod
    async def get_user(telegram_id: int) -> Optional[User]:
        async with async_session_maker() as session:
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            return result.scalar_one_or_none()
    
    @staticmethod
    async def create_user(telegram_id: int, username: str = None, 
                         first_name: str = None, referrer_id: int = None) -> User:
        async with async_session_maker() as session:
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name
            )
            
            # Обработка реферала
            if referrer_id:
                referrer = await Database.get_user(referrer_id)
                if referrer:
                    user.referrer_id = referrer.id
                    referrer.referral_count += 1
                    
                    # Бонус рефереру: 3 дня VIP
                    if referrer.vip_until:
                        referrer.vip_until += timedelta(days=settings.REFERRAL_BONUS_DAYS)
                    else:
                        referrer.is_vip = True
                        referrer.vip_until = datetime.utcnow() + timedelta(days=settings.REFERRAL_BONUS_DAYS)
                    
                    session.add(referrer)
            
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
    
    @staticmethod
    async def update_user(user: User):
        async with async_session_maker() as session:
            session.add(user)
            await session.commit()
    
    @staticmethod
    async def increment_usage(telegram_id: int) -> bool:
        async with async_session_maker() as session:
            user = await Database.get_user(telegram_id)
            if not user:
                return False
            
            # Сброс счетчика если новый день
            if user.last_usage_date.date() < datetime.utcnow().date():
                user.daily_usage = 0
            
            user.daily_usage += 1
            user.total_generated += 1
            user.last_usage_date = datetime.utcnow()
            
            # Добавляем опыт
            level_up = user.add_experience(10)
            
            session.add(user)
            await session.commit()
            
            return level_up
    
    @staticmethod
    async def activate_vip(telegram_id: int, days: int = 30):
        async with async_session_maker() as session:
            user = await Database.get_user(telegram_id)
            if not user:
                return False
            
            user.is_vip = True
            if user.vip_until and user.vip_until > datetime.utcnow():
                user.vip_until += timedelta(days=days)
            else:
                user.vip_until = datetime.utcnow() + timedelta(days=days)
            
            session.add(user)
            await session.commit()
            return True
    
    @staticmethod
    async def create_payment(user_id: int, amount: float, payment_system: str, 
                            payment_type: str = "vip") -> Payment:
        async with async_session_maker() as session:
            payment = Payment(
                user_id=user_id,
                amount=amount,
                payment_system=payment_system,
                payment_type=payment_type
            )
            session.add(payment)
            await session.commit()
            await session.refresh(payment)
            return payment
    
    @staticmethod
    async def save_content(user_id: int, content_type: str, prompt: str = None, 
                          result_data: str = None) -> GeneratedContent:
        async with async_session_maker() as session:
            content = GeneratedContent(
                user_id=user_id,
                content_type=content_type,
                prompt=prompt,
                result_data=result_data
            )
            session.add(content)
            await session.commit()
            await session.refresh(content)
            return content
    
    @staticmethod
    async def get_top_users(limit: int = 10):
        async with async_session_maker() as session:
            result = await session.execute(
                select(User).order_by(User.experience.desc()).limit(limit)
            )
            return result.scalars().all()
    
    @staticmethod
    async def get_user_stats(telegram_id: int) -> dict:
        user = await Database.get_user(telegram_id)
        if not user:
            return {}
        
        return {
            "level": user.level,
            "experience": user.experience,
            "total_generated": user.total_generated,
            "referrals": user.referral_count,
            "is_vip": user.is_vip_active(),
            "vip_until": user.vip_until.strftime("%Y-%m-%d") if user.vip_until else None
        }
    
    @staticmethod
    async def get_all_users():
        async with async_session_maker() as session:
            result = await session.execute(select(User))
            return result.scalars().all()
    
    @staticmethod
    async def get_stats():
        async with async_session_maker() as session:
            total_users = await session.execute(select(User))
            total_users = len(total_users.scalars().all())
            
            vip_users = await session.execute(select(User).where(User.is_vip == True))
            vip_users = len(vip_users.scalars().all())
            
            total_payments = await session.execute(select(Payment).where(Payment.status == "completed"))
            payments = total_payments.scalars().all()
            total_revenue = sum(p.amount for p in payments)
            
            return {
                "total_users": total_users,
                "vip_users": vip_users,
                "total_revenue": total_revenue,
                "total_payments": len(payments)
            }


db = Database()
