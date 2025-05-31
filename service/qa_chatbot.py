import json
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from schema.qa_schema import QAResponse
from utils.text_similarity import normalize_text
from service.gpt_fallback import call_gpt_response

# 간단한 TF-IDF 기반 Q&A 응답
def get_best_answer(merchant_id: str, customer_question: str) -> QAResponse:
    with open("model/merchant_qa_data.json", "r", encoding="utf-8") as f:
        qa_data = json.load(f)

    merchant_qas = qa_data.get(merchant_id, [])
    if not merchant_qas:
        return QAResponse(matched_question="", answer="죄송합니다. 등록된 답변이 없습니다.", score=0.0)

    questions = [normalize_text(item["question"]) for item in merchant_qas]
    answers = [item["answer"] for item in merchant_qas]
    normalized_question = normalize_text(customer_question)

    tfidf = TfidfVectorizer().fit(questions + [normalized_question])
    vectors = tfidf.transform(questions + [normalized_question])

    similarities = cosine_similarity(vectors[-1], vectors[:-1])[0]
    best_idx = similarities.argmax()
    best_score = similarities[best_idx]

    if best_score < 0.4:
        answer = call_gpt_response(customer_question, merchant_qas)
        return QAResponse(matched_question="", answer=answer, score=float(best_score))

    return QAResponse(
        matched_question=merchant_qas[best_idx]["question"],
        answer=answers[best_idx],
        score=float(best_score)
    )