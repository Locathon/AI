from fastapi import APIRouter, HTTPException
from schema.qa_schema import QAEntry
from service.qa_manager import add_qa, delete_qa, list_qas, edit_qa

router = APIRouter()

@router.post("/qa/add")
def add_qa_entry(merchant_id: str, qa: QAEntry):
    success = add_qa(merchant_id, qa)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add QA entry.")
    return {"message": "QA entry added successfully."}

@router.delete("/qa/delete")
def delete_qa_entry(merchant_id: str, question: str):
    success = delete_qa(merchant_id, question)
    if not success:
        raise HTTPException(status_code=404, detail="QA not found.")
    return {"message": "QA entry deleted successfully."}

@router.get("/qa/list")
def list_qa_entries(merchant_id: str):
    return list_qas(merchant_id)


# Edit QA entry endpoint
@router.put("/qa/edit")
def edit_qa_entry(merchant_id: str, qa: QAEntry):
    success = edit_qa(merchant_id, qa)
    if not success:
        raise HTTPException(status_code=404, detail="QA not found or update failed.")
    return {"message": "QA entry updated successfully."}