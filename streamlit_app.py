import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

st.title("Family English Tutor 🎤")

# --- 1. APIキーの設定 ---
if "GOOGLE_API_KEY" in st.secrets:
    # 接続を初期化
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーをSecretsに設定してください。")

# --- 2. モデルの指定（2026年最新のフルネーム形式） ---
# 404エラーを避けるため、最も確実に存在する「latest」を指定します
try:
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
except:
    # 万が一上記がダメな場合の予備
    model = genai.GenerativeModel('gemini-1.5-flash')

# --- 3. アプリの動作 ---
if "messages" not in st.session_state:
    st.session_state.messages = []

audio_value = st.audio_input("ここを押して話してね")

if audio_value:
    with st.spinner('Waiting for AI teacher...'):
        try:
            # 音声データを送信
            response = model.generate_content([
                "You are a friendly English teacher. Reply in 1 short sentence.",
                {"mime_type": "audio/wav", "data": audio_value.getvalue()}
            ])
            
            # 返答を表示
            st.write(f"Teacher: {response.text}")
            
            # 音声を再生（JavaScript）
            clean_text = response.text.replace('"', '\\"')
            js_code = f"<script>var m=new SpeechSynthesisUtterance('{clean_text}');m.lang='en-US';window.speechSynthesis.speak(m);</script>"
            components.html(js_code, height=0)
            
        except Exception as e:
            # ここで404が出る場合は、APIキー自体の権限エラーです
            st.error(f"接続エラー: {e}")
