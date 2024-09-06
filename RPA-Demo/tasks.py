from robocorp.tasks import task
from resources.steps import (open_the_intranet_website, start_environment,
                             log_in, download_excel_file,
                             fill_form_with_excel_data, collect_results,
                             export_as_pdf, log_out)


# Automatation
@task
def robot_spare_bin_python():
    """Insert the sales data for the week and export it as a PDF"""

    start_environment()
    open_the_intranet_website()
    log_in()
    download_excel_file()
    fill_form_with_excel_data()
    collect_results()
    export_as_pdf()
    log_out()
