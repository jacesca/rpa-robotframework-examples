import os

from resources.tasktype import SalesData
from config.filelocation import (SITE_URL, EXCEL_FILE, LOCAL_EXCEL_FILE,
                                 SCREENSHOT_FILE, SALES_RESULT_PDF_FILE)

from dotenv import load_dotenv
from time import sleep

from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Excel.Files import Files
from RPA.PDF import PDF


# Global page
page = None


def start_environment() -> None:
    """Configure environment to run automation"""
    # browser.configure(
    #     slowmo=100   # milliseconds
    # )
    load_dotenv(dotenv_path='config/.env')


def open_the_intranet_website(site: str = SITE_URL) -> None:
    """Navigates to the given url site"""
    global page
    browser.goto(site)
    page = browser.page()


def log_in() -> None:
    """Fills in the login form and clicks the 'Log in' button"""

    user = os.getenv('USER')
    password = os.getenv('PASSWORD')

    page.locator("#username").fill(user)
    page.locator("#password").fill(password)
    page.locator("button:text('Log in')").click()
    sleep(3)


def fill_and_submit_sales_form(
    sales_data: SalesData
) -> None:
    """Insert the sales data for the week and export it as a PDF"""

    page.locator("#firstname").fill(sales_data['First Name'])
    page.locator("#lastname").fill(sales_data['Last Name'])
    page.locator("#salesresult").fill(str(sales_data['Sales']))
    page.locator("#salestarget").select_option(str(sales_data['Sales Target']))
    page.locator("button:text('SUBMIT')").click()


def download_excel_file(excel_file: str = EXCEL_FILE,
                        local_excel_file: str = LOCAL_EXCEL_FILE) -> None:
    """Downloads excel file from the given URL"""
    http = HTTP()
    http.download(url=excel_file, target_file=local_excel_file)


def fill_form_with_excel_data(
    local_excel_file: str = LOCAL_EXCEL_FILE
) -> None:
    """Read data from excel and fill in the sales form"""
    excel = Files()
    excel.open_workbook(local_excel_file)
    worksheet = excel.read_worksheet_as_table("data", header=True)
    excel.close_workbook()

    for row in worksheet:
        fill_and_submit_sales_form(sales_data=row)


def collect_results(screenshot_file: str = SCREENSHOT_FILE):
    """Take a screenshot of the page"""
    page = browser.page()
    page.screenshot(path=screenshot_file)


def export_as_pdf(sales_result_pdf_file: str = SALES_RESULT_PDF_FILE):
    """Export the data to a pdf file"""
    sales_results_html = page.locator("#sales-results").inner_html()
    pdf = PDF()
    pdf.html_to_pdf(sales_results_html, sales_result_pdf_file)


def log_out():
    """Presses the 'Log out' button"""
    page.locator("#logout").click()
