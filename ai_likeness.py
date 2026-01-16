import re

# よくある「AI寄り」定型表現
TEMPLATE_WORDS = [
    "ご利用いただきありがとうございます",
    "貴重なご意見",
    "今後ともよろしく",
    "申し訳ございませんでした",
    "心より感謝申し上げます"
]

def calc_ai_likeness(text: str) -> int:
    """
    AIっぽさスコア
    100 = 理想 ではなく「このレビューに対して適合している状態」
    """

    score = 100

    # ① 定型表現への依存
    for w in TEMPLATE_WORDS:
        if w in text:
            score -= 8  # 強すぎない減点

    # ② 文の長さ（短すぎる＝情報不足）
    length = len(text)
    if length < 80:
        score -= 12
    elif length < 120:
        score -= 6

    # ③ 文の構造（「。」の数）
    sentences = re.findall(r"。", text)
    if len(sentences) <= 1:
        score -= 10
    elif len(sentences) == 2:
        score -= 4

    # ④ 同じ言い回しの繰り返し（軽い検知）
    repeats = re.findall(r"(ありがとう|申し訳)", text)
    if len(repeats) >= 3:
        score -= 6

    return max(min(score, 100), 0)
