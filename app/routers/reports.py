from fastapi import APIRouter, BackgroundTasks, status
from fastapi.responses import FileResponse, JSONResponse
from sqlmodel import Session

from app.db import ActiveSession
from app.utils.lock import Lock
from app.utils.report import Report

router = APIRouter(tags=["reports"])

file_lock = Lock()


@router.get("/trigger_report", response_class=JSONResponse)
async def trigger_report(
    background_tasks: BackgroundTasks, session: Session = ActiveSession
):

    if file_lock.is_applied():
        return JSONResponse(status_code=status.HTTP_200_OK, content="in_process")

    report = Report()
    background_tasks.add_task(report.generate_report, file_lock, session)

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content="started")


@router.get("/get_report", response_class=FileResponse)
async def get_report():

    if file_lock.is_applied():
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content="Running",
        )

    report = Report()

    if not report.exists():
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="Report doesn't exist",
        )

    return FileResponse(
        path=report.get_full_file_path(),
        media_type=report.media_type,
        filename=report.filename,
    )
