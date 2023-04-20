import traceback

from fastapi import APIRouter
from app.models.report_storage import SubmitReportModel, Report, submit_report_model_to_report
from app.db.report_storage_db import insert_report

report_routes = APIRouter()


@report_routes.post("/submit", response_description="Submit new reports")
async def submit_new_report(report_dto: SubmitReportModel):
    """Submit new reports"""
    try:
        report = await submit_report_model_to_report(report_dto)
        await insert_report(report)
        return {"message": "Report submitted successfully"}

    except Exception as e:
        traceback.print_exception(e)
        return {"error": "Something went wrong"}
