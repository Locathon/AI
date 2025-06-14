def extract_changed_keywords(original: str, transformed: str) -> list:
    original_words = set(re.findall(r'[가-힣]{2,}', original))
    transformed_words = set(re.findall(r'[가-힣]{2,}', transformed))
    return list(transformed_words - original_words)
from openai import OpenAI
import os
from dotenv import load_dotenv
from service.log_writer import save_transform_log
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def highlight_keywords(text: str, keywords: list):
    def _replace(match):
        return f'<span style="color:#286FFD">{match.group(0)}</span>'
    for kw in sorted(set(keywords), key=len, reverse=True):
        if kw:
            text = re.sub(re.escape(kw), _replace, text, flags=re.IGNORECASE)
    return text

def convert_style(original_text: str, tone: str = None, store_name: str = None, sns: str = None) -> str:
    try:
        # 1. store_name + sns 조합 우선 처리
        if store_name and sns:
            platform = sns
            store = store_name
        # 2. tone만 전달된 경우(tone=인스타그램 등)
        elif tone:
            platform = tone
            store = store_name or ""
        else:
            platform = "일반"
            store = store_name or ""
        
        tone_desc = {
            "인스타그램": "감성적, 이모지와 해시태그 사용",
            "X": "150자 이내, 짧고 임팩트 있게",
            "네이버 스토어": "정보 중심, 신뢰감 있는 톤",
            "스레드": "트렌디하고 캐주얼하게"
        }.get(platform, "친근하고 읽기 쉽게")

        store_mention = f'스토어명: "{store}"을(를) 포함하고, ' if store else ""

        prompt = f"""
                당신은 MZ세대를 대상으로 한 소셜미디어 마케팅 전문가입니다.
                플랫폼: {platform}
                스타일: {tone_desc}
                {store_mention}원문을 {platform}에 적합한 말투로 최대 150자(트윗 X는 280자)로 변환해 주세요.
                구조: [Hook → 본문 → CTA] 형식으로 구성하세요.

                원문:
                {original_text}

                예시 출력:
                Hook: "WOW~!"
                본문: "달콤함 가득! 황금동의 전통 약과, 직접 만든 수제 디저트."
                CTA: "지금 바로 확인하세요!"

                변환된 문구:
                """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "당신은 감성적인 카피라이팅 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )

        transformed = response.choices[0].message.content.strip()

        # AI가 새로 만든 단어 추출
        changed_keywords = extract_changed_keywords(original_text, transformed)

        # 문장 구조 제거 (Hook/본문/CTA 구분 없애고 문장으로)
        transformed = re.sub(r'(Hook|본문|CTA):\s*', '', transformed)
        transformed = transformed.replace('"', '').replace('\n', ' ')

        transformed = highlight_keywords(transformed, changed_keywords)

        save_transform_log(original_text, transformed)
        return transformed
    except Exception as e:
        print("🔥 변환 중 에러 발생:", e)
        raise