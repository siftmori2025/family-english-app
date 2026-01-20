import streamlit as st
import google.generativeai as genai
# ここを修正：明示的に types をインポートします
from google.generativeai import types

st.title("Family English Tutor (Gemini 3) 🎤")

# APIキー設定
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーが設定されていません。")

# モデルの設定
model = genai.GenerativeModel('gemini-3-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# 音声入力
audio_value = st.audio_input("ここを押して話してね")

if audio_value:
    with st.spinner('Gemini 3 が聞き取っています...'):
        try:
            # 【修正点】確実に Blob を作成するための記述
            audio_data = genai.types.Blob(
                mime_type='audio/wav',
                data=audio_value.read()
            )
            
            prompt = "You are a friendly English teacher. Reply in short English. If the user mentions a situation like 'hotel' or 'directions', play along."
            
            # AIに送信
            response = model.generate_content([prompt, audio_data])
            
            st.session_state.messages.append(f"User: (Voice message)")
            st.session_state.messages.append(f"Teacher: {response.text}")
            
            st.subheader("Teacher:")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
