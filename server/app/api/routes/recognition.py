from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.api.deps import get_db, verify_api_key
from app.core.config import get_settings
from app.db.repositories import recognition_repository
from app.schemas.recognition import RecognitionRead, RecognitionResponse
from app.services.image_service import save_image
from app.services.recognition_service import recognize_image
from app.utils.image_utils import load_image_bytes

router = APIRouter(tags=["recognition"])


@router.post(
    "/recognize",
    response_model=RecognitionResponse,
    dependencies=[Depends(verify_api_key)],
)
async def recognize(
    file: UploadFile = File(...),
    device_id: Optional[str] = Form(default=None),
    db: Session = Depends(get_db),
):
    settings = get_settings()

    data = await file.read()
    image = load_image_bytes(data, settings.max_upload_mb)
    image_path = save_image(data, file.filename or "capture.jpg")

    result = await run_in_threadpool(
        recognize_image, db, image, device_id, image_path
    )
    return result


@router.get("/recognitions", response_model=List[RecognitionRead])
def list_recognitions(
    limit: int = 50,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    return recognition_repository.list_recognitions(db, limit=limit)
