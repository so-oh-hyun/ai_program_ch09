import streamlit as st
from openai import OpenAI

# 텍스트-음성 변환 함수 수정
def text_to_speech(client, text, voice, speed):
	response = client.audio.speech.create(
		model="tts-1",
		voice=voice,
		input=text,
		speed=speed,
	)
	speech_file_path = "AI음성.mp3"
	with open(speech_file_path, "wb") as audio_file:
		audio_file.write(response.content)

def main():
	st.set_page_config(layout="wide")
	st.title("AI 텍스트 낭독기")
	st.caption("텍스트를 음성으로 변환하기")
	# 사이드바 설정
	with st.sidebar:
		openai_api_key = st.text_input("OpenAI API Key", type="password")
		st.write("[OpenAI API Key 받기](https://platform.openai.com/account/api-keys)")
		# 음성 종류 선택
		st.subheader("음성 설정")
		voice = st.selectbox(
			"목소리 선택:",
			[
				"alloy",
				"ash",
				"coral",
				"echo",
				"fable",
				"onyx",
				"nova",
				"sage",
				"shimmer",
			],
		)
		# 음성 속도 조절
		speed = st.slider("속도 조절:", 0.25, 4.0, 1.0)
	# 텍스트 입력 위젯 수정
	default_user_input = """안녕하세요. 여러분.
오늘은 영어에서 자주 사용되는 'Phrasal Verbs'에 대해 배워볼 거예요.
Phrasal Verb란 한국어에는 없는 새로운 개념으로,
동사와 전치사 또는 부사가 결합돼 만들어진 새로운 의미의 표현입니다.
예를 들면 'look up', 'turn off', 'get along' 등이 있습니다.
Phrasal Verb는 일상 대화는 물론 공식적인 글에서도 자주 사용되기 때문에 중요합니다.
또한 문맥에 따라 의미가 달라질 수 있습니다.
다음은 예제 문장입니다.
"I looked up the word in the dictionary.": 사전에서 단어를 찾다.
"Could you please turn off the lights?": 불을 꺼주시겠어요?
"They get along well with each other.": 그들은 서로 잘 지낸다.
"""
	user_input = st.text_area(
		"음성으로 변환할 텍스트를 입력하세요:",
		value=default_user_input,
		height=300,
	)
	# 음성 생성 버튼 추가
	if st.button("음성 생성"):
		if not openai_api_key:
			st.info("계속하려면 API Key를 추가하세요.")
			st.stop()
		if not user_input.strip():
			st.warning("음성으로 변환할 텍스트를 입력하세요.")
			st.stop()
		# OpenAI 클라이언트 생성
		client = OpenAI(api_key=openai_api_key)
		# 텍스트-음성 변환 함수 호출
		text_to_speech(client, user_input, voice, speed)
		# 음성 파일을 오디오 위젯으로 출력
		with open("AI음성.mp3", "rb") as audio_file:
			audio_data = audio_file.read()
			st.audio(data=audio_data, format="audio/mpeg")
		# 다운로드 버튼 추가
		st.download_button(
			label="MP3 다운로드",       	# 버튼에 표시될 텍스트
			data=audio_data,          	# 다운로드할 실제 데이터
			file_name="AI음성.mp3",    	# 다운로드 후 저장될 파일명
		)

if __name__ == "__main__":
	main()
