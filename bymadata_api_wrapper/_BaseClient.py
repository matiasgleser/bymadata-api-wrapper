import requests
import time
import pandas as pd

from weakref import finalize
from requests.adapters import HTTPAdapter

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
    Generic Client for engagement with BymaData APIs. Takes arguments client id and secret key to obtain API Token.
    
        client_id : str
        client_secret : str

    """

    def __init__(self, client_id : str, client_secret : str):
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

        self._token = None
        self._token_expiration = 0 # Initialize token expiration time

        self._api_params = None
        
        self._refresh_token()  # Fetch the initial token

        self._session.mount("https://", adapter=HTTPAdapter())

        self._endpoint = None

        # Associate the finalize callbacks with the instance.
        # When the instance is garbage collected, the sessions will be closed.
        finalize(self, self._close_sessions)

    def _refresh_token(self):

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


    def _make_api_request(self, url, params=None, method="GET"):
    
        _reqs_ = {
            "GET": self._session.get,
            "POST": self._session.post,
        }

        try:
            req = _reqs_.get(method)
        except KeyError:
            raise KeyError("Invalid method. Must be one of: %s" % _reqs_.keys())
            
        r = req(url, params = params or None, headers = {"Authorization": f"Bearer {self._token}"})

        return process_response(r)

    @ensure_token
    def _data_request(self, path, params=None):


        valid_paths = {'equity', 'fixed_income', 'futures', 'options', 'collateralized_repos', 'trading_lots', 'loans', 'indices', 'turnover', 'intraday'}

        if not path in valid_paths:
            raise ValueError('Invalid path. Must be one of: %s' % valid_paths)
        
        req_url = API_BASE_URL + self._endpoint + "/" + path

        req = self._make_api_request(req_url, params=params)

        return req

    def _close_sessions(self):
        self._session.close()
        self._auth_session.close()
