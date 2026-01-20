import streamlit as st
import google.generativeai as genai

st.title("Family English Tutor (Gemini 3) 🎤")

# APIキー設定
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーを設定してください。")

model_name = "gemini-3-flash-preview"
model = genai.GenerativeModel(model_name)

if "messages" not in st.session_state:
    st.session_state.messages = []

audio_value = st.audio_input("ここを押して話してね")

if audio_value:
    with st.spinner('Gemini 3 が考えています...'):
        try:
            audio_data = {
                "mime_type": "audio/wav",
                "data": audio_value.getvalue()
            }
            
            # 【ポイント】AIに「音声で答えられるように短く返して」と指示を微調整
            response = model.generate_content([
                "You are a friendly English teacher. Reply in short English (1-2 sentences).",
                *st.session_state.messages,
                audio_data
            ])
            
            st.session_state.messages.append(f"User: (Voice)")
            st.session_state.messages.append(f"Teacher: {response.text}")
            
            st.subheader("Teacher:")
            st.write(response.text)

            # --- ここから音声読み上げ機能を追加 ---
            # Googleの標準的な読み上げ機能（TTS）を呼び出します
            st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={response.text.replace(' ', '%20')}&tl=en&client=tw-ob", format="audio/mp3")
            # ------------------------------------
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

st.divider()
if st.button("アドバイスをもらう"):
    if st.session_state.messages:
        advice = model.generate_content(["今の会話の添削を日本語でして", str(st.session_state.messages)])
        st.write(advice.text)
