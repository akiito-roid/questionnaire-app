from datetime import datetime
import os
import pandas as pd
import streamlit as st

st.title("SPARK山中湖_出発時間アンケート（9/23）")
st.write("出発時間の希望を教えてください。")

# データ保存用のCSVファイル名
CSV_FILE = "responses.csv"


# データを読み込む関数
def load_data():
  if os.path.exists(CSV_FILE):
    return pd.read_csv(CSV_FILE)
  else:
    # ファイルがなければ空のDataFrameを作成
    return pd.DataFrame(columns=["名前", "出発時間", "送信日時"])


# データを保存する関数
def save_data(df):
  df.to_csv(CSV_FILE, index=False)


# 現在のデータをロード
df = load_data()

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
    # 新しい回答データを作成
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = pd.DataFrame(
        [{"名前": user_name, "出発時間": choice, "送信日時": now_time}]
    )

    # 既存データに追加（同じ名前ですでに回答している場合は最新で上書き、または追加）
    df = pd.concat([df, new_row], ignore_index=True)

    # サーバー上のCSVファイルに保存
    save_data(df)

    st.success(
        f"【送信完了】{user_name} さんの「{choice}」を登録しました！"
    )
    st.balloons()
    # 画面を再読み込みして最新の表を表示
    st.rerun()

else:
  st.warning("まずは名前を入力してください。")

# --- 現在の回答状況一覧（全員に共有） ---
st.subheader("📊 現在の回答状況一覧")

# 最新のCSVデータを再読み込みして表示
current_df = load_data()

if not current_df.empty:
  st.dataframe(current_df, use_container_width=True)
  st.write(f"現在の回答者数: **{len(current_df)}人** / 13人")
else:
  st.info("まだ回答はありません。最初の回答者になってね！")