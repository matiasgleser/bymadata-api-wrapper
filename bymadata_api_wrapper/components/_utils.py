import time
import json
import requests

from typing import Any, Dict

from functools import wraps
from inspect import signature

from .BymaDataAPIError import (
    BymaDataAPIError,
    UnexpectedResponseError
)

from ._enums import (
    EquityParameters,
    FixedIncomeParameters,
    FuturesParameters,
    OptionsParameters,
    ReposParameters,
    TradingLotsParameters,
    LoansParameters,
)


listring = lambda x: ", ".join(x)


def ensure_token(func):
    def wrapper(self, *args, **kwargs):
        current_time = time.time()
        if self._token is None or self._token_expiration - current_time <= 60:
            self._refresh_token()
        return func(self, *args, **kwargs)
    return wrapper



def process_response(response: requests.Response) -> Dict[str, Any]:
    try:
        if response.status_code == 200:
            return response.json()

        elif response.status_code == 400:
            try:
                data = response.json()
                error_msg = data.get("descripcion", "Server responded with a 400 status without a description")
                raise BymaDataAPIError(error_msg)
            except ValueError:
                error_msg = "Server responded with a 400 status without a description"
                raise BymaDataAPIError(error_msg)
        else:
            error_msg = f"Received unexpected status code: {response.status_code}"
            raise UnexpectedResponseError(error_msg)

    except requests.RequestException as e:
        raise BymaDataAPIError("An error ocurred when processing the request.") from e

    except:
        raise BymaDataAPIError("An unexpected error ocurred") from e



def _validate_params(service, **kwargs):

    PARAMETERS = {
    "equity" : EquityParameters,
    "fixed_income" : FixedIncomeParameters,
    "futures" : FuturesParameters,
    "options" : OptionsParameters,
    "collateralized_repos" : ReposParameters,
    "trading_lots" : TradingLotsParameters,
    "loans" : LoansParameters,
    # "intraday" : IntradayOpsParameters
    }

    validator = PARAMETERS.get(service)

    required_params = list(validator.Required.keys())

    try:
        unrequired_params = list(validator.NotRequired.keys())
    except AttributeError:
        pass

    # Check if all required parameters are present
    missing_params = [param for param in required_params if param not in kwargs]
    if missing_params:
        raise ValueError(f"Missing required parameters: {listring(missing_params)}")

    for key, value in kwargs.items():
        
        if key in required_params:
            _valids = [val.value for val in validator.Required.get(key).__members__.values()]
        elif unrequired_params and key in unrequired_params:
            _valids = [val.value for val in validator.NotRequired.get(key).__members__.values()]
        else:
            raise ValueError(f"Unknown parameter: {key}")
        
        if key in required_params:
            if not value in _valids:
                raise ValueError("Invalid value for {_key} parameter: {_value}. Must be one of {_vals}".format(
                        _key=key, _value=value, _vals=listring(_valids)
                    )    
                )
            
        elif key in unrequired_params:
            if not value in _valids:
                raise ValueError("Invalid value for {_key} parameter: {_value}. Must be one of {_vals}".format(
                        _key=key, _value=value, _vals=listring(_valids)
                    )    
                )


def validate_params(service, validator=_validate_params, ignore=None):
    """
    Parameter validation decorator
    """
    if ignore is None:
        ignore = []

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Prepare arguments for validation
            bound_args = signature(func).bind(*args, **kwargs)
            bound_args.apply_defaults()
            arguments = bound_args.arguments

            # Exclude 'self' and ignored parameters
            validated_args = {k: v for k, v in arguments.items() if v is not None and k != 'self' and k not in ignore}

            # Run validation
            validator(service=service, **validated_args)

            return func(*args, **kwargs)

        return wrapper

    return decorator

