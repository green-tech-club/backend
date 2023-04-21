from datetime import date
from beanie import Document
from bson import ObjectId
from pydantic import BaseModel
from app.db.db import get_access_token_db
from app.models.token import AccessToken


class Report(Document):
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
                "country": "Hungary"
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
    access_token = await AccessToken.find_one({"token": report_dto.access_token})
    report.user_id = access_token.user_id
    report.upload_date = date.today().strftime("%d/%m/%Y")

    return report
