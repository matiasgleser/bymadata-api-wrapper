"""Unofficial BYMADATA API wrapper."""

import pandas as pd
from datetime import datetime

from .components._constants import ENDPOINTS
from .components._utils import validate_params
from .components.BymaDataAPIError import BymaDataAPIError

from ._BaseClient import BymaDataClient



class BymaDataAPI(BymaDataClient):

    """
    Generic Client API for BymaData APIs engament methods. Takes arguments client id and secret key to obtain API Token.
    
        client_id : str
        client_secret : str

    """

    def __init__(self, client_id : str, client_secret : str, endpoint = None):
        if not client_id and not client_id:
            raise ValueError("""
                Insert valid BymaData client ID and client secret key.
                """
            )

        else:
            super().__init__(client_id, client_secret)

        if endpoint in ENDPOINTS:
            self._endpoint = endpoint
        else:
            raise ValueError(
                """
                Invalid endpoint parameter. Must be one of: %s
                """
                % ENDPOINTS
            )

        if not endpoint in self._scopes:
            raise BymaDataAPIError(
                f"""
                No permissions for {endpoint} endpoint.
                """
            )

# Interaction methods
    
    @validate_params(service="equity", ignore=["ticker"])
    def equity(self, ticker=None, settle_period="0003", group="ACCIONES", subgroup=None, operative_form="CONTADO", currency="ARS"):

        path="equity"

        params={
            "group": group,
            "subGroup": subgroup or None if group == "ACCIONES" else None,
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
    def fixed_income(self, ticker=None, settle_period="0003", group="TITULOSPUBLICOS", market="PPT", operative_form="CONTADO", currency="ARS"):

        path="fixed_income"

        params={
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
    def futures(self, group="FUTMONEDAS"):

        path="futures"

        params={
            "group": group,
        }

        res = self._data_request(path=path, params=params)

        return res["result"]


    @validate_params(service="options", ignore=["ticker"])
    def options(self, ticker=None, currency="ARS"):

        path="options"

        params={
            "group": 'OPCIONES',
            "currency": currency
        }

        res = self._data_request(path=path, params=params)

        ops = res["result"]

        if ticker:
            ops = [op for op in ops if op.get("security_id").startswith(ticker)]
            
        return ops


    @validate_params(service="collateralized_repos")
    def repos(self, group="CAUCIONES"):

        path="collateralized_repos"

        params={
            "group": group
        }

        res = self._data_request(path=path, params=params)

        return res["result"]


    @validate_params(service="trading_lots")
    def trading_lots(self, group="PXL", currency="ARS"):

        path="trading_lots"

        params={
            "group": group,
            "currency": currency
        }

        res = self._data_request(path=path, params=params)

        return res["result"]


    @validate_params(service="loans")
    def loans(self, group="PRESTAMOSV", currency="ARS"):

        path="loans"

        params={
            "group": group,
            "currency": currency
        }

        res = self._data_request(path=path, params=params)

        return res["result"]


    def indices(self):

        res = self._data_request(path="indices")

        return res["result"]



    def turnover(self):

        res = self._data_request(path="turnover")

        return res["result"]



    def intraday_ops(self, ticker=None, settle_period="0003", currency="ARS", market="CT", operative_form="C", security_id=None):

        path="intraday"

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
    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret, "snapshot")


class DelayedAPI(BymaDataAPI):
    """API for Delayed MARKET DATA Snapshots"""
    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret, "delay20")


class EndOfDayAPI(BymaDataAPI):
    """API for End-of-Day MARKET DATA Snapshots"""
    def __init__(self, client_id, client_secret):
        super().__init__(client_id, client_secret, "eod")
