import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# ページ設定
st.set_page_config(page_title="Family English Tutor", page_icon="🎓")
st.title("Family English Tutor 🎤✨")

# --- 1. APIキーの設定 ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーを設定してください。")

# 最も安定しているモデルを指定
model = genai.GenerativeModel('gemini-1.5-flash')

# 履歴の保持
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. 使い方ガイド ---
st.info("💡 スマホのキーボードにある「マイクのマーク」を押して英語で話しかけてね！")

# --- 3. 入力部分（テキストチャット形式） ---
# これがスマホの音声入力と相性抜群です
user_input = st.chat_input("Type or use voice dictation here...")

if user_input:
    # ユーザーの入力を表示
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.spinner('先生が考えています...'):
        try:
            # AIへの送信（テキストのみなので高速・低エラー率）
            response = model.generate_content([
                "You are a friendly, encouraging English teacher. Reply in 1-2 short sentences. Keep it simple for a family.",
                user_input
            ])
            
            ai_reply = response.text
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
            ai_reply = None

# --- 4. 会話の表示と音声再生 ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
        
        # 最新のAIの返事だけを自動で喋らせる
        if msg == st.session_state.messages[-1]:
            clean_text = msg["content"].replace("\n", " ").replace('"', '\\"')
            js_code = f"""
            <script>
                var msg = new SpeechSynthesisUtterance("{clean_text}");
                msg.lang = 'en-US';
                msg.rate = 0.9;
                window.speechSynthesis.speak(msg);
            </script>
            """
            components.html(js_code, height=0)

# --- 5. アドバイス機能（任意） ---
st.divider()
if st.button("今日のアドバイスをもらう"):
    if st.session_state.messages:
        with st.spinner('分析中...'):
            advice = model.generate_content([
                "以下の会話履歴を見て、文法のアドバイスを日本語で優しく教えてください。",
                str(st.session_state.messages)
            ])
            st.success("✨ 先生からのアドバイス")
            st.write(advice.text)
