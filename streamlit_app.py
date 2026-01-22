import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

st.set_page_config(page_title="Family English Tutor")
st.title("Family English Tutor 🎤")

# --- 1. APIキーの設定 ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("SecretsにAPIキーを設定してください。")

# --- 2. モデルの指定（2.0 Flash を使用） ---
# 1.5で404が出る場合は、2.0を指定するのが2026年の正解です
model = genai.GenerativeModel('gemini-2.0-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. 動作部分 ---
audio_value = st.audio_input("話しかけてね")

if audio_value:
    with st.spinner('Thinking...'):
        try:
            # 音声データを送信
            response = model.generate_content([
                "You are a friendly English teacher. Reply in 1 short sentence.",
                {"mime_type": "audio/wav", "data": audio_value.getvalue()}
            ])
            
            # 返答を表示
            st.subheader("Teacher:")
            st.write(response.text)
            
            # 音声を再生（JavaScriptでブラウザ音声を呼び出し）
            clean_text = response.text.replace('"', '\\"')
            js_code = f"<script>var m=new SpeechSynthesisUtterance('{clean_text}');m.lang='en-US';window.speechSynthesis.speak(m);</script>"
            components.html(js_code, height=0)
            
        except Exception as e:
            # まだ404が出る場合は、APIキーが有効になるまで数分待つ必要があります
            st.error(f"接続エラー: {e}")
            if "404" in str(e):
                st.info("APIキーを新プロジェクトで作ったばかりの場合、有効化まで3〜5分かかることがあります。少し待ってリロードしてください。")
