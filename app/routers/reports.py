from fastapi import APIRouter, BackgroundTasks, status
from fastapi.responses import FileResponse, JSONResponse

from app.routers.utils import Report

router = APIRouter(tags=["reports"])

report = Report()


@router.get("/trigger_report", response_class=JSONResponse)
async def trigger_report(background_tasks: BackgroundTasks):

    if report.status():
        return JSONResponse(status_code=status.HTTP_200_OK, content="in_process")

    background_tasks.add_task(report.generate_report)

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content="started")


@router.get("/get_report", response_class=FileResponse)
async def get_report():
    if not report.exists():
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content="file not found, run /trigger_report first",
        )

    return FileResponse(
        path=report.get_full_file_path(),
        media_type=report.media_type,
        filename=report.filename,
    )
