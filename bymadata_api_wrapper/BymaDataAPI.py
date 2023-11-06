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

        try:
            ops = res.get("result")
        except KeyError:
            return res
            raise ValueError("Error processing request.")

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

        try:
            ops = res.get("result")
        except KeyError:
            return res
            raise ValueError("Error processing request.")

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

        try:
            ops = res.get("result")
        except KeyError:
            return res
            raise ValueError("Error processing request.")

        return ops


    @validate_params(service="options", ignore=["ticker"])
    def options(self, ticker=None, currency="ARS"):

        path="options"

        params={
            "group": 'OPCIONES',
            "currency": currency
        }

        res = self._data_request(path=path, params=params)

        try:
            ops = res.get("result")
        except KeyError:
            return res
            raise ValueError("Error processing request.")

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

        try:
            ops = res.get("result")
        except KeyError:
            return res
            raise ValueError("Error processing request.")

        return ops


    @validate_params(service="trading_lots")
    def trading_lots(self, group="PXL", currency="ARS"):

        path="trading_lots"

        params={
            "group": group,
            "currency": currency
        }

        res = self._data_request(path=path, params=params)

        try:
            ops = res.get("result")
        except KeyError:
            return res
            raise ValueError("Error processing request.")

        return ops


    @validate_params(service="loans")
    def loans(self, group="PRESTAMOSV", currency="ARS"):

        path="loans"

        params={
            "group": group,
            "currency": currency
        }

        res = self._data_request(path=path, params=params)

        try:
            ops = res.get("result")
        except KeyError:
            return res
            raise ValueError("Error processing request.")

        return ops



    def indices(self):

        res = self._data_request(path="indices")

        try:
            ops = res.get("result")
        except KeyError:
            return res
            raise ValueError("Error processing request.")

        return ops



    def turnover(self):

        res = self._data_request(path="turnover")

        try:
            ops = res.get("result")
        except KeyError:
            return res
            raise ValueError("Error processing request.")

        return ops



    def intraday_ops(self, ticker=None, settle_period="0003", currency="ARS", market="CT", operative_form="C", as_df=False, security_id=None):

        path="intraday"

        if not security_id:
            security_id = f'{ticker}-{settle_period}-{operative_form}-{market}-{currency}'

        params = {"instrument": security_id}

        res = self._data_request(path=path, params=params)

        try:
            ops = res.get("result")
        except KeyError:
            raise BymaDataAPIError("Error processing request.")

        if as_df:
            ops = pd.DataFrame(ops)
            if not ops.empty:
                ops["Datetime"] = ops.apply(lambda row: datetime(int(row["Date"].split("-")[0]),
                                                                 int(row["Date"].split("-")[1]),
                                                                 int(row["Date"].split("-")[2]),
                                                                 int(str(row["Transact_Time"])[0:2]),
                                                                 int(str(row["Transact_Time"])[2:4]),
                                                                 int(str(row["Transact_Time"])[4:6])), axis = 1)
                ops.drop(["Date", "Transact_Time"], axis = 1, inplace = True)
                ops.set_index("Datetime", inplace = True)

        return ops


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
