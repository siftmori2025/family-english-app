import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import time

st.title("Family English Tutor 🎤")

# APIキー設定
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーをSecretsに設定してください。")

# 2026年現在、最も安定している名前を指定
model_name = 'models/gemini-1.5-flash'
model = genai.GenerativeModel(model_name)

audio_value = st.audio_input("ここを押して話してね")

if audio_value:
    with st.spinner('AIが声を聴いています...'):
        try:
            # 音声データ送信
            # 429エラー対策として、失敗しても一度だけ自動で少し待ってリトライします
            for attempt in range(2):
                try:
                    response = model.generate_content([
                        "You are a friendly English teacher. Reply in 1 short sentence.",
                        {"mime_type": "audio/wav", "data": audio_value.getvalue()}
                    ])
                    
                    if response.text:
                        st.subheader("Teacher:")
                        st.write(response.text)
                        # 音声再生
                        clean_text = response.text.replace('"', '\\"')
                        js_code = f"<script>var m=new SpeechSynthesisUtterance('{clean_text}');m.lang='en-US';window.speechSynthesis.speak(m);</script>"
                        components.html(js_code, height=0)
                        break # 成功したらループを抜ける
                except Exception as e:
                    if "429" in str(e) and attempt == 0:
                        time.sleep(5) # 5秒だけ待って再試行
                        continue
                    raise e # 2回目もダメならエラーを表示

        except Exception as e:
            if "404" in str(e):
                st.error("接続エラー(404): モデルが見つかりません。APIキーを『New Project』で作り直してみてください。")
            elif "429" in str(e):
                st.warning("先生が混み合っています(429)。30秒ほど休んでから、もう一度話しかけてね。")
            else:
                st.error(f"エラーが発生しました: {e}")
