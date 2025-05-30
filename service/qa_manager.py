import json
import os
from schema.qa_schema import QAEntry

QA_FILE = "model/merchant_qa_data.json"

def _load_data():
    if not os.path.exists(QA_FILE):
        return {}
    with open(QA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_data(data):
    with open(QA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def add_qa(merchant_id: str, qa: QAEntry) -> bool:
    data = _load_data()
    data.setdefault(merchant_id, []).append(qa.dict())
    _save_data(data)
    return True

def delete_qa(merchant_id: str, question: str) -> bool:
    data = _load_data()
    if merchant_id not in data:
        return False
    original = len(data[merchant_id])
    data[merchant_id] = [q for q in data[merchant_id] if q["question"] != question]
    if len(data[merchant_id]) == original:
        return False
    _save_data(data)
    return True

def list_qas(merchant_id: str):
    data = _load_data()
    return data.get(merchant_id, [])

def edit_qa(merchant_id: str, qa: QAEntry) -> bool:
    data = _load_data()
    if merchant_id not in data:
        return False
    updated = False
    for item in data[merchant_id]:
        if item["question"] == qa.question:
            item["answer"] = qa.answer
            updated = True
            break
    if not updated:
        return False
    _save_data(data)
    return True