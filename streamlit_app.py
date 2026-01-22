import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="English Tutor", page_icon="🎓")
st.title("Family English Tutor 🎤✨")

# --- 1. APIキーの設定 ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーを設定してください。")

# --- 2. モデルの指定（最もエラーが起きにくい名前に固定） ---
model = genai.GenerativeModel('gemini-1.5-flash-latest')

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. 入力部分 ---
user_input = st.chat_input("Speak using your keyboard mic...")

if user_input:
    # 履歴に追加
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner('Thinking...'):
        try:
            # AIへの送信
            response = model.generate_content([
                "You are a friendly English teacher. Reply in 1 very short sentence.",
                user_input
            ])
            
            ai_reply = response.text
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
        except Exception as e:
            # 404や429が出た時のための優しいエラー表示
            if "404" in str(e):
                st.error("AI先生が見つかりません。別のモデル(gemini-2.0-flash)を試します...")
                model = genai.GenerativeModel('gemini-2.0-flash') # 自動切り替え
            elif "429" in str(e):
                st.warning("少し混み合っています。30秒だけ待ってからもう一度送ってみてね。")
            else:
                st.error(f"Error: {e}")

# --- 4. 会話の表示と音声再生 ---
for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.write(msg["content"])
        
        # AIの最新の返事だけを喋らせる
        if msg == st.session_state.messages[-1] and role == "assistant":
            clean_text = msg["content"].replace('"', '\\"')
            js = f"<script>var m=new SpeechSynthesisUtterance('{clean_text}');m.lang='en-US';window.speechSynthesis.speak(m);</script>"
            components.html(js, height=0)
