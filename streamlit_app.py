import streamlit as st
import google.generativeai as genai

st.title("Family English Tutor (Gemini 3) 🎤")

# APIキー設定
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーを設定してください。")

# 【ここが重要】画像から判明した最新のモデル名に固定します
model_name = "gemini-3-flash-preview"
model = genai.GenerativeModel(model_name)

if "messages" not in st.session_state:
    st.session_state.messages = []

# 音声入力
audio_value = st.audio_input("ここを押して話してね")

if audio_value:
    with st.spinner('Gemini 3 が考えています...'):
        try:
            # 最新の送信形式
            audio_data = {
                "mime_type": "audio/wav",
                "data": audio_value.getvalue()
            }
            
            response = model.generate_content([
                "You are a friendly English teacher. Roleplay based on situations. Keep it short.",
                *st.session_state.messages,
                audio_data
            ])
            
            st.session_state.messages.append(f"User: (Voice)")
            st.session_state.messages.append(f"Teacher: {response.text}")
            
            st.subheader("Teacher:")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

st.divider()
if st.button("アドバイスをもらう"):
    if st.session_state.messages:
        advice = model.generate_content(["今の会話の添削を日本語でして", str(st.session_state.messages)])
        st.write(advice.text)
