import traceback
from fastapi import APIRouter, HTTPException
from app.models.report_storage import SubmitReportModel, Report, submit_report_model_to_report

report_routes = APIRouter()


@report_routes.post("/submit", response_description="Submit new reports")
async def submit_new_report(report_dto: SubmitReportModel):
    """Submit new reports"""
    try:
        report = await submit_report_model_to_report(report_dto)
        await report.insert()
        return {"message": "Report submitted successfully"}

    except Exception as e:
        if "object has no attribute 'user_id'" in str(e):
            raise HTTPException(status_code=400, detail="Invalid access token")
