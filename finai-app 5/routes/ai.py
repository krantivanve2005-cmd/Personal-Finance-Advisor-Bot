from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import AIRecommendation, Income, Expense
from ai_service import get_ai_response

ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/advisor")
@login_required
def advisor():
    history = (
        AIRecommendation.query.filter_by(user_id=current_user.id)
        .order_by(AIRecommendation.created_at.asc())
        .all()
    )
    return render_template("advisor.html", history=history)


@ai_bp.route("/api/advisor/ask", methods=["POST"])
@login_required
def ask():
    data = request.get_json(silent=True) or request.form
    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"error": "prompt is required"}), 400

    incomes = Income.query.filter_by(user_id=current_user.id).all()
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    context = {
        "monthly_income": sum(i.amount for i in incomes) or current_user.monthly_income,
        "monthly_expenses": sum(e.amount for e in expenses),
        "financial_goal": current_user.financial_goal,
    }
    answer = get_ai_response(prompt, context)

    rec = AIRecommendation(user_id=current_user.id, prompt=prompt, response=answer)
    db.session.add(rec)
    db.session.commit()

    return jsonify({"response": answer})
