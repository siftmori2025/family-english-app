import streamlit as st
import google.generativeai as genai

st.title("Family English Tutor 🎤")

# APIキー設定
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーが設定されていません。")

# 【修正ポイント】モデル名を最新の指定に変更
# もしこれでもエラーが出る場合は 'gemini-1.5-flash-latest' もお試しください
model = genai.GenerativeModel('gemini-1.5-flash-latest')

if "messages" not in st.session_state:
    st.session_state.messages = []

# 音声入力
audio_value = st.audio_input("ここを押して話してね")

if audio_value:
    with st.spinner('先生が考えています...'):
        try:
            # 音声データの変換
            audio_data = {
                "mime_type": "audio/wav",
                "data": audio_value.read()
            }
            
            # 先生への指示
            response = model.generate_content([
                "You are a friendly English teacher. Please roleplay based on the user's situation (hotel, directions, etc.). Keep replies short and in English. Do not give advice yet.",
                *st.session_state.messages,
                audio_data
            ])
            
            # 履歴の更新
            st.session_state.messages.append(f"User: (Voice Message)")
            st.session_state.messages.append(f"Teacher: {response.text}")
            
            st.subheader("Teacher:")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
            st.info("モデル名を 'gemini-1.5-flash-latest' に書き換えると直る場合があります。")

st.divider()

# アドバイスボタン
if st.button("今日の英会話のアドバイスをもらう"):
    if len(st.session_state.messages) > 0:
        with st.spinner('アドバイスをまとめています...'):
            advice_res = model.generate_content([
                "これまでの会話履歴を分析して、文法の間違いや、より自然な言い回しを日本語で優しく教えてください。",
                str(st.session_state.messages)
            ])
            st.success("✨ 先生からのアドバイス")
            st.write(advice_res.text)
    else:
        st.warning("まずは会話を始めてみてね！")
