import openai
from config.openai_config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def call_gpt_response(user_question: str, qa_list: list) -> str:
    qa_formatted = "\n".join([f"Q: {q['question']}\nA: {q['answer']}" for q in qa_list])
    
    prompt = (
        "당신은 가게 안내 도우미입니다. 아래는 매장 정보 기반 Q&A입니다.\n"
        f"{qa_formatted}\n\n"
        f"사용자 질문: {user_question}\n\n자연스럽고 정중하게 대답해주세요."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 정중한 고객 응대 전문가입니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()