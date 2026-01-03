from typing import Any, Dict, Optional

import httpx


class HttpClientError(Exception):
    """Base exception for HTTP client errors."""


class HttpClient:
    def __init__(
        self,
        base_url: str,
        timeout: float = 10.0,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = headers or {}

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            with httpx.Client(timeout=self.timeout, headers=self.headers) as client:
                response = client.get(url, params=params)
                response.raise_for_status()
                return response.json()

        except httpx.HTTPStatusError as exc:
            raise HttpClientError(
                f"HTTP error {exc.response.status_code} for {url}"
            ) from exc

        except httpx.RequestError as exc:
            raise HttpClientError(
                f"Request error while calling {url}"
            ) from exc
