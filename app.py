from datetime import datetime
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("SPARK山中湖_帰りの出発時間アンケート（9/23）")
st.write("出発時間の希望を教えてください。")

# Googleスプレッドシートへの接続 (ttl=0 でキャッシュを無効化し、常に最新データを取得)
conn = st.connection("gsheets", type=GSheetsConnection)
existing_data = conn.read(ttl=0)

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
    # 1. 新しい行データを作成（送信日時も記録すると便利です）
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = pd.DataFrame(
        [{"名前": user_name, "出発時間": choice, "送信日時": now_time}]
    )

    # 2. 既存データと新しいデータを結合
    if existing_data.empty:
      updated_df = new_row
    else:
      updated_df = pd.concat(
          [existing_data, new_row], ignore_index=True
      )

    # 3. Googleスプレッドシートを更新
    conn.update(data=updated_df)

    st.success(
        f"【送信完了】{user_name} さんの「{choice}」を登録しました！"
    )
    st.balloons()
    # 画面を再読み込みして最新の表を表示させる
    st.rerun()

else:
  st.warning("まずは名前を入力してください。")

# --- 現在の回答状況一覧 ---
st.subheader("📊 現在の回答状況一覧")

# 最新のデータを再度読み込み
current_data = conn.read(ttl=0)

if not current_data.empty:
  st.dataframe(current_data, use_container_width=True)
  st.write(f"現在の回答者数: **{len(current_data)}人** / 13人")
else:
  st.info("まだ回答はありません。最初の回答者になってね！")