import json
import logging
import re
import time
from datetime import datetime
from urllib.parse import parse_qs


def generate_user_email() -> str:
    """Generate user email"""
    suffix = 'mailinator.com'
    dynamic_part = datetime.now().strftime('%Y-%m-%dT%H-%M-%S.%f')
    return f"automation_{dynamic_part}@{suffix}"


def get_network_traffic_by_count(driver, request_url: str, path: str, timeout=10, count=1) -> list:
    """Get requests for specific url from all requests data"""
    regex = fr"https?:\/\/.*?{request_url}.*?{path}"
    result = []
    for _ in range(count):
        result.append(driver.wait_for_request(regex, timeout))
    if not result:
        msg = f"No requests found for {request_url}"
        logging.error(msg)
        raise ValueError(msg)
    return result


def get_all_network_traffic(driver, request_url: str) -> list:
    """Get all requests for specific url from all requests data"""
    # wait for requests received
    time.sleep(6)
    result = []
    regex = fr"https?:\/\/.*?{request_url}"
    for request in driver.requests:
        x = re.search(regex, request.url)
        if x is not None:
            result.append(request)
    if not result:
        msg = f"No requests found for {request_url}"
        logging.error(msg)
        raise ValueError(msg)
    return result


def decode_bstring(request_body, request_headers) -> dict:
    """
    Decode b'' string to dictionary

    Args:
        request_body (bytes or str): The body of the HTTP request.
        request_headers (dict): The headers of the HTTP request.

    Returns:
        dict: Decoded dictionary.
    """
    decoded_string = request_body

    # Decode byte string to utf-8 if necessary
    if isinstance(request_body, bytes):
        decoded_string = request_body.decode('utf-8')

    # Check if the content type is JSON
    if 'Content-Type' in request_headers and request_headers['Content-Type'] == 'application/json':
        try:
            return json.loads(decoded_string)
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing JSON: {e}")
            return {}

    # Parse query string if content type is not JSON
    try:
        return parse_qs(decoded_string, errors='True')
    except ValueError as e:
        logging.error(f"Error parsing: {e}")
        return {}


def parse_event_params(params):
    result = {}
    for key, value in params.items():
        if key == 'e':
            params_str = value

            # logic for parsing request.body for kibana events
            params_list = []
            if isinstance(value, list):
                for item in value:
                    item_list = json.loads(item)
                    for i in item_list:
                        params_list.append(i)
                params_str = json.dumps(params_list)

            result = json.loads(params_str)
    return result


def parse_network_request_data(driver, request_url: str, path: str, timeout=10) -> list:
    """Get list of specific requests with parsed body"""
    requests = get_network_traffic_by_count(driver, request_url, path, timeout=timeout)
    result = []
    for request in requests:
        result.append({
            "request_url": request.url,
            "request_path": request.path,
            "request_body": decode_bstring(request.body, request.headers),
            "request_params": request.params,
            "response_body": decode_bstring(request.response.body, request.response.headers),
            "response_status_code": request.response.status_code,
            "response_reason": request.response.reason
        })
    logging.info("Request data is received")
    return result


def parse_network_events_data(driver, request_url: str) -> list:
    """Get list of events with parsed body"""
    requests = get_all_network_traffic(driver, request_url)
    result = []
    for request in reversed(requests):
        if request.response:
            params = parse_event_params(request.params)

            # logic for parsing request.body for kibana events
            if not params:
                request_body = decode_bstring(request.body, request.headers)
                params = parse_event_params(request_body)

            for param in params:
                event_type = param.get('event_type')
                result.append({
                    "request_url": request.url,
                    "request_path": request.path,
                    "event_type": event_type,
                    "request_params": param,
                    "response_status_code": request.response.status_code,
                    "response_reason": request.response.reason
                })
    logging.info("Request data is received")
    return result
