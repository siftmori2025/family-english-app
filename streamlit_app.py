import streamlit as st
import google.generativeai as genai

st.title("Family English Tutor 🎤")

# APIキー設定
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーが設定されていません。")

model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# 【変更点】より安定した音声入力パーツに変更
audio_value = st.audio_input("ここを押して話してね")

# もし上がダメな場合、以下の「ファイルアップロード」を予備として出す
if audio_value is None:
    st.info("※マイクが反応しない場合は、スマホのボイスメモ録音ファイルを下にドラッグしてもOKです。")
    audio_value = st.file_uploader("音声ファイルをアップロード", type=['wav', 'mp3', 'm4a'])

if audio_value:
    with st.spinner('先生が考えています...'):
        response = model.generate_content([
            "あなたはフレンドリーな英会話講師です。今はロールプレイ中で、アドバイスはせず会話を楽しんでください。返信は短く。",
            *st.session_state.messages,
            audio_value
        ])
        st.session_state.messages.append(f"User (Audio attached)")
        st.session_state.messages.append(f"Teacher: {response.text}")
    
    st.subheader("Teacher:")
    st.write(response.text)

st.divider()

if st.button("今日の英会話のアドバイスをもらう"):
    if len(st.session_state.messages) > 0:
        with st.spinner('アドバイスをまとめています...'):
            advice_res = model.generate_content(["これまでの会話を日本語で優しく添削して", str(st.session_state.messages)])
            st.success("✨ 先生からのアドバイス")
            st.write(advice_res.text)
