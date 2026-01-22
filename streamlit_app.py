import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

st.title("Family English Tutor 🎤")

# APIキー設定
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーをSecretsに設定してください。")

# 2026年現在、最も普及している標準名で固定
model = genai.GenerativeModel("gemini-1.5-flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

audio_value = st.audio_input("ここを押して話してね")

if audio_value:
    with st.spinner('Thinking...'):
        try:
            # 音声送信
            res = model.generate_content([
                "You are a friendly English teacher. Reply in 1 short sentence.",
                {"mime_type": "audio/wav", "data": audio_value.getvalue()}
            ])
            
            st.write(f"Teacher: {res.text}")
            
            # 音声再生
            clean_text = res.text.replace('"', '\\"')
            components.html(f"<script>var m=new SpeechSynthesisUtterance('{clean_text}');m.lang='en-US';window.speechSynthesis.speak(m);</script>", height=0)
            
        except Exception as e:
            st.error(f"Error: {e}")
