import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

st.title("Family English Tutor 🎤")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーを設定してください。")

# 安全設定を「すべて許可」に近く設定（エラー回避のため）
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel("gemini-1.5-flash", safety_settings=safety_settings)

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
            response = model.generate_content([
                "You are a friendly English teacher. Reply in short English (1 sentence).",
                *st.session_state.messages,
                content
            ])
            
            # 【修正点】AIが空っぽで返してきた場合のチェック
            if response.candidates and response.candidates[0].content.parts:
                res_text = response.text
                st.session_state.messages.append({"role": "user", "parts": ["(Voice)" if audio_value else text_input]})
                st.session_state.messages.append({"role": "model", "parts": [res_text]})
                
                st.subheader("Teacher:")
                st.write(res_text)

                clean_text = res_text.replace("\n", " ").replace('"', '\\"')
                js_code = f"<script>var msg = new SpeechSynthesisUtterance('{clean_text}'); msg.lang = 'en-US'; window.speechSynthesis.speak(msg);</script>"
                components.html(js_code, height=0)
            else:
                st.warning("先生がうまく聞き取れなかったみたい。もう一度ゆっくり喋ってみてね！")
            
        except Exception as e:
            st.error(f"エラー: {e}")
