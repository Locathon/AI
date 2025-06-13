from openai import OpenAI
import os
from dotenv import load_dotenv
from service.log_writer import save_transform_log
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def convert_style(original_text: str, tone: str = None) -> str:
    try:
        tone_instruction = f" 톤은 '{tone}' 느낌으로." if tone else ""
        prompt = (
            "다음 가게 소개글을 MZ세대에게 어필할 수 있도록 감성적인 문체로 자연스럽게 바꿔줘. "
            "과하지 않게, 150자 이내로 부탁해." + tone_instruction + "\n\n"
            f"원문: {original_text}\n\n감성 문체:"
        )
    
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 감성적인 카피라이팅 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )

        transformed = response.choices[0].message.content.strip()
        save_transform_log(original_text, transformed)
        return transformed
    except Exception as e:
            print("🔥 변환 중 에러 발생:", e)
            raise