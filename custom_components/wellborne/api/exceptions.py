"""Exceptions for the Wellborne API client."""

from __future__ import annotations


class WellborneError(Exception):
    """Base exception for Wellborne integration."""


class AuthenticationError(WellborneError):
    """Authentication failed - invalid credentials or expired session."""


class ApiConnectionError(WellborneError):
    """Error connecting to the API."""


class ApiResponseError(WellborneError):
    """Invalid response from the API."""

    def __init__(self, message: str, result_code: int | None = None) -> None:
        """Initialize the exception."""
        super().__init__(message)
        self.result_code = result_code


class ChargerOfflineError(WellborneError):
    """Charger is offline or not responding."""


class SessionExpiredError(AuthenticationError):
    """Session has expired - needs re-authentication."""
