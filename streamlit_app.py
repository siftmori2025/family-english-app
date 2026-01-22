import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="Family English Tutor", page_icon="🎓")
st.title("Family English Tutor 🎤✨")

# APIキー設定
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーをSecretsに設定してください。")

# 2.0 Flash を指定
model = genai.GenerativeModel('gemini-2.0-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 429回避：二重送信防止用のフラグ ---
if "processing" not in st.session_state:
    st.session_state.processing = False

user_input = st.chat_input("Type here or use keyboard mic...", disabled=st.session_state.processing)

if user_input and not st.session_state.processing:
    st.session_state.processing = True
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 即座に画面を更新して「考えています」を出す
    st.rerun()

# メッセージの表示
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# AIの返信処理
if st.session_state.processing:
    with st.chat_message("assistant"):
        with st.spinner('Thinking...'):
            try:
                # ユーザーの最後の発言を取得
                last_user_msg = st.session_state.messages[-1]["content"]
                
                # AI送信
                response = model.generate_content([
                    "You are a friendly English teacher. Reply in 1 very short sentence.",
                    last_user_msg
                ])
                
                ai_reply = response.text
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                st.write(ai_reply)

                # 音声再生
                clean_text = ai_reply.replace('"', '\\"')
                js = f"<script>var m=new SpeechSynthesisUtterance('{clean_text}');m.lang='en-US';window.speechSynthesis.speak(m);</script>"
                components.html(js, height=0)
                
            except Exception as e:
                if "429" in str(e):
                    st.error("⚠️ Googleの無料枠がいっぱいです。30秒〜1分ほど完全に何もしないで待ってから、ページをリロードしてね。")
                else:
                    st.error(f"Error: {e}")
            
            # 処理終了
            st.session_state.processing = False
            # 最後に1回だけ画面更新
            st.rerun()
