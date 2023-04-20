from app.db.db import db_reports, db_users, db_tokens
from ..models.report_storage import Report


async def insert_report(report: Report):
    """Insert a report into the database"""
    report_id = await db_reports.insert_one(report.__dict__)
    return report_id


async def get_all_reports():
    """Get all reports from the database"""
    reports = await db_reports.find().to_list(100)
    return reports


async def get_report_by_id(report_id: str):
    """Get a report from the database by its id"""
    report = await db_reports.find_one({"_id": report_id})
    return report


async def get_reports_by_user_id(user_id: str):
    """Get all reports from the database by their uploader"""
    reports = await db_reports.find({"user_id": user_id}).to_list(100)
    return reports


async def get_reports_by_country(country: str):
    """Get all reports from the database by their uploader"""
    reports = await db_reports.find({"country": country}).to_list(100)
    return reports


async def get_reports_by_title(title: str):
    """Get all reports from the database by their title"""
    reports = await db_reports.find({"title": title}).to_list(100)
    return reports


async def get_reports_by_date(date: str):
    """Get all reports from the database by their date"""
    reports = await db_reports.find({"uploadDate": date}).to_list(100)
    return reports


async def delete_report_by_id(report_id: str):
    """Delete a report from the database by its id"""
    report = await db_reports.delete_one({"_id": report_id})
    return report
