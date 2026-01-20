import streamlit as st
import google.generativeai as genai

st.title("Family English Tutor 🎤")

# APIキー設定
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーが設定されていません。")

model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# 音声入力
audio_value = st.audio_input("ここを押して話してね")

if audio_value:
    with st.spinner('先生が考えています...'):
        # 【重要】AIが読み取れる形式（Blob）にデータを包み直す
        audio_data = {
            "mime_type": "audio/wav",
            "data": audio_value.read()
        }
        
        # 先生への指示と音声データを一緒に送る
        response = model.generate_content([
            "あなたはフレンドリーな英会話講師です。今はロールプレイ中なので、アドバイスはせず会話を楽しんでください。返信は英語で短く返してください。",
            *st.session_state.messages,
            audio_data
        ])
        
        # 履歴の更新（テキストのみ保存）
        st.session_state.messages.append(f"User: (Sent an audio message)")
        st.session_state.messages.append(f"Teacher: {response.text}")
    
    st.subheader("Teacher:")
    st.write(response.text)

st.divider()

# アドバイスボタン
if st.button("今日の英会話のアドバイスをもらう"):
    if len(st.session_state.messages) > 0:
        with st.spinner('アドバイスをまとめています...'):
            advice_res = model.generate_content([
                "これまでの会話の履歴を見て、文法ミスやより自然な言い回しを日本語で優しく教えてください。",
                str(st.session_state.messages)
            ])
            st.success("✨ 先生からのアドバイス")
            st.write(advice_res.text)
    else:
        st.warning("まずは会話を始めてみてね！")
