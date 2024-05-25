import requests
import time
from weakref import finalize
from requests.adapters import HTTPAdapter
from typing import Optional, Dict, Any

from .components._constants import (
    AUTH_URL,
    API_BASE_URL,
    CONTENT_TYPE,
)

from .components._utils import (
    ensure_token,
    process_response
)



class BymaDataClient(object):
    """
    Generic Client for engagement with BymaData APIs. Takes client ID and secret key to obtain API Token.

    Args:
        client_id (str): Client ID for BymaData API.
        client_secret (str): Client secret key for BymaData API.
    """

    def __init__(self, client_id: str, client_secret: str):
        super(BymaDataClient, self).__init__()

        self._client_id = client_id or None
        self._client_secret = client_secret or None

        self._session = requests.Session()
        self._auth_session = requests.Session()

        self._auth_session.headers.update(
            {
                "Content-Type": CONTENT_TYPE
            }
        )

        self._auth_session.data = {
            "grant_type": "client_credentials",
            "client_id": self._client_id,
            "client_secret": self._client_secret,
        }

        self._token: Optional[str] = None
        self._token_expiration: float = 0  # Initialize token expiration time

        self._api_params: Optional[Dict[str, Any]] = None

        self._refresh_token()  # Fetch the initial token

        self._session.mount("https://", HTTPAdapter())

        self._endpoint: Optional[str] = None

        # Associate the finalize callbacks with the instance.
        # When the instance is garbage collected, the sessions will be closed.
        finalize(self, self._close_sessions)

    def _refresh_token(self) -> None:
        """Refreshes the API token."""
        current_time = time.time()

        token_response = self._auth_session.post(AUTH_URL, data=self._auth_session.data)

        if token_response:
            r = token_response.json()
            self._scopes = r.get("scope", [])
            self._token = r.get("access_token", "")
            self._token_type = r.get("token_type", "")
            self._token_expiration = current_time + r.get("expires_in", 0)
            self._session.headers.update(
                {
                    "Authorization": f"{self._token_type} {self._token}"
                }
            )

    def _make_api_request(self, url: str, params: Optional[Dict[str, Any]] = None, method: str = "GET") -> Any:
        """
        Makes an API request.

        Args:
            url (str): The URL for the API request.
            params (Optional[Dict[str, Any]]): The parameters for the API request.
            method (str): The HTTP method for the API request. Defaults to "GET".

        Returns:
            Any: The processed response from the API.

        Raises:
            KeyError: If an invalid HTTP method is provided.
        """
        _reqs_ = {
            "GET": self._session.get,
            "POST": self._session.post,
        }

        req = _reqs_.get(method)
        if not req:
            raise KeyError("Invalid method. Must be one of: %s" % _reqs_.keys())

        r = req(url, params=params or None, headers={"Authorization": f"Bearer {self._token}"})

        return process_response(r)

    @ensure_token
    def _data_request(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Makes a data request to the API.

        Args:
            path (str): The path for the API request.
            params (Optional[Dict[str, Any]]): The parameters for the API request.

        Returns:
            Any: The processed response from the API.

        Raises:
            ValueError: If an invalid path is provided.
        """
        valid_paths = {'equity', 'fixed_income', 'futures', 'options', 'collateralized_repos', 'trading_lots', 'loans', 'indices', 'turnover', 'intraday'}

        if path not in valid_paths:
            raise ValueError('Invalid path. Must be one of: %s' % valid_paths)

        req_url = API_BASE_URL + self._endpoint + "/" + path

        req = self._make_api_request(req_url, params=params)

        return req

    def _close_sessions(self) -> None:
        """Closes the HTTP sessions."""
        self._session.close()
        self._auth_session.close()
