import uuid
import json
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from app.models.user_model import User
from app.models.event_model import Event
from app.db.session import SessionLocal, engine
from app.db.base import Base

# ✅ Tạo bảng nếu chưa có
Base.metadata.create_all(bind=engine)

def init_db():
    print("⚡ Start seeding")
    db: Session = SessionLocal()

    try:
        # ❌ Nếu đã có user → không seed lại
        # if db.query(User).first():
        #     print("✅ Database already seeded.")
        #     return

        now = datetime.now(timezone.utc)

        # ✅ Danh sách người dùng mẫu
        users = [
            User(
                id=str(uuid.uuid4()),
                first_name="Wei Ling",
                last_name="Tan",
                phone_number="+65 8123 4567",
                email="weiling.tan@singmail.sg",
                avatar="",
                gender="female",
                job_title="Frontend Engineer",
                company="Grab",
                city="Singapore",
                state="SG",
            ),
            User(
                id=str(uuid.uuid4()),
                first_name="Jun Hao",
                last_name="Lim",
                phone_number="+65 9876 5432",
                email="junhao.lim@byte.sg",
                avatar="",
                gender="male",
                job_title="DevOps Engineer",
                company="Sea Group",
                city="Singapore",
                state="SG",
            ),
            User(
                id=str(uuid.uuid4()),
                first_name="Sheryl",
                last_name="Ng",
                phone_number="+65 8234 7890",
                email="sheryl.ng@temasek.sg",
                avatar="",
                gender="female",
                job_title="Product Manager",
                company="Shopee",
                city="Singapore",
                state="SG",
            ),
            User(
                id=str(uuid.uuid4()),
                first_name="Zhi Yong",
                last_name="Tan",
                phone_number="+65 8120 3344",
                email="zhiyong.tan@open.sg",
                avatar="",
                gender="male",
                job_title="AI Engineer",
                company="GovTech",
                city="Singapore",
                state="SG",
            ),
            User(
                id=str(uuid.uuid4()),
                first_name="Mei Xin",
                last_name="Chong",
                phone_number="+65 8000 1111",
                email="meixin.chong@dsb.sg",
                avatar="",
                gender="female",
                job_title="UX Designer",
                company="DBS Bank",
                city="Singapore",
                state="SG",
            ),
        ]

        db.add_all(users)
        db.commit()
        for u in users:
            db.refresh(u)

        user_ids = [u.id for u in users]

        # ✅ Danh sách sự kiện mẫu
        events = [
            Event(
                id=str(uuid.uuid4()),
                slug="grab-townhall-2025",
                title="Grab Annual Townhall",
                description="Company-wide strategy update & Q&A with leadership.",
                start_at=now,
                end_at=now + timedelta(hours=2),
                venue="Grab HQ, One-North",
                max_capacity=200,
                owner=user_ids[0],
                hosts=",".join([user_ids[0], user_ids[2]]),
                attendees=json.dumps([user_ids[1], user_ids[4]]),
                status="published",
            ),
            Event(
                id=str(uuid.uuid4()),
                slug="tech-sg-meetup",
                title="TechSG Monthly Meetup",
                description="Networking and lightning talks by local devs.",
                start_at=now,
                end_at=now + timedelta(hours=3),
                venue="Pixel Building, One-North",
                max_capacity=100,
                owner=user_ids[2],
                hosts=",".join([user_ids[2]]),
                attendees=json.dumps([user_ids[0], user_ids[1], user_ids[3]]),
                status="draft",
            ),
            Event(
                id=str(uuid.uuid4()),
                slug="ai-in-govtech",
                title="AI in GovTech Workshop",
                description="Learn how GovTech is using AI in public services.",
                start_at=now,
                end_at=now + timedelta(hours=1),
                venue="GovTech Campus @ Maxwell",
                max_capacity=50,
                owner=user_ids[3],
                hosts=",".join([user_ids[3]]),
                attendees=json.dumps([user_ids[4]]),
                status="published",
            ),
        ]

        db.add_all(events)
        db.commit()
    except Exception as e:
        print("❌ Error seeding database:", e)
        db.rollback()

    finally:
        db.close()
        print("✅ Seed done")

if __name__ == "__main__":
    print("⚡ Calling init_db() now")
    init_db()