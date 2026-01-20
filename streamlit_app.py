import streamlit as st
import google.generativeai as genai

st.title("Family English Tutor 🎤")

# APIキー設定
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーが設定されていません。")

# モデルの設定（最新の gemini-1.5-flash または gemini-2.0-flash などが安定しています）
# Gemini 3 がエラーになる場合はここを 'gemini-1.5-flash' に戻してみてください
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# 音声入力
audio_value = st.audio_input("ここを押して話してね")

if audio_value:
    with st.spinner('先生が聞いています...'):
        try:
            # 【解決策】最もシンプルなデータ形式でAIに渡します
            audio_data = {
                "mime_type": "audio/wav",
                "data": audio_value.getvalue() # read()ではなくgetvalue()を使うのがStreamlitのコツです
            }
            
            prompt = "You are a friendly English teacher. Reply in short English. If the user mentions a situation like 'hotel' or 'directions', play along."
            
            # AIに送信
            response = model.generate_content([prompt, audio_data])
            
            st.session_state.messages.append(f"User: (Voice message)")
            st.session_state.messages.append(f"Teacher: {response.text}")
            
            st.subheader("Teacher:")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
