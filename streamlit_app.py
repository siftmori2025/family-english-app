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

if "messages" not in st.session_state:
    st.session_state.messages = []

# 音声入力
audio_value = st.audio_input("ここを押して話してね")

if audio_value:
    with st.spinner('Gemini 3 が考えています...'):
        try:
            # 最新の送信形式
            audio_data = {
                "mime_type": "audio/wav",
                "data": audio_value.getvalue()
            }
            
            response = model.generate_content([
                "You are a friendly English teacher. Reply in short English (1-2 sentences).",
                *st.session_state.messages,
                audio_data
            ])
            
            st.session_state.messages.append(f"User: (Voice)")
            st.session_state.messages.append(f"Teacher: {response.text}")
            
            st.subheader("Teacher:")
            st.write(response.text)

            # --- AIが自動で喋る魔法のコード ---
            # 返信テキストから余計な改行や引用符を消してJavaScriptに渡します
            clean_text = response.text.replace("\n", " ").replace('"', '\\"')
            js_code = f"""
            <script>
                var msg = new SpeechSynthesisUtterance("{clean_text}");
                msg.lang = 'en-US';
                msg.rate = 0.9; // 少しだけゆっくり
                window.speechSynthesis.speak(msg);
            </script>
            """
            components.html(js_code, height=0)
            # -------------------------------
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

st.divider()
if st.button("アドバイスをもらう"):
    if st.session_state.messages:
        advice = model.generate_content(["今の会話の添削を日本語でして", str(st.session_state.messages)])
        st.write(advice.text)
