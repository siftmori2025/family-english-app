import streamlit as st
import google.generativeai as genai

st.title("Family English Tutor (Gemini 3 版) 🎤")

# APIキー設定
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーが設定されていません。")

# 【ここを最新に！】
# Google AI Studioの最新環境に合わせてモデル名を指定します
model = genai.GenerativeModel('gemini-3-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

audio_value = st.audio_input("ここを押して話してね")

if audio_value:
    with st.spinner('Gemini 3 が考えています...'):
        try:
            audio_data = {
                "mime_type": "audio/wav",
                "data": audio_value.read()
            }
            
            # Gemini 3 はより複雑な指示も理解できます
            response = model.generate_content([
                "You are an expert English coach using the Gemini 3 model. Help the user practice English for specific situations (hotel, asking directions). Be natural and encouraging. Keep it short.",
                *st.session_state.messages,
                audio_data
            ])
            
            st.session_state.messages.append(f"User: (Voice)")
            st.session_state.messages.append(f"Teacher: {response.text}")
            
            st.subheader("Teacher (Gemini 3):")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"モデル呼び出しエラー: {e}")
            st.info("もし 'model not found' と出る場合は 'gemini-1.5-flash' に戻すと安定します。")

st.divider()

if st.button("今日の英会話のアドバイスをもらう"):
    if len(st.session_state.messages) > 0:
        with st.spinner('Gemini 3 が分析中...'):
            advice_res = model.generate_content([
                "Gemini 3の高度な分析能力を使って、これまでの会話を日本語で優しく添削してください。",
                str(st.session_state.messages)
            ])
            st.success("✨ Gemini 3 からのアドバイス")
            st.write(advice_res.text)
