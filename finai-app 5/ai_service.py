"""
AI integration layer for the AI Financial Advisor.

Routes to OpenAI or Gemini depending on which API key is present in the
environment. Never hardcode API keys here -- they are read from os.environ,
which config.py populates from a local .env file (see .env.example).

If no key is configured, get_ai_response() falls back to a rule-based
response so the rest of the app (routes, templates, UI) can be demoed and
graded without needing a live API key.
"""
import os
import requests


def get_ai_response(prompt, context=None):
    context = context or {}
    openai_key = os.environ.get("OPENAI_API_KEY")
    gemini_key = os.environ.get("GEMINI_API_KEY")

    system_prompt = (
        "You are FinAI, a personal finance advisor. Use the user's income, "
        "expenses, budgets and savings goals to give short, specific, "
        "actionable advice in Indian Rupees (INR). "
        f"User context: {context}"
    )

    try:
        if openai_key:
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {openai_key}"},
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                },
                timeout=15,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]

        if gemini_key:
            resp = requests.post(
                "https://generativelanguage.googleapis.com/v1beta/models/"
                f"gemini-1.5-flash:generateContent?key={gemini_key}",
                json={"contents": [{"parts": [{"text": f"{system_prompt}\n\nUser: {prompt}"}]}]},
                timeout=15,
            )
            resp.raise_for_status()
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"]

    except Exception:
        # Any network/API error falls through to the offline response below
        # rather than breaking the advisor page.
        pass

    return _fallback_response(context)


def _fallback_response(context):
    income = context.get("monthly_income") or 60000
    expenses = context.get("monthly_expenses") or 34250
    savings = income - expenses
    return (
        f"Based on your income of \u20b9{income:,.0f} and expenses of \u20b9{expenses:,.0f}, "
        f"you're currently saving about \u20b9{savings:,.0f} per month. Consider trimming "
        "discretionary categories like shopping and entertainment by 10-15% to reach "
        "your savings goal faster. (Add an OPENAI_API_KEY or GEMINI_API_KEY to .env "
        "for live AI-generated responses.)"
    )
