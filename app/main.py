from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.core.schemas import AskRequest, AskResponse
from app.services.qa import QAService


app = FastAPI(title=settings.app_name)
templates = Jinja2Templates(directory=str(settings.data_dir.parent / "app" / "templates"))
qa_service = QAService()


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "app_name": settings.app_name,
            "doc_count": len(list(settings.docs_dir.glob("*.md"))),
        },
    )


@app.post("/api/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    return qa_service.answer(request.question)


@app.post("/api/reindex")
def reindex() -> dict[str, str]:
    qa_service.refresh_index()
    return {"status": "ok", "message": "Knowledge base reindexed."}


@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)) -> dict[str, str]:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".md", ".txt"}:
        raise HTTPException(status_code=400, detail="Only .md and .txt files are supported.")

    safe_name = Path(file.filename or "uploaded_doc.md").name.replace(" ", "_")
    if not safe_name:
        safe_name = "uploaded_doc.md"
    destination = settings.docs_dir / safe_name
    contents = await file.read()
    destination.write_text(contents.decode("utf-8"), encoding="utf-8")
    qa_service.refresh_index()
    return {"status": "ok", "message": f"Uploaded {safe_name} and refreshed the index."}
