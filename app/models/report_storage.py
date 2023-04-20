from datetime import date

from bson import ObjectId
from pydantic import BaseModel
from app.db.user_db import get_user_id_by_token


class Report:
    title: str = None
    report_url: str = None
    user_id: str = None
    country: str = None
    upload_date: str = None


class SubmitReportModel(BaseModel):
    title: str = None
    report_url: str = None
    access_token: str = None
    country: str = None

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "A report",
                "report_url": "www.report.com/report.pdf",
                "access_token": "aCcEssToKEn",
                "uploader": "Hungary"
            }
        }


class GetUserReportsModel(BaseModel):
    access_token: str = None

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "access_token": "aCcEssToKEn"
            }
        }


async def submit_report_model_to_report(report_dto: SubmitReportModel):
    """Converts a SubmitReportModel to a Report"""
    report = Report()
    report.title = report_dto.title
    report.report_url = report_dto.report_url
    report.country = report_dto.country
    report.user_id = await get_user_id_by_token(report_dto.access_token)
    report.upload_date = date.today().strftime("%d/%m/%Y")

    return report
