from resources.steps import NewsDataTable

from robocorp.tasks import task


@task
def export_extracted_data_to_excel():
    """
    Third step in the process automation for extracting data from a news site.
    This steps parser the html and export it to an excel file.
    """
    data_table = NewsDataTable()

    data_table.format_table()
    data_table.export_as_excel_file()
    data_table.save_images_to_workitems()
