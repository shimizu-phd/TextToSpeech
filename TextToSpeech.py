import os
from google.cloud import texttospeech
import io
import streamlit as st
from io import StringIO

from google.oauth2 import service_account



credentials = service_account.Credentials.from_service_account_info(st.secrets['GCP'])

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secret.json'



def synthesize_speech(text, lang='日本語', gender='male'):
    name = {
        'ja-JPmale': 'ja-JP-Standard-C',
        'ja-JPfemale': 'ja-JP-Standard-A',
        'en-USmale': 'en-US-Standard-A',
        'en-USfemale': 'en-US-Standard-C'
    }

    lang_code = {
        '英語': 'en-US',
        '日本語': 'ja-JP'
    }

    gender_code = {
        '男性': 'male',
        '女性': 'female'
    }

    client = texttospeech.TextToSpeechClient(credentials=credentials)

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=lang_code[lang],
        ssml_gender=texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED,
        name=name[lang_code[lang] + gender_code[gender]]
    )
    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response

st.title('音声出力アプリ')

st.markdown('### データ準備')

input_option = st.selectbox('入力データの選択', ('直接入力', 'テキストファイル'))

input_data = None

if input_option == '直接入力':
    input_data = st.text_area('こちらにテキストを入力してください', 'これはサンプルです')

else:
    uploaded_file = st.file_uploader('テキストファイルをアップロードしてください', ['TXT'])
    if uploaded_file is not None:
        content = uploaded_file.read()
        input_data = content.decode()

if input_data is not None:
    st.write('入力データ')
    st.write(input_data)

    st.markdown('### パラメータの設定')
    st.subheader('言語と話者の選択')

    lang = st.selectbox('言語を選択してください', ('日本語', '英語'))
    gender = st.selectbox('性別を選択してください', ('男性', '女性'))

    st.markdown('### 音声合成')
    st.write('こちらの文章で音声を作成しますか？')
    if st.button('開始'):
        comment = st.empty()
        comment.write('音声出力を開始')
        response = synthesize_speech(input_data, lang=lang, gender=gender)
        st.audio(response.audio_content)
        comment.write('完了しました')
