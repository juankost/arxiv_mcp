import functools
import logging
import random
import time
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


def retry_with_exponential_backoff(
    max_retries: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 3.0,
    jitter: bool = True,
):
    """
    Decorator for retrying functions with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay between retries in seconds
        exponential_base: Base for exponential backoff calculation
        jitter: Whether to add random jitter to delay times
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries == max_retries:
                        logging.error(f"Failed after {max_retries} attempts. Final error: {str(e)}")
                        raise

                    # Calculate exponential backoff delay
                    delay = min(base_delay * (exponential_base ** (retries - 1)), max_delay)

                    # Add jitter to avoid thundering herd problem
                    if jitter:
                        delay = delay * (0.5 + random.random() * 0.5)

                    logging.warning(
                        f"Attempt {retries} failed. Retrying in {delay:.2f} seconds... "
                        f"Error: {str(e)}"
                    )
                    time.sleep(delay)

            return func(*args, **kwargs)  # Final attempt

        return wrapper

    return decorator
