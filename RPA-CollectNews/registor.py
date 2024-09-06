from resources.steps import ImageRegistor

from robocorp.tasks import task


@task
def download_image_news():
    """
    Fourth step in the process automation for extracting data from a news site.
    This steps download each news images.
    """
    data_table = ImageRegistor()

    data_table.download_images()
    data_table.archive_images()
