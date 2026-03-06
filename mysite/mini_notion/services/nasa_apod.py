import json
from datetime import date
import socket
import ssl
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

try:
    import certifi
except ImportError:  # pragma: no cover - deployment fallback
    certifi = None


class NasaApiError(Exception):
    """Raised when the NASA APOD API cannot be reached or parsed safely."""


def fetch_apod(*, api_key: str, timeout_seconds: int = 10, apod_date: date | None = None) -> dict:
    """
    Fetch NASA Astronomy Picture of the Day data.
    Returns a normalized dictionary used by Django views/templates.
    """
    if not api_key:
        raise NasaApiError("NASA_API_KEY is missing.")

    query_params = {"api_key": api_key}
    if apod_date is not None:
        query_params["date"] = apod_date.isoformat()

    url = f"https://api.nasa.gov/planetary/apod?{urlencode(query_params)}"

    try:
        ssl_context = (
            ssl.create_default_context(cafile=certifi.where())
            if certifi is not None
            else ssl.create_default_context()
        )
        with urlopen(url, timeout=timeout_seconds, context=ssl_context) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        if exc.code == 429:
            raise NasaApiError(
                "NASA API rate limit exceeded. The DEMO_KEY allows only 30 requests per hour. "
                "Get your free API key at https://api.nasa.gov/ for 1,000 requests/hour limit. "
                "Note: Some NASA APIs have been archived - APOD API is still active."
            ) from exc
        elif exc.code == 403:
            raise NasaApiError(
                "NASA API access forbidden. This may be due to: "
                "1) Invalid API key, 2) Archived/deprecated endpoint, or 3) Service maintenance. "
                "Check https://api.nasa.gov/ for API status."
            ) from exc
        elif exc.code >= 500:
            raise NasaApiError(
                f"NASA API server error ({exc.code}). The service may be temporarily unavailable. "
                "Try again in a few minutes."
            ) from exc
        raise NasaApiError(f"NASA API HTTP error: {exc.code}") from exc
    except URLError as exc:
        reason = exc.reason
        if isinstance(reason, socket.timeout):
            raise NasaApiError("Could not connect to NASA API: request timed out.") from exc
        if isinstance(reason, OSError):
            details = reason.strerror or str(reason)
        else:
            details = str(reason) if reason else "unknown network error"
        raise NasaApiError(f"Could not connect to NASA API: {details}") from exc
    except (ValueError, json.JSONDecodeError) as exc:
        raise NasaApiError("NASA API returned invalid JSON.") from exc

    if "error" in payload:
        message = payload["error"].get("message", "Unknown NASA API error.")
        raise NasaApiError(message)

    return {
        "date": payload.get("date"),
        "title": payload.get("title"),
        "explanation": payload.get("explanation"),
        "media_type": payload.get("media_type"),
        "url": payload.get("url"),
        "hdurl": payload.get("hdurl"),
        "copyright": payload.get("copyright"),
    }
