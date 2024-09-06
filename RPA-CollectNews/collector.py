from resources.steps import NewsScrapper

from robocorp.tasks import task


@task
def colect_news():
    """
    Second step in the process automation for extracting data from a news site.
    This steps filter the news according to parameters, and extract the html.
    """
    scrapper = NewsScrapper()

    scrapper.start_environment()
    scrapper.open_website()
    scrapper.filter_by_search_key()
    scrapper.order_by_date()
    scrapper.getting_more_news_if_available()
    scrapper.extract_html_result()
    scrapper.clean_html_result()
    scrapper.save_html_to_workitems()
