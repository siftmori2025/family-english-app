import streamlit as st
import google.generativeai as genai

st.title("Family English Tutor 🎤")

# APIキー設定
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーをSecretsに設定してください。")

# --- 404エラーを絶対に回避するためのモデルロード ---
@st.cache_resource
def get_working_model():
    # 2026年現在、利用可能な可能性が高いモデル名を順番に試します
    candidates = [
        'models/gemini-1.5-flash',
        'models/gemini-1.5-flash-latest',
        'models/gemini-2.0-flash',
        'gemini-1.5-flash'
    ]
    for name in candidates:
        try:
            m = genai.GenerativeModel(name)
            # 接続テスト（これを通れば本物）
            m.generate_content("Hi")
            return m
        except:
            continue
    return None

model = get_working_model()

if model is None:
    st.error("GoogleのAIに接続できません。APIキーの有効化が完了していないか、名前が変更されています。")
# ----------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

audio_value = st.audio_input("ここを押して話してね")

if audio_value:
    with st.spinner('先生が考えています...'):
        try:
            # 音声データを送信可能な形式に変換
            audio_part = {
                "mime_type": "audio/wav",
                "data": audio_value.getvalue()
            }
            
            # 会話の実行
            response = model.generate_content([
                "You are a friendly English teacher. Roleplay. Keep it short.",
                *st.session_state.messages,
                audio_part
            ])
            
            st.session_state.messages.append(f"User: (Voice)")
            st.session_state.messages.append(f"Teacher: {response.text}")
            
            st.subheader("Teacher:")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"エラー: {e}")

st.divider()
if st.button("アドバイスをもらう"):
    if st.session_state.messages:
        advice = model.generate_content(["今の会話の添削を日本語でして", str(st.session_state.messages)])
        st.write(advice.text)
