# utils/retry_handler.py

import time


# ============================================================
# CHECK RETRYABLE ERROR
# ============================================================

def is_retryable_error(error):

    error_text = str(error).lower()

    retryable_errors = [

        "timeout",
        "timed out",

        "connection",
        "connection error",
        "connection reset",

        "rate limit",
        "429",
        "too many requests",

        "500",
        "502",
        "503",
        "504",

        "internal server error",
        "bad gateway",
        "service unavailable",
        "gateway timeout",

        "temporarily unavailable",
        "temporary error",
        "server error",
    ]

    return any(
        message in error_text
        for message in retryable_errors
    )


# ============================================================
# RETRY AI FUNCTION
# ============================================================

def run_ai_with_retry(
    function,
    max_retries=3
):

    last_error = None

    for attempt in range(
        1,
        max_retries + 1
    ):

        try:

            return function()

        except Exception as error:

            last_error = error

            if not is_retryable_error(error):

                raise

            if attempt >= max_retries:

                raise

            wait_time = 2 ** (attempt - 1)

            time.sleep(wait_time)

    raise last_error
