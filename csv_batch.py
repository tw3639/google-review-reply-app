import pandas as pd
from prompt_builder import build_prompt
from openai_client import generate_reply
from ai_likeness import calc_ai_likeness

def csv_batch_generate(file):
    df = pd.read_csv(file)
    results = []

    for _, row in df.iterrows():
        prompt, meta = build_prompt(row["review"], int(row["rating"]))
        reply = generate_reply(prompt, meta["temperature"])
        score = calc_ai_likeness(reply)

        results.append({
            "review": row["review"],
            "rating": row["rating"],
            "reply": reply,
            "ai_likeness": score
        })

    return pd.DataFrame(results)
