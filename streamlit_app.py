import streamlit as st
import google.generativeai as genai
from google.generativeai import types # 追加

st.title("Family English Tutor (Gemini 3) 🎤")

# APIキー設定
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーが設定されていません。")

# モデルの設定
model = genai.GenerativeModel('gemini-3-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# 音声入力パーツ
audio_value = st.audio_input("ここを押して話してね")

if audio_value:
    with st.spinner('Gemini 3 が聞き取っています...'):
        try:
            # 【エラー解決の鍵】Blobオブジェクトを正しく作成する
            audio_data = types.Blob(
                mime_type='audio/wav',
                data=audio_value.read()
            )
            
            # 命令（プロンプト）の作成
            prompt = "You are a friendly English teacher. Reply in short English. If the user mentions a situation like 'hotel' or 'directions', play along."
            
            # AIに送信
            response = model.generate_content([prompt, audio_data])
            
            # 履歴の保存
            st.session_state.messages.append(f"User: (Voice message)")
            st.session_state.messages.append(f"Teacher: {response.text}")
            
            st.subheader("Teacher:")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
            st.info("ブラウザの『鍵マーク』からマイク許可を再確認してください。")

st.divider()

if st.button("今日の英会話のアドバイスをもらう"):
    if len(st.session_state.messages) > 0:
        with st.spinner('アドバイスを作成中...'):
            advice_res = model.generate_content([
                "これまでの会話を振り返り、文法ミスやより良い表現を日本語で優しく解説してください。",
                str(st.session_state.messages)
            ])
            st.success("✨ 先生からのアドバイス")
            st.write(advice_res.text)
