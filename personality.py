def classify_personality(review: str) -> str:
    if any(w in review for w in ["詳しく", "具体的", "細かく"]):
        return "情報重視タイプ"
    if any(w in review for w in ["雰囲気", "楽しい", "気持ち"]):
        return "体験重視タイプ"
    if any(w in review for w in ["早い", "無駄", "効率"]):
        return "効率重視タイプ"
    return "対話志向タイプ"
