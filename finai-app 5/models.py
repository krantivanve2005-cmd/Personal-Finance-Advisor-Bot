from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    monthly_income = db.Column(db.Float, default=0)
    financial_goal = db.Column(db.String(255))
    currency = db.Column(db.String(10), default="INR")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    incomes = db.relationship("Income", backref="user", lazy=True, cascade="all, delete-orphan")
    expenses = db.relationship("Expense", backref="user", lazy=True, cascade="all, delete-orphan")
    budgets = db.relationship("Budget", backref="user", lazy=True, cascade="all, delete-orphan")
    goals = db.relationship("SavingsGoal", backref="user", lazy=True, cascade="all, delete-orphan")
    recommendations = db.relationship("AIRecommendation", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ExpenseCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    source = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), default="Card")
    date = db.Column(db.Date, default=datetime.utcnow)


class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    limit_amount = db.Column(db.Float, nullable=False)
    month = db.Column(db.String(20), nullable=False)  # e.g. "2026-09"


class SavingsGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    saved_amount = db.Column(db.Float, default=0)

    @property
    def progress_pct(self):
        if not self.target_amount:
            return 0
        return round(min(self.saved_amount / self.target_amount * 100, 100))


class MonthlyReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    month = db.Column(db.String(20), nullable=False)
    total_income = db.Column(db.Float)
    total_expenses = db.Column(db.Float)
    total_savings = db.Column(db.Float)
    ai_summary = db.Column(db.Text)


class AIRecommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
