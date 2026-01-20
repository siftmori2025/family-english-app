import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

st.title("Family English Tutor (Gemini 3) 🎤")

# APIキー設定
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーを設定してください。")

model_name = "gemini-3-flash-preview"
model = genai.GenerativeModel(model_name)

# 履歴を保存する場所（テキストのみを保存するようにします）
if "messages" not in st.session_state:
    st.session_state.messages = []

audio_value = st.audio_input("ここを押して話してね")

if audio_value:
    with st.spinner('Gemini 3 が考えています...'):
        try:
            # 今回の音声データ
            audio_data = {
                "mime_type": "audio/wav",
                "data": audio_value.getvalue()
            }
            
            # AIにこれまでの「テキスト履歴」と「今回の音声」を渡す
            response = model.generate_content([
                "You are a friendly English teacher. Reply in short English (1-2 sentences).",
                *st.session_state.messages,
                audio_data
            ])
            
            # 【重要】履歴には「何と言ったか（音声）」ではなく、AIの返答など「テキスト」だけを蓄積する
            # ユーザーが喋ったという事実だけをテキストで残す
            st.session_state.messages.append({"role": "user", "parts": ["(The user spoke in English)"]})
            st.session_state.messages.append({"role": "model", "parts": [response.text]})
            
            st.subheader("Teacher:")
            st.write(response.text)

            # 音声読み上げ
            clean_text = response.text.replace("\n", " ").replace('"', '\\"')
            js_code = f"""
            <script>
                var msg = new SpeechSynthesisUtterance("{clean_text}");
                msg.lang = 'en-US';
                msg.rate = 0.9;
                window.speechSynthesis.speak(msg);
            </script>
            """
            components.html(js_code, height=0)
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

st.divider()

# アドバイスボタンの修正
if st.button("アドバイスをもらう"):
    if len(st.session_state.messages) > 0:
        with st.spinner('これまでの会話を分析中...'):
            # 履歴（テキストのみ）を渡してアドバイスをもらう
            advice_res = model.generate_content([
                "これまでの英会話のやり取りを見て、文法ミスや、より自然な表現を日本語で優しく教えてください。",
                str(st.session_state.messages)
            ])
            st.success("✨ 先生からのアドバイス")
            st.write(advice_res.text)
    else:
        st.warning("まずは会話を始めてみてね！")
