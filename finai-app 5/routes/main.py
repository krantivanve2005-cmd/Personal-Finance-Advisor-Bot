from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from extensions import db
from models import Income, Expense, SavingsGoal, Budget

main_bp = Blueprint("main", __name__)

EXPENSE_CATEGORIES = [
    "Food", "Transport", "Shopping", "Bills",
    "Education", "Entertainment", "Healthcare", "Other",
]


@main_bp.route("/")
def landing():
    return render_template("landing.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    incomes = Income.query.filter_by(user_id=current_user.id).all()
    expenses = Expense.query.filter_by(user_id=current_user.id).all()

    total_income = sum(i.amount for i in incomes) or current_user.monthly_income
    total_expenses = sum(e.amount for e in expenses)
    total_savings = total_income - total_expenses

    by_category = {}
    for e in expenses:
        by_category[e.category] = by_category.get(e.category, 0) + e.amount

    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    budget_rows = []
    for b in budgets:
        spent = by_category.get(b.category, 0)
        pct = round(min(spent / b.limit_amount * 100, 999)) if b.limit_amount else 0
        budget_rows.append({"category": b.category, "spent": spent, "limit": b.limit_amount, "pct": pct})

    return render_template(
        "dashboard.html",
        total_income=total_income,
        total_expenses=total_expenses,
        total_savings=total_savings,
        by_category=by_category,
        budget_rows=budget_rows,
    )


@main_bp.route("/transactions")
@login_required
def transactions():
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    incomes = Income.query.filter_by(user_id=current_user.id).order_by(Income.date.desc()).all()
    return render_template(
        "transactions.html",
        expenses=expenses,
        incomes=incomes,
        categories=EXPENSE_CATEGORIES,
    )


@main_bp.route("/transactions/add-expense", methods=["POST"])
@login_required
def add_expense():
    date_str = request.form.get("date")
    e = Expense(
        user_id=current_user.id,
        description=request.form.get("description", "").strip() or "Expense",
        category=request.form.get("category", "Other"),
        amount=float(request.form.get("amount", 0) or 0),
        payment_method=request.form.get("payment_method", "Card"),
        date=datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else datetime.utcnow().date(),
    )
    db.session.add(e)
    db.session.commit()
    flash("Expense added.", "success")
    return redirect(url_for("main.transactions"))


@main_bp.route("/transactions/add-income", methods=["POST"])
@login_required
def add_income():
    i = Income(
        user_id=current_user.id,
        source=request.form.get("source", "Income").strip() or "Income",
        amount=float(request.form.get("amount", 0) or 0),
    )
    db.session.add(i)
    db.session.commit()
    flash("Income added.", "success")
    return redirect(url_for("main.transactions"))


@main_bp.route("/savings")
@login_required
def savings():
    goals = SavingsGoal.query.filter_by(user_id=current_user.id).all()
    return render_template("savings.html", goals=goals)


@main_bp.route("/savings/create", methods=["POST"])
@login_required
def create_goal():
    g = SavingsGoal(
        user_id=current_user.id,
        name=request.form.get("name", "New Goal").strip() or "New Goal",
        target_amount=float(request.form.get("target_amount", 0) or 0),
        saved_amount=float(request.form.get("saved_amount", 0) or 0),
    )
    db.session.add(g)
    db.session.commit()
    flash("Savings goal created.", "success")
    return redirect(url_for("main.savings"))
