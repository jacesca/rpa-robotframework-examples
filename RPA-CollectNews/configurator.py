from robocorp.tasks import task
from resources.steps import ProcessConfiguration


@task
def configurator():
    """
    First step in the process automation for extracting data from a news site.
    Three saved parameters in the workitem:
    - search phrase
    - news category/section/topic
    - number of months for which you need to receive news (if applicable)
    """
    configuration = ProcessConfiguration()
    configuration.get_parameters_from_cloud_storage()
    configuration.save_parameters_to_workitems()
