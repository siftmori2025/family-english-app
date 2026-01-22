import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

st.title("Family English Tutor 🎤")

# APIキー設定
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("APIキーをSecretsに設定してください。")

# --- 【解決策】利用可能なモデルを自動検出する ---
@st.cache_resource
def find_working_model():
    try:
        # あなたのキーで「今」使えるモデルを一覧取得
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # 優先順位をつけて探す
        priority = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.5-flash-8b']
        
        for p in priority:
            for actual in available_models:
                if p in actual:
                    return genai.GenerativeModel(actual)
        
        # 何も見つからなければ最初の一つを使う
        if available_models:
            return genai.GenerativeModel(available_models[0])
    except Exception as e:
        st.error(f"モデルリストの取得に失敗しました: {e}")
    return None

model = find_working_model()

if model is None:
    st.error("利用可能なAIモデルが一つも見つかりません。APIキーが正しく作成されているか確認してください。")
else:
    # どのモデルが選ばれたか、デバッグ用に小さく表示
    st.caption(f"Connected to: {model.model_name}")

# --- 動作部分 ---
audio_value = st.audio_input("話しかけてね")

if audio_value:
    with st.spinner('Thinking...'):
        try:
            # 音声データを送信
            response = model.generate_content([
                "You are a friendly English teacher. Reply in 1 very short sentence.",
                {"mime_type": "audio/wav", "data": audio_value.getvalue()}
            ])
            
            st.subheader("Teacher:")
            st.write(response.text)
            
            # 音声再生
            clean_text = response.text.replace('"', '\\"')
            js_code = f"<script>var m=new SpeechSynthesisUtterance('{clean_text}');m.lang='en-US';window.speechSynthesis.speak(m);</script>"
            components.html(js_code, height=0)
            
        except Exception as e:
            st.error(f"Error: {e}")
