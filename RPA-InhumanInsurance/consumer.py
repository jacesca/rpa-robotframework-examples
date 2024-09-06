from robocorp.tasks import task
from robocorp import workitems
from resources.steps import post_traffic_data_to_sales_system


@task
def consume_traffic_data():
    """
    Inhuman Insurance, Inc. Artificial Intelligence System automation.
    Consumes traffic data work items.
    """
    print("consume")
    for item in workitems.inputs:
        traffic_data = item.payload["traffic_data"]
        # Check country code is three letters long
        if len(traffic_data['country']) == 3:
            status, return_json = post_traffic_data_to_sales_system(traffic_data)  # noqa
            if status == 200:
                item.done()
            else:
                item.fail(
                    exception_type='APPLICATION',
                    code='TRAFFIC_DATA_POST_FAILED',
                    message=return_json["message"]
                )
        else:
            item.fail(
                exception_type='BUSINESS',
                code='INVALID_TRAFFIC_DATA',
                message=item.payload
            )
