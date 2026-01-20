import streamlit as st
import google.generativeai as genai

st.title("Family English Tutor 🎤")

# --- 設定 ---
# APIキーを読み込む
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーが未設定です。Streamlit CloudのSettingsから設定してください。")

# モデル名を一番確実なものに固定
model = genai.GenerativeModel('gemini-2.0-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 音声入力 ---
audio_value = st.audio_input("ここを押して話してね")

if audio_value:
    with st.spinner('先生が考えています...'):
        try:
            # 音声データを準備
            audio_content = {
                "mime_type": "audio/wav",
                "data": audio_value.getvalue()
            }
            
            # AIへのメッセージ送信
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
            st.error(f"エラーが発生しました: {e}")

# --- アドバイスボタン ---
st.divider()
if st.button("アドバイスをもらう"):
    if st.session_state.messages:
        advice = model.generate_content([
            "これまでの会話を振り返り、改善点を日本語で優しく教えてください。",
            str(st.session_state.messages)
        ])
        st.success("✨ 先生のアドバイス")
        st.write(advice.text)
