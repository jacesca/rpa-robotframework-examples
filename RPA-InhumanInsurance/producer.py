from robocorp.tasks import task
from resources.steps import (download_traffic_data, load_traffic_data_as_table,
                             filter_and_sort_traffic_data,
                             get_latest_data_by_country,
                             create_work_item_payloads,
                             save_work_item_payloads)


@task
def produce_traffic_data():
    """
    Inhuman Insurance, Inc. Artificial Intelligence System automation.
    Produces traffic data work items.
    """
    print("Produce task")
    download_traffic_data()
    traffic_data = load_traffic_data_as_table()
    filtered_data = filter_and_sort_traffic_data(traffic_data)
    filtered_data = get_latest_data_by_country(filtered_data)
    payloads = create_work_item_payloads(filtered_data)
    save_work_item_payloads(payloads)
