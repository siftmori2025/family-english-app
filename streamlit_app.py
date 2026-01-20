import streamlit as st
import google.generativeai as genai

st.title("Family English Tutor 🎤")
st.write("ボタンを押して英語で話してね！終わったらアドバイスボタンを押してね。")

# APIキー設定
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーが設定されていません。")

model = genai.GenerativeModel('gemini-1.5-flash')

# 会話履歴を保存する仕組み
if "messages" not in st.session_state:
    st.session_state.messages = []

# 音声入力
audio_value = st.audio_input("ここを押して話してね")

if audio_value:
    with st.spinner('先生が考えています...'):
        # 先生への指示（会話モード）
        response = model.generate_content([
            "あなたはフレンドリーな英会話講師です。ホテルの受付や道案内の役になりきってください。今はまだアドバイスはせず、会話を楽しんでください。1回の返信は短く。 ",
            *st.session_state.messages, # 過去の会話を覚えさせる
            audio_value
        ])
        st.session_state.messages.append(f"User: {audio_value}") # 履歴に追加
        st.session_state.messages.append(f"Teacher: {response.text}")
    
    st.subheader("Teacher:")
    st.write(response.text)

st.divider() # 区切り線

# 【ここが追加ポイント】アドバイスボタン
if st.button("今日の英会話のアドバイスをもらう"):
    if len(st.session_state.messages) > 0:
        with st.spinner('アドバイスをまとめています...'):
            advice_query = "これまでの会話を振り返って、文法の間違いや、より自然な言い回しを日本語で優しく解説してください。"
            advice_res = model.generate_content([advice_query, str(st.session_state.messages)])
            st.success("✨ 先生からのアドバイス")
            st.write(advice_res.text)
    else:
        st.warning("まずは会話を始めてみてね！")
