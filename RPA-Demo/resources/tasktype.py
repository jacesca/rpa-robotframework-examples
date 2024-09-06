from typing import TypedDict


SalesData = TypedDict(
    'SalesData',
    {
        'First Name': str,
        'Last Name': str,
        'Sales': float,
        'Sales Target': float
    }
)
