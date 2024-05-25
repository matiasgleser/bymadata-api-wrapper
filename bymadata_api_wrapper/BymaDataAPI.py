"""Unofficial BYMADATA API wrapper."""

from .components._constants import ENDPOINTS
from .components._utils import validate_params
from .components.BymaDataAPIError import BymaDataAPIError
from ._BaseClient import BymaDataClient
from typing import Optional, List, Dict, Any


class BymaDataAPI(BymaDataClient):
    """
    Generic Client API for BymaData APIs engagement methods.

    Args:
        client_id (str): Client ID for BymaData API.
        client_secret (str): Client secret key for BymaData API.
        endpoint (Optional[str]): Endpoint for the API. Must be one of the valid endpoints.

    Raises:
        ValueError: If client_id or client_secret is not provided, or if the endpoint is invalid.
        BymaDataAPIError: If there are no permissions for the specified endpoint.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        endpoint: Optional[str] = None
    ):
        if not client_id or not client_secret:
            raise ValueError("Insert valid BymaData client ID and client secret key.")

        super().__init__(client_id, client_secret)

        if endpoint in ENDPOINTS:
            self._endpoint = endpoint
        else:
            raise ValueError(f"Invalid endpoint parameter. Must be one of: {ENDPOINTS}")

        if endpoint not in self._scopes:
            raise BymaDataAPIError(f"No permissions for {endpoint} endpoint.")

    @validate_params(service="equity", ignore=["ticker"])
    def equity(
        self,
        ticker: Optional[str] = None
        settle_period: str = "0003",
        group: str = "ACCIONES",
        subgroup: Optional[str] = None,
        operative_form: str = "CONTADO",
        currency: str = "ARS"
    ) -> List[Dict[str, Any]]:
        """
        Fetches equity data.

        Args:
            ticker (Optional[str]): Ticker symbol to filter results.
            settle_period (str): Settlement period.
            group (str): Group category.
            subgroup (Optional[str]): Subgroup category.
            operative_form (str): Operative form.
            currency (str): Currency code.

        Returns:
            List[Dict[str, Any]]: List of equity operations.
        """
        path = "equity"

        params = {
            "group": group,
            "subGroup": subgroup or (None if group == "ACCIONES" else None),
            "settlPeriod": settle_period,
            "operativeForm": operative_form,
            "currency": currency
        }

        res = self._data_request(path=path, params=params)
        ops = res["result"]

        if ticker:
            ops = [op for op in ops if op.get("security_id").startswith(ticker)]

        return ops

    @validate_params(service="fixed_income", ignore=["ticker"])
    def fixed_income(
        self,
        ticker: Optional[str] = None,
        settle_period: str = "0003",
        group: str = "TITULOSPUBLICOS",
        market: str = "PPT",
        operative_form: str = "CONTADO",
        currency: str = "ARS"
    ) -> List[Dict[str, Any]]:
        """
        Fetches fixed income data.

        Args:
            ticker (Optional[str]): Ticker symbol to filter results.
            settle_period (str): Settlement period.
            group (str): Group category.
            market (str): Market type.
            operative_form (str): Operative form.
            currency (str): Currency code.

        Returns:
            List[Dict[str, Any]]: List of fixed income operations.
        """
        path = "fixed_income"

        params = {
            "group": group,
            "settlPeriod": settle_period,
            "market": market,
            "operativeForm": operative_form,
            "currency": currency
        }

        res = self._data_request(path=path, params=params)
        ops = res.get("result")

        if ticker:
            ops = [op for op in ops if op.get("security_id").startswith(ticker)]

        return ops

    @validate_params(service="futures")
    def futures(
        self,
        group: str = "FUTMONEDAS"
    ) -> List[Dict[str, Any]]:
        """
        Fetches futures data.

        Args:
            group (str): Group category.

        Returns:
            List[Dict[str, Any]]: List of futures operations.
        """
        path = "futures"

        params = {
            "group": group,
        }

        res = self._data_request(path=path, params=params)

        return res["result"]

    @validate_params(service="options", ignore=["ticker"])
    def options(
        self,
        ticker: Optional[str] = None,
        currency: str = "ARS"
    ) -> List[Dict[str, Any]]:
        """
        Fetches options data.

        Args:
            ticker (Optional[str]): Ticker symbol to filter results.
            currency (str): Currency code.

        Returns:
            List[Dict[str, Any]]: List of options operations.
        """
        path = "options"

        params = {
            "group": 'OPCIONES',
            "currency": currency
        }

        res = self._data_request(path=path, params=params)
        ops = res["result"]

        if ticker:
            ops = [op for op in ops if op.get("security_id").startswith(ticker)]

        return ops

    @validate_params(service="collateralized_repos")
    def repos(
        self,
        group: str = "CAUCIONES"
    ) -> List[Dict[str, Any]]:
        """
        Fetches collateralized repos data.

        Args:
            group (str): Group category.

        Returns:
            List[Dict[str, Any]]: List of repos operations.
        """
        path = "collateralized_repos"

        params = {
            "group": group
        }

        res = self._data_request(path=path, params=params)

        return res["result"]

    @validate_params(service="trading_lots")
    def trading_lots(
        self,
        group: str = "PXL",
        currency: str = "ARS"
    ) -> List[Dict[str, Any]]:
        """
        Fetches trading lots data.

        Args:
            group (str): Group category.
            currency (str): Currency code.

        Returns:
            List[Dict[str, Any]]: List of trading lots operations.
        """
        path = "trading_lots"

        params = {
            "group": group,
            "currency": currency
        }

        res = self._data_request(path=path, params=params)

        return res["result"]

    @validate_params(service="loans")
    def loans(
        self,
        group: str = "PRESTAMOSV",
        currency: str = "ARS"
    ) -> List[Dict[str, Any]]:
        """
        Fetches loans data.

        Args:
            group (str): Group category.
            currency (str): Currency code.

        Returns:
            List[Dict[str, Any]]: List of loans operations.
        """
        path = "loans"

        params = {
            "group": group,
            "currency": currency
        }

        res = self._data_request(path=path, params=params)

        return res["result"]

    def indices(
        self
    ) -> List[Dict[str, Any]]:
        """
        Fetches indices data.

        Returns:
            List[Dict[str, Any]]: List of indices data.
        """
        res = self._data_request(path="indices")

        return res["result"]

    def turnover(
        self
    ) -> List[Dict[str, Any]]:
        """
        Fetches turnover data.

        Returns:
            List[Dict[str, Any]]: List of turnover data.
        """
        res = self._data_request(path="turnover")

        return res["result"]

    def intraday_ops(
        self,
        ticker: Optional[str] = None,
        settle_period: str = "0003",
        currency: str = "ARS",
        market: str = "CT",
        operative_form: str = "C",
        security_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetches intraday operations data.

        Args:
            ticker (Optional[str]): Ticker symbol to filter results.
            settle_period (str): Settlement period.
            currency (str): Currency code.
            market (str): Market type.
            operative_form (str): Operative form.
            security_id (Optional[str]): Security ID.

        Returns:
            List[Dict[str, Any]]: List of intraday operations.
        """
        path = "intraday"

        if not security_id:
            security_id = f'{ticker}-{settle_period}-{operative_form}-{market}-{currency}'

        params = {"instrument": security_id}

        res = self._data_request(path=path, params=params)

        return res["result"]


######################################################
# ENDPOINT SPECIFIC API WRAPPERS
######################################################

class SnapshotAPI(BymaDataAPI):
    """API for Real-Time MARKET DATA Snapshots"""
    def __init__(self, client_id: str, client_secret: str):
        super().__init__(client_id, client_secret, "snapshot")


class DelayedAPI(BymaDataAPI):
    """API for Delayed MARKET DATA Snapshots"""
    def __init__(self, client_id: str, client_secret: str):
        super().__init__(client_id, client_secret, "delay20")


class EndOfDayAPI(BymaDataAPI):
    """API for End-of-Day MARKET DATA Snapshots"""
    def __init__(self, client_id: str, client_secret: str):
        super().__init__(client_id, client_secret, "eod")
