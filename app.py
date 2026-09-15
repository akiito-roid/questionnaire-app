from datetime import datetime
import pandas as pd
import streamlit as st

st.title("SPARK山中湖_帰りの出発時間アンケート（9/23）")
st.write("出発時間の希望を教えてください。")

# --- セッションステート（アプリ起動中のメモリ）を使ってデータを保持する ---
# 初回起動時のみ、空のDataFrame（または初期データ）を作成
if "responses" not in st.session_state:
  st.session_state.responses = pd.DataFrame(
      columns=["名前", "出発時間", "送信日時"]
  )

# ユーザー名の入力
user_name = st.text_input("あなたの名前（ニックネーム可）")

options = [
    "15時出発（池袋・渋谷着: 17時頃の目安）",
    "16時出発（池袋・渋谷着: 18時頃の目安）",
    "17時出発（池袋・渋谷着: 19時頃の目安）",
    "18時出発（池袋・渋谷着: 20時頃の目安）",
    "その他・未定",
]

if user_name:
  choice = st.radio("山中湖からの出発時間を選んでね", options)

  if st.button("回答を送信する"):
    # 新しい回答をデータフレームとして作成
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = pd.DataFrame(
        [{"名前": user_name, "出発時間": choice, "送信日時": now_time}]
    )

    # 既存の回答リストに追加
    st.session_state.responses = pd.concat(
        [st.session_state.responses, new_row], ignore_index=True
    )

    st.success(
        f"【送信完了】{user_name} さんの「{choice}」を登録しました！"
    )
    st.balloons()
else:
  st.warning("まずは名前を入力してください。")

# --- 現在の回答状況一覧（全員にリアルタイム共有） ---
st.subheader("📊 現在の回答状況一覧")

df = st.session_state.responses

if not df.empty:
  # 同じ名前の人が重複して送信した場合に最新を優先したい場合は drop_duplicates を使うこともできますが、
  # 今回はシンプルに全員分の履歴を表示します
  st.dataframe(df, use_container_width=True)
  st.write(f"現在の回答者数: **{len(df)}人** / 13人")
else:
  st.info("まだ回答はありません。最初の回答者になってね！")