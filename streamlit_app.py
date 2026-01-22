import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

st.title("Family English Tutor 🎤")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーを設定してください。")

# --- 429対策：最も制限が緩く、無料枠に強い 8B モデルを指定 ---
model = genai.GenerativeModel('gemini-1.5-flash-8b')

if "messages" not in st.session_state:
    st.session_state.messages = []

# 音声入力（クリックして録音を開始し、完了したら送る形式）
audio_value = st.audio_input("ここを押して英語で話してね")

if audio_value:
    # 前回の送信と同じデータなら送らない（429対策）
    if "last_audio" not in st.session_state or st.session_state.last_audio != audio_value.getvalue():
        with st.spinner('先生が考えています...'):
            try:
                # 音声データを送信
                response = model.generate_content([
                    "You are a friendly English teacher. Reply in 1 very short sentence.",
                    {"mime_type": "audio/wav", "data": audio_value.getvalue()}
                ])
                
                # 成功したらデータを記録
                st.session_state.last_audio = audio_value.getvalue()
                
                res_text = response.text
                st.subheader("Teacher:")
                st.write(res_text)

                # 音声再生
                clean_text = res_text.replace("\n", " ").replace('"', '\\"')
                js_code = f"<script>var m=new SpeechSynthesisUtterance('{clean_text}');m.lang='en-US';window.speechSynthesis.speak(m);</script>"
                components.html(js_code, height=0)
                
            except Exception as e:
                if "429" in str(e):
                    st.warning("⚠️ 先生が少し混み合っています。10秒だけ待ってから、もう一度ボタンを押してみてね！")
                else:
                    st.error(f"エラー: {e}")

st.divider()
st.caption("※無料版のため、連続で話しすぎるとお休みが必要になることがあります。")
