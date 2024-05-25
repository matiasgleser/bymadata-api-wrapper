import time
import json
import requests

from typing import Any, Dict, Callable, Optional, List
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

def ensure_token(func: Callable) -> Callable:
    """
    Decorator to ensure that the API token is valid and refreshed if necessary.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        current_time = time.time()
        if self._token is None or self._token_expiration - current_time <= 60:
            self._refresh_token()
        return func(self, *args, **kwargs)
    return wrapper

def process_response(response: requests.Response) -> Dict[str, Any]:
    """
    Process the response from the API.

    Args:
        response (requests.Response): The response object from the API request.

    Returns:
        Dict[str, Any]: The processed response data.

    Raises:
        BymaDataAPIError: If the response contains an error or unexpected status code.
        UnexpectedResponseError: If the response contains an unexpected status code.
    """
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
        raise BymaDataAPIError("An error occurred when processing the request.") from e
    except Exception:
        raise BymaDataAPIError("An unexpected error occurred")

def _validate_params(service: str, **kwargs: Any) -> None:
    """
    Validates parameters for the specified service.

    Args:
        service (str): The service name.
        **kwargs (Any): The parameters to validate.

    Raises:
        ValueError: If required parameters are missing or have invalid values.
    """
    PARAMETERS = {
        "equity": EquityParameters,
        "fixed_income": FixedIncomeParameters,
        "futures": FuturesParameters,
        "options": OptionsParameters,
        "collateralized_repos": ReposParameters,
        "trading_lots": TradingLotsParameters,
        "loans": LoansParameters,
        # "intraday": IntradayOpsParameters
    }

    validator = PARAMETERS.get(service)

    required_params = list(validator.Required.keys())

    try:
        unrequired_params = list(validator.NotRequired.keys())
    except AttributeError:
        unrequired_params = []

    # Check if all required parameters are present
    missing_params = [param for param in required_params if param not in kwargs]
    if missing_params:
        raise ValueError(f"Missing required parameters: {listring(missing_params)}")

    for key, value in kwargs.items():
        if key in required_params:
            _valids = [val.value for val in validator.Required.get(key).__members__.values()]
        elif key in unrequired_params:
            _valids = [val.value for val in validator.NotRequired.get(key).__members__.values()]
        else:
            raise ValueError(f"Unknown parameter: {key}")

        if key in required_params or key in unrequired_params:
            if value not in _valids:
                raise ValueError(f"Invalid value for {key} parameter: {value}. Must be one of {listring(_valids)}")

def validate_params(service: str, validator: Callable = _validate_params, ignore: Optional[List[str]] = None) -> Callable:
    """
    Parameter validation decorator.

    Args:
        service (str): The service name.
        validator (Callable): The validation function.
        ignore (Optional[List[str]]): List of parameters to ignore during validation.

    Returns:
        Callable: The decorator function.
    """
    if ignore is None:
        ignore = []

    def decorator(func: Callable) -> Callable:
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
