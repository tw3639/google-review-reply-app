import streamlit as st
from prompt_builder import build_prompt
from openai_client import generate_reply
from ai_likeness import calc_ai_likeness
from csv_batch import csv_batch_generate

# -----------------------------
# ページ設定
# -----------------------------
st.set_page_config(
    page_title="Review Reply QA",
    layout="wide"
)

# -----------------------------
# タイトル & 説明
# -----------------------------
st.title("Review Reply QA")

st.markdown("""
Googleレビューへの返信文を、★評価ごとの方針に基づいて生成するツールです。  
定型的なAI返信を避け、**人が書いたように自然に見える表現**を重視しています。
""")

with st.expander("このツールについて"):
    st.markdown("""
    **主な特徴**
    - ★1〜★5で返信の目的・トーンを明確に分離
    - レビュー文の内容から返信スタイルを調整
    - 定型文を避けた自然な文章生成
    - 「AIっぽさ」を参考スコアとして可視化

    ※ 自動生成された返信文は、必ず内容をご確認のうえご利用ください。
    """)

st.divider()

# -----------------------------
# モード選択
# -----------------------------
mode = st.radio(
    "モード選択",
    ["単体レビュー", "CSV一括生成（軽量）"]
)

# =====================================================
# 単体レビュー
# =====================================================
if mode == "単体レビュー":
    st.subheader("① レビュー入力")

    review = st.text_area(
        "レビュー本文",
        height=180,
        placeholder="ここにGoogleレビューの本文を貼り付けてください"
    )

    rating = st.selectbox(
        "★評価",
        [1, 2, 3, 4, 5]
    )

    st.divider()

    st.subheader("② 返信生成")

    if st.button("返信を生成する"):
        if not review.strip():
            st.error("レビュー本文を入力してください。")
        else:
            prompt, meta = build_prompt(review, rating)

            with st.spinner("返信文を生成中..."):
                reply = generate_reply(
                    prompt,
                    temperature=meta["temperature"]
                )

            st.subheader("生成された返信文（編集可）")

            edited_reply = st.text_area(
                "必要に応じて表現を調整してください",
                reply,
                height=240
            )

            # -----------------------------
            # AIっぽさスコア表示（編集後）
            # -----------------------------
            score = calc_ai_likeness(edited_reply)

            st.markdown("### 🧪 AIっぽさスコア")
            st.caption(
                "このスコアは、文章の中に含まれる**定型的・機械的に見えやすい表現の傾向**を"
                "独自基準で数値化したものです。"
            )

            st.progress(score / 100)
            st.markdown(f"**スコア：{score} / 100**")

            with st.expander("AIっぽさスコアの考え方（必ずお読みください）"):
                st.markdown("""
                このスコアは **品質・良し悪しを判定するものではありません**。

                - 高スコアでも、業務上まったく問題なく使える文章は多く存在します
                - 低スコアでも、必ずしも「正解の表現」というわけではありません

                あくまで  
                **「自分で手直しした結果、定型AI感がどう変化したかを確認するための補助指標」**  
                としてご活用ください。
                """)

# =====================================================
# CSV一括生成（軽量）
# =====================================================
elif mode == "CSV一括生成（軽量）":
    st.subheader("① CSVアップロード")

    st.markdown("""
    CSVファイルに複数のレビューをまとめて、返信文を一括生成します。  
    **検証・社内確認用途向けの軽量モード**です。
    """)

    with st.expander("CSVの形式例"):
        st.markdown("""
        以下のような形式のCSVをご用意ください。

        ```csv
        review,rating
        とても丁寧な接客でした。,5
        料理の提供が遅かったです。,2
        普通でした。,3
        ```

        - `review`：レビュー本文  
        - `rating`：★評価（1〜5の数値）
        """)

    uploaded = st.file_uploader(
        "CSVをアップロード（review,rating の列が必要）",
        type="csv"
    )

    if uploaded:
        with st.spinner("CSV一括生成中..."):
            df = csv_batch_generate(uploaded)

        st.subheader("生成結果")
        st.dataframe(df, use_container_width=True)

        st.caption(
            "※ 一括生成ではAPI使用量が増えるため、件数にはご注意ください。"
        )
