import requests
from resources.locations import (TRAFFIC_DATA_URL, TRAFFIC_DATA_JSON_FILE,
                                 TRAFFIC_DATA_CSV_FILE, SALES_SYSTEM_API,
                                 RATE_KEY, GENDER_KEY, COUNTRY_KEY, YEAR_KEY)
from resources.types import TrafficPayload

from typing import List

from RPA.HTTP import HTTP
from RPA.JSON import JSON
from RPA.Tables import Tables, Table
from robocorp import workitems


# Global objects
http = HTTP()
json = JSON()
table = Tables()


def download_traffic_data() -> None:
    """Download the road traffic fatality rate."""
    http.download(
        url=TRAFFIC_DATA_URL,
        target_file=TRAFFIC_DATA_JSON_FILE,
        overwrite=True
    )


def load_traffic_data_as_table() -> Table:
    """Load the traffic data and return a RPA.Tables"""
    json_data = json.load_json_from_file(TRAFFIC_DATA_JSON_FILE)
    table_from_json = table.create_table(json_data['value'])
    table.write_table_to_csv(table_from_json, TRAFFIC_DATA_CSV_FILE)
    return table_from_json


def filter_and_sort_traffic_data(data: Table,
                                 max_rate: float = 5.0,
                                 gender_group: str = "BTSX") -> Table:
    """
    Filter traffic data to obtain lowest road traffic fatality
    for each country
    """
    table.filter_table_by_column(data, RATE_KEY, "<", max_rate)
    table.filter_table_by_column(data, GENDER_KEY, '==', gender_group)
    table.sort_table_by_column(data, YEAR_KEY, ascending=False)
    return data


def get_latest_data_by_country(data: Table) -> Table:
    """
    Filter traffic data to return the latest available data per country
    """
    latest_data_by_country = []

    data = table.group_table_by_column(data, COUNTRY_KEY)
    for group in data:
        first_row = table.pop_table_row(group)
        latest_data_by_country.append(first_row)
    return latest_data_by_country


def create_work_item_payloads(data: Table) -> List[TrafficPayload]:
    """Transform the raw data into business data (sales system API payloads)"""
    payloads = []
    for row in data:
        payloads.append({
            'country': row[COUNTRY_KEY],
            'year': row[YEAR_KEY],
            'rate': row[RATE_KEY]
        })
    return payloads


def save_work_item_payloads(payloads: List[TrafficPayload]) -> None:
    """
    Saves each payload as a work item.
    Review `RPA-InhumanInsurance/devdata/work-items-out/run-1/work-items.json`
    for more details
    """
    for payload in payloads:
        variables = dict(traffic_data=payload)
        workitems.outputs.create(variables)


def post_traffic_data_to_sales_system(traffic_data: TrafficPayload) -> None:
    """Send data to sales system API"""
    response = requests.post(SALES_SYSTEM_API, json=traffic_data)
    # response.raise_for_status()  # For debugging purposes
    return response.status_code, response.json()
