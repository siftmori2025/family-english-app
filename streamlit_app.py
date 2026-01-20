import streamlit as st
import google.generativeai as genai

st.title("Family English Tutor 🎤")

# APIキー設定
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーが未設定です。")

# 【ここを1.5に固定！】
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# 音声入力
audio_value = st.audio_input("ここを押して話してね")

if audio_value:
    with st.spinner('先生が考えています...'):
        try:
            # 音声データを準備
            audio_content = {
                "mime_type": "audio/wav",
                "data": audio_value.getvalue()
            }
            
            # AIに送信
            response = model.generate_content([
                "You are a friendly English teacher. Roleplay situations like hotels or directions. Reply in short English.",
                *st.session_state.messages,
                audio_content
            ])
            
            # 履歴に保存
            st.session_state.messages.append(f"User: (Voice)")
            st.session_state.messages.append(f"Teacher: {response.text}")
            
            st.subheader("Teacher:")
            st.write(response.text)
            
        except Exception as e:
            # ここで制限エラー(429)が出た場合は、時間を置くしかありません
            st.error(f"エラーが発生しました: {e}")

st.divider()
if st.button("アドバイスをもらう"):
    if st.session_state.messages:
        advice = model.generate_content([
            "これまでの会話を振り返り、改善点を日本語で教えてください。",
            str(st.session_state.messages)
        ])
        st.write(advice.text)
