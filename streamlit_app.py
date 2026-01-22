import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

st.title("English Tutor (Simple)")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.0-flash')

# 複雑な履歴管理を一度捨て、1回ごとのやり取りに特化
user_input = st.text_input("Talk to me:")

if user_input:
    try:
        # AI送信
        response = model.generate_content(f"Reply in 1 short sentence: {user_input}")
        
        # 返信を表示
        st.subheader("Teacher:")
        st.write(response.text)

        # 音声再生
        clean_text = response.text.replace('"', '\\"')
        js = f"<script>var m=new SpeechSynthesisUtterance('{clean_text}');m.lang='en-US';window.speechSynthesis.speak(m);</script>"
        components.html(js, height=0)
    except Exception as e:
        st.error(f"Error: {e}")
