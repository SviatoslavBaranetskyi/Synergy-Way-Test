import pytest
from unittest.mock import patch, MagicMock
from app.services.http_client import HttpClient, HttpClientError
import httpx

BASE_URL = "http://testserver"


def test_get_success():
    client = HttpClient(BASE_URL)

    mock_response = MagicMock()
    mock_response.json.return_value = {"key": "value"}
    mock_response.raise_for_status.return_value = None

    with patch("httpx.Client") as mock_client_class:
        mock_client_instance = mock_client_class.return_value.__enter__.return_value
        mock_client_instance.get.return_value = mock_response

        result = client.get("/endpoint", params={"a": 1})
        assert result == {"key": "value"}
        mock_client_instance.get.assert_called_once_with(
            f"{BASE_URL}/endpoint", params={"a": 1}
        )


def test_get_http_status_error():
    client = HttpClient(BASE_URL)

    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Error", request=MagicMock(), response=MagicMock(status_code=404)
    )

    with patch("httpx.Client") as mock_client_class:
        mock_client_instance = mock_client_class.return_value.__enter__.return_value
        mock_client_instance.get.return_value = mock_response

        with pytest.raises(HttpClientError) as exc_info:
            client.get("/endpoint")

        assert "HTTP error 404" in str(exc_info.value)


def test_get_request_error():
    client = HttpClient(BASE_URL)

    with patch("httpx.Client") as mock_client_class:
        mock_client_instance = mock_client_class.return_value.__enter__.return_value
        mock_client_instance.get.side_effect = httpx.RequestError("Network failure")

        with pytest.raises(HttpClientError) as exc_info:
            client.get("/endpoint")

        assert "Request error while calling" in str(exc_info.value)
