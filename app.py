from streamlit_gsheets import GSheetsConnection
import streamlit as st

st.title("SPARK山中湖_帰りの出発時間アンケート（9/23）")
st.write("出発時間の希望を教えてください。")

# Googleスプレッドシートへの接続
conn = st.connection("gsheets", type=GSheetsConnection)

# 既存データの読み込み
existing_data = conn.read(ttl=0)

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
    # 新しい回答データ
    new_data = {"名前": [user_name], "出発時間": [choice]}
    # スプレッドシートに追記する処理（イメージ）
    # updated_df = pd.concat([existing_data, new_row], ignore_index=True)
    # conn.update(data=updated_df)
    st.success(f"【送信完了】{user_name} さんは「{choice}」で登録しました！")
    st.balloons()

# 現在の回答状況を全員に見せる
st.subheader("📊 現在の回答状況一覧")
if not existing_data.empty:
  st.dataframe(existing_data)
else:
  st.info("まだ回答はありません。一番乗りで送信してね！")