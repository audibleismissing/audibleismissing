from typing import Any, Dict, Optional, Union

import requests

# def make_api_request(
#     method: str,
#     url: str,
#     headers: Optional[Dict[str, str]] = None,
#     params: Optional[Dict[str, Any]] = None,
#     data: Optional[Union[Dict[str, Any], str]] = None,
#     json_data: Optional[Dict[str, Any]] = None,
#     timeout: int = 30,
#     allow_redirects: bool = True,
#     verify_ssl: bool = True
# ) -> Dict[str, Any]:
#     """
#     Make a REST API request and return JSON as a Python object.

#     Args:
#         method: HTTP method (GET, POST, PUT, PATCH, DELETE, etc.)
#         url: The URL to make the request to
#         headers: Optional dictionary of HTTP headers
#         params: Optional dictionary of URL parameters
#         data: Optional data to send in the request body (form data)
#         json_data: Optional JSON data to send in the request body
#         timeout: Request timeout in seconds (default: 30)
#         allow_redirects: Whether to allow redirects (default: True)
#         verify_ssl: Whether to verify SSL certificates (default: True)

#     Returns:
#         Dictionary containing the JSON response

#     Raises:
#         requests.exceptions.RequestException: If the request fails
#         ValueError: If the response is not valid JSON
#     """
#     try:
#         # Make the request
#         response = requests.request(
#             method=method.upper(),
#             url=url,
#             headers=headers,
#             params=params,
#             data=data,
#             json=json_data,
#             timeout=timeout,
#             allow_redirects=allow_redirects,
#             verify=verify_ssl
#         )


#         # Raise an exception for bad status codes (4xx or 5xx)
#         response.raise_for_status()

#         # Parse and return JSON response
#         try:
#             return response.json()
#         except ValueError as e:
#             raise ValueError(f"Invalid JSON response: {e}")

#     except requests.exceptions.RequestException as e:
#         raise requests.exceptions.RequestException(f"API request failed: {e}")


def make_api_request(
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Union[Dict[str, Any], str]] = None,
    json_data: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
    allow_redirects: bool = True,
    verify_ssl: bool = True,
) -> Dict[str, Any]:
    """
    Make a REST API request and return JSON as a Python object.

    Args:
        method: HTTP method (GET, POST, PUT, PATCH, DELETE, etc.)
        url: The URL to make the request to
        headers: Optional dictionary of HTTP headers
        params: Optional dictionary of URL parameters
        data: Optional data to send in the request body (form data)
        json_data: Optional JSON data to send in the request body
        timeout: Request timeout in seconds (default: 30)
        allow_redirects: Whether to allow redirects (default: True)
        verify_ssl: Whether to verify SSL certificates (default: True)

    Returns:
        Dictionary containing the JSON response

    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If the response is not valid JSON
    """

    # Make the request
    response = requests.request(
        method=method.upper(),
        url=url,
        headers=headers,
        params=params,
        data=data,
        json=json_data,
        timeout=timeout,
        allow_redirects=allow_redirects,
        verify=verify_ssl,
    )

    # we want to allow 40x codes since they may just be that the item wasn't found
    if response:
        return response.json()
    else:
        if response.status_code == "404":
            print(f"Not found: {response.status_code()}")
        if response.status_code == "403":
            print(f"Forbidden: {response.status_code()}")
        return None


def get_json_from_api(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
) -> Dict[str, Any]:
    """
    Convenience function to make a GET request and return JSON.

    Args:
        url: The URL to make the request to
        headers: Optional dictionary of HTTP headers
        params: Optional dictionary of URL parameters
        timeout: Request timeout in seconds (default: 30)

    Returns:
        Dictionary containing the JSON response
    """
    return make_api_request(
        method="GET", url=url, headers=headers, params=params, timeout=timeout
    )


def post_json_to_api(
    url: str,
    data: Dict[str, Any],
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 30,
) -> Dict[str, Any]:
    """
    Convenience function to make a POST request with JSON data.

    Args:
        url: The URL to make the request to
        data: Dictionary of data to send as JSON
        headers: Optional dictionary of HTTP headers
        timeout: Request timeout in seconds (default: 30)

    Returns:
        Dictionary containing the JSON response
    """
    return make_api_request(
        method="POST", url=url, headers=headers, json_data=data, timeout=timeout
    )
