import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

st.set_page_config(page_title="Voice English Tutor", layout="centered")
st.title("English Tutor (Hybrid Mode) 🎤")

# APIキー設定
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.0-flash')
else:
    st.error("APIキーを設定してください。")

# --- ブラウザ側で「聞き取り」と「送信」を行うJavaScript ---
# AIに直接音声を送らないため、429エラーが激減します
st_js = """
<script>
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'en-US';
recognition.interimResults = false;

function startListen() {
    recognition.start();
    document.getElementById('status').innerText = 'Listening...';
}

recognition.onresult = (event) => {
    const text = event.results[0][0].transcript;
    document.getElementById('status').innerText = 'Sending: ' + text;
    // Streamlitにテキストを渡す
    const btn = window.parent.document.querySelector('textarea');
    const nativeValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
    nativeValueSetter.call(btn, text);
    btn.dispatchEvent(new Event('input', { bubbles: true }));
    // エンターキーをシミュレート
    const ke = new KeyboardEvent('keydown', { bubbles: true, cancelable: true, keyCode: 13 });
    btn.dispatchEvent(ke);
};
</script>
<button onclick="startListen()" style="padding:10px 20px; border-radius:10px; background-color:#FF4B4B; color:white; border:none; width:100%; font-size:20px;">
    🎤 Click to Talk (English)
</button>
<div id="status" style="margin-top:10px; color:gray; font-size:14px;"></div>
"""

components.html(st_js, height=120)

# --- Streamlit側の処理（テキストのみ受取） ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# 受信用の隠し入力欄（JSからここに値が入る）
user_input = st.chat_input("Recognized text will appear here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        try:
            # テキスト送信は非常に軽量なので429エラーに強い
            response = model.generate_content(f"Reply in 1 short sentence: {user_input}")
            ai_reply = response.text
            st.write(ai_reply)
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
            # ブラウザの音声合成で喋らせる（これも無料・無制限）
            clean_text = ai_reply.replace('"', '\\"')
            components.html(f"""
                <script>
                var m = new SpeechSynthesisUtterance("{clean_text}");
                m.lang = 'en-US';
                window.speechSynthesis.speak(m);
                </script>
            """, height=0)
        except Exception as e:
            st.error(f"Error: {e}")
