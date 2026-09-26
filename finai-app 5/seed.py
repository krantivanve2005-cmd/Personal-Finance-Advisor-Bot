"""Seed demo data matching the FinAI design brief (Priya, INR amounts, etc).
Run with: python seed.py
"""
from datetime import date
from app import create_app
from extensions import db
from models import User, Income, Expense, SavingsGoal, Budget

app = create_app()

with app.app_context():
    if User.query.filter_by(email="priya@email.com").first():
        print("Demo data already exists -- skipping seed.")
    else:
        user = User(
            full_name="Priya Sharma",
            email="priya@email.com",
            monthly_income=60000,
            financial_goal="Save \u20b92,00,000 for an emergency fund.",
        )
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        db.session.add(Income(user_id=user.id, source="Salary", amount=60000, date=date(2026, 9, 23)))

        expenses = [
            ("Grocery", "Food", 1250, date(2026, 9, 24)),
            ("Bus Pass", "Transport", 800, date(2026, 9, 21)),
            ("Shopping", "Shopping", 2500, date(2026, 9, 20)),
            ("Electricity Bill", "Bills", 1800, date(2026, 9, 18)),
            ("Movie Night", "Entertainment", 600, date(2026, 9, 15)),
        ]
        for desc, cat, amt, d in expenses:
            db.session.add(Expense(user_id=user.id, description=desc, category=cat, amount=amt, date=d))

        for name, target, saved in [
            ("New Laptop", 80000, 45000),
            ("Emergency Fund", 100000, 62000),
            ("Vacation", 50000, 20000),
        ]:
            db.session.add(SavingsGoal(user_id=user.id, name=name, target_amount=target, saved_amount=saved))

        for cat, limit in [("Food", 8000), ("Transport", 5000), ("Entertainment", 3000), ("Shopping", 4000)]:
            db.session.add(Budget(user_id=user.id, category=cat, limit_amount=limit, month="2026-09"))

        db.session.commit()
        print("Demo data seeded. Login with priya@email.com / password123")
