from django.db import connection

def generate_day_report(report_date):
    with connection.cursor() as cursor:
        cursor.callproc('GenerateDailyReport', [report_date])

def generate_material_report_details(report_date):
    with connection.cursor() as cursor:
        cursor.callproc('GenerateMaterialReportDetails', [report_date])