import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

st.title("Family English Tutor 🎤")

# --- 1. APIキーの設定 ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーをSecretsに設定してください。")

# --- 2. モデルの自動選択（404対策の決定版） ---
@st.cache_resource
def get_model():
    # 2026年現在の最新候補を優先順位順に並べています
    candidates = [
        'gemini-2.0-flash', 
        'gemini-1.5-flash-8b', 
        'gemini-1.5-flash-latest',
        'gemini-1.5-flash'
    ]
    # あなたのキーで使えるモデルを一覧取得
    available = [m.name.replace('models/', '') for m in genai.list_models()]
    
    for c in candidates:
        if c in available:
            return genai.GenerativeModel(f'models/{c}')
    # どれも見つからない場合は、リストの最初にあるFlash系を探す
    for a in available:
        if 'flash' in a:
            return genai.GenerativeModel(f'models/{a}')
    return None

model = get_model()

if model is None:
    st.error("利用可能なFlashモデルが見つかりません。")
else:
    # 実際に繋がったモデルを表示（安心のため）
    st.caption(f"Connected to: {model.model_name}")

# --- 3. メイン動作 ---
audio_value = st.audio_input("ここを押して話してね")

if audio_value:
    with st.spinner('Thinking...'):
        try:
            # 音声送信
            res = model.generate_content([
                "You are a friendly English teacher. Reply in 1 short sentence.",
                {"mime_type": "audio/wav", "data": audio_value.getvalue()}
            ])
            
            st.write(f"Teacher: {res.text}")
            
            # 音声再生
            clean_text = res.text.replace('"', '\\"')
            components.html(f"<script>var m=new SpeechSynthesisUtterance('{clean_text}');m.lang='en-US';window.speechSynthesis.speak(m);</script>", height=0)
            
        except Exception as e:
            if "429" in str(e):
                st.warning("少し混み合っています。10秒待ってからもう一度話してね。")
            else:
                st.error(f"Error: {e}")
