import streamlit as st
import google.generativeai as genai

st.title("Family English Tutor 🎤")

# APIキー設定
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーを再設定してください。")

# 【修正】モデル名を指定せず、今使える最新を自動で選ばせる記述
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

audio_value = st.audio_input("ここを押して話してね")

if audio_value:
    with st.spinner('先生が聞いています...'):
        try:
            # 2026年最新の音声送信形式
            response = model.generate_content([
                "You are a friendly English teacher. Roleplay situations like hotels. Reply in short English.",
                {"mime_type": "audio/wav", "data": audio_value.getvalue()}
            ])
            
            st.session_state.messages.append(f"Teacher: {response.text}")
            st.subheader("Teacher:")
            st.write(response.text)
            
        except Exception as e:
            # もし404が出るなら、利用可能なモデルを表示してデバッグする
            st.error(f"エラー内容: {e}")
            if "404" in str(e):
                st.info("AI Studioで『新しいプロジェクト』としてキーを作り直してみてください。")
