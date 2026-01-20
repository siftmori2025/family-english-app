import streamlit as st
import google.generativeai as genai

st.title("Family English Tutor 🎤")

# APIキー設定
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーが設定されていません。Settings > Secretsを確認してください。")

# --- モデルの読み込み（エラー回避ロジック） ---
@st.cache_resource
def load_model():
    # 2026年現在、最も確実に動く候補を順番に試します
    model_names = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-3-flash']
    for name in model_names:
        try:
            m = genai.GenerativeModel(name)
            # テスト送信して確認
            m.generate_content("test")
            return m
        except:
            continue
    return None

model = load_model()

if model is None:
    st.error("利用可能なAIモデルが見つかりませんでした。APIキーが正しいか、Google AI Studioで有効か確認してください。")
# --------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# 音声入力
audio_value = st.audio_input("ここを押して話してね")

if audio_value:
    with st.spinner('先生が聞いています...'):
        try:
            # 音声データをAIが受け取れる辞書形式に
            audio_data = {
                "mime_type": "audio/wav",
                "data": audio_value.getvalue()
            }
            
            prompt = "You are a friendly English teacher. Roleplay based on situations like 'hotel' or 'directions'. Keep it short."
            
            # 履歴を含めて送信
            response = model.generate_content([prompt, *st.session_state.messages, audio_data])
            
            st.session_state.messages.append(f"User: (Voice message)")
            st.session_state.messages.append(f"Teacher: {response.text}")
            
            st.subheader("Teacher:")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"会話中にエラーが発生しました: {e}")

st.divider()

if st.button("今日の英会話のアドバイスをもらう"):
    if len(st.session_state.messages) > 0:
        with st.spinner('分析中...'):
            advice_res = model.generate_content([
                "これまでの会話履歴を分析して、間違いを日本語で優しく教えてください。",
                str(st.session_state.messages)
            ])
            st.success("✨ 先生からのアドバイス")
            st.write(advice_res.text)
