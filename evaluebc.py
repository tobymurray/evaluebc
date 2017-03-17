import requests
import json
from bs4 import BeautifulSoup
import sys

OUTER_DATA_KEY = 'd'
INNER_DATA_KEY = 'aaData'

ADDRESS_INDEX = 2
PID_IDNEX = 3
PROPERTY_KEY_INDEX = 4

TOTAL_VALUE_ELEMENT = 'span'
TOTAL_VALUE_CLASS = 'recentSearchBTValue'

HEADERS = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Language': "en-US,en;q=0.5",
    'Accept-Encoding': "gzip, deflate",
    'Content-Type': "application/json; charset=utf-8",
    'X-Requested-With': "XMLHttpRequest",
    'Referer': "https://evaluebc.bcassessment.ca/Default.aspx",
}

PAYLOAD = {
    'PID': sys.argv[1]
}

lookup_request = requests.get(
    'https://evaluebc.bcassessment.ca/Default.aspx/GetPIDs', headers=HEADERS, params=PAYLOAD)

wrapped_lookup_response = json.loads(lookup_request.json()[OUTER_DATA_KEY])

lookup_response_array = wrapped_lookup_response.get(INNER_DATA_KEY)[0]

property_key = lookup_response_array[PROPERTY_KEY_INDEX]

detail_request = requests.get(
    'https://evaluebc.bcassessment.ca/Property.aspx?_oa=' + property_key,
    headers=HEADERS
)

html_soup = BeautifulSoup(detail_request.content, 'html.parser')

total_value = html_soup.findAll(
    TOTAL_VALUE_ELEMENT, {'class': TOTAL_VALUE_CLASS})[0].text
print("For property at " + lookup_response_array[ADDRESS_INDEX] + " with PID " 
    + lookup_response_array[PID_IDNEX] + " the list price is " + total_value)
