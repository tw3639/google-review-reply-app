import random
from personality import classify_personality

MAX_LENGTH = {
    1: 320,
    2: 300,
    3: 260,
    4: 220,
    5: 240
}

TEMPERATURE = {
    1: 0.3,
    2: 0.35,
    3: 0.45,
    4: 0.6,
    5: 0.7
}

# ==============================
# ゆらぎ表現（VARIATIONS）
# ==============================
VARIATIONS = [
    "とても嬉しく思います",
    "大変ありがたく感じます",
    "心より感謝申し上げます",
    "嬉しい限りです",
    "感謝の気持ちでいっぱいです",
    "喜びを感じております"
]

# ==============================
# 感嘆符ルール
# ==============================
def exclamation_rule(star: int, review_text: str) -> str:
    mentions_service = any(
        word in review_text
        for word in ["接客", "対応", "温か", "親切", "気配り"]
    )

    if star == 3:
        return (
            "感嘆符（！）は一切使用せず、事実と感想を淡々と受け止める、落ち着いた文体で返信してください。"
        )
    if star == 4:
        if mentions_service and random.random() < 0.3:
            return (
                "感嘆符は基本的に使用しないでください。ただし接客や人の温かさへの感謝を表す場合に限り、文末に1回自然に使用しても構いません。"
            )
        else:
            return "感嘆符は使用せず、落ち着いた丁寧な日本語表現で返信してください。"
    if star == 5:
        if random.random() < 0.5:
            return "感嘆符は多用せず、文末に1回まで使用可能です。連続使用は禁止します。"
        else:
            return "感嘆符は使用せず、穏やかで品のある喜びを表現してください。"
    # ★1・★2
    return "感嘆符は使用せず、感情や対応内容は言葉で丁寧に表現してください。"

# ==============================
# プロンプト生成
# ==============================
def build_prompt(review: str, rating: int):
    personality = classify_personality(review)
    ex_rule = exclamation_rule(rating, review)

    # パターンをランダムに選択
    pattern = random.choice(["A", "B", "C"])
    variation = random.choice(VARIATIONS)

    base = f"""
以下のGoogleレビューに対する返信文を作成してください。

【レビュー】
{review}

【返信方針】
★{rating}
パーソナリティ：{personality}
条件：
・定型文は禁止
・レビュー内容に具体的に触れる
・日本語で自然な文章
・文字数は{MAX_LENGTH[rating]}文字以内
・{ex_rule}
・文のパターン: {pattern}
・冒頭または末尾に自然に「{variation}」を使用
"""

    # 星ごとの追加条件
    if rating == 1:
        base += """
・感情ケアを最優先
・謝罪は一度だけ、過剰にしない
・「またのご来店」は禁止
"""
    elif rating == 2:
        base += """
・事実整理と実務対応を明確に
・改善姿勢を具体的に示す
"""
    elif rating == 3:
        base += """
・中立的で落ち着いたトーン
・感情に寄りすぎない
"""
    elif rating == 4:
        base += """
・簡潔で好意的
・パーソナリティを軽く反映
"""
    elif rating == 5:
        base += """
・感謝＋余韻を残す
・表現にランダム性を持たせる
"""

    return base.strip(), {
        "temperature": TEMPERATURE[rating]
    }
