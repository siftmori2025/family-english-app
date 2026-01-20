import streamlit as st
import google.generativeai as genai

st.title("Family English Tutor 🎤")

# APIキー設定
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーが設定されていません。")

# 【ここを修正】2026年現在、最も確実に動くモデル名の指定方法です
# 'models/' を頭に付けることで、バージョンの違いを吸収します
try:
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except:
    # 万が一上記でダメな場合の予備（最新のGemini 3など）
    model = genai.GenerativeModel('models/gemini-3-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# 音声入力
audio_value = st.audio_input("ここを押して話してね")

if audio_value:
    with st.spinner('先生が聞いています...'):
        try:
            # 音声データの変換
            audio_data = {
                "mime_type": "audio/wav",
                "data": audio_value.getvalue()
            }
            
            # 先生への指示
            response = model.generate_content([
                "You are a friendly English teacher. Roleplay based on situations like 'hotel' or 'directions'. Keep it short and easy.",
                *st.session_state.messages,
                audio_data
            ])
            
            st.session_state.messages.append(f"User: (Voice message)")
            st.session_state.messages.append(f"Teacher: {response.text}")
            
            st.subheader("Teacher:")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

st.divider()

# アドバイスボタン
if st.button("今日の英会話のアドバイスをもらう"):
    if len(st.session_state.messages) > 0:
        with st.spinner('アドバイスをまとめています...'):
            advice_res = model.generate_content([
                "これまでの会話履歴を分析して、間違いを日本語で優しく教えてください。",
                str(st.session_state.messages)
            ])
            st.success("✨ 先生からのアドバイス")
            st.write(advice_res.text)
