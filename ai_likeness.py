import re

TEMPLATE_WORDS = [
    "ご利用いただきありがとうございます",
    "貴重なご意見",
    "今後ともよろしく"
]

def calc_ai_likeness(text: str) -> int:
    score = 100

    for w in TEMPLATE_WORDS:
        if w in text:
            score -= 15

    if len(re.findall(r"。", text)) < 3:
        score -= 10

    if len(text) < 120:
        score -= 10

    return max(score, 0)
