import openpyxl
import csv

wb = openpyxl.load_workbook("/home/wunmijordan/gatewaymagnetapp/Report Summary (x_report_summary) (2).xlsx")
sheet = wb.active

with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for row in sheet.iter_rows(values_only=True):
        writer.writerow(row)
