import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

st.title("Family English Tutor 🎤")

# --- 1. APIキーの設定 ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーをSecretsに設定してください。")

# --- 2. モデルを自動で探す（404回避の最終手段） ---
@st.cache_resource
def get_best_model():
    # 候補をすべて並べる
    candidates = [
        'gemini-1.5-flash',
        'gemini-2.0-flash',
        'gemini-3-flash-preview',
        'models/gemini-1.5-flash'
    ]
    for name in candidates:
        try:
            m = genai.GenerativeModel(name)
            # 実際に動くかテスト
            m.generate_content("Hi")
            return m
        except:
            continue
    return None

model = get_best_model()

if model is None:
    st.error("利用可能なAIが見つかりません。APIキーが新しいプロジェクトで作られたか確認してください。")
# -----------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

audio_value = st.audio_input("ここを押して話してね")
text_input = st.chat_input("またはここに英語を書いてね")

content = None
if audio_value:
    content = {"mime_type": "audio/wav", "data": audio_value.getvalue()}
elif text_input:
    content = text_input

if content:
    with st.spinner('先生が考えています...'):
        try:
            # 安全設定などは入れず、最も標準的な形で送信
            response = model.generate_content([
                "You are a friendly English teacher. Reply in short English (1 sentence).",
                *st.session_state.messages,
                content
            ])
            
            # 返信があるかチェック
            if response and response.text:
                res_text = response.text
                st.session_state.messages.append({"role": "user", "parts": ["(Voice)" if audio_value else text_input]})
                st.session_state.messages.append({"role": "model", "parts": [res_text]})
                
                st.subheader("Teacher:")
                st.write(res_text)

                # 音声読み上げ（ブラウザ標準機能）
                clean_text = res_text.replace("\n", " ").replace('"', '\\"')
                js_code = f"<script>var msg = new SpeechSynthesisUtterance('{clean_text}'); msg.lang = 'en-US'; window.speechSynthesis.speak(msg);</script>"
                components.html(js_code, height=0)
            
        except Exception as e:
            # 429（回数制限）が出たときのアナウンス
            if "429" in str(e):
                st.warning("先生が少し休憩中です。1分だけ待ってからもう一度話してね！")
            else:
                st.error(f"エラー: {e}")
