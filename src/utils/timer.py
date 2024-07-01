import time
from functools import wraps
import logging
import tracemalloc
from threading import Lock
from logger import log


def timer_decorator(func):
    """
    Decorator that prints the execution time of the function it decorates.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        log.info(
            f"Function '{func.__name__}' took {elapsed_time:.4f} seconds to execute."
        )
        return result

    return wrapper


def advanced_timer_decorator(
    threshold=None,
    log_to_console=False,
    log_return_value=False,
    log_file="execution_times.log",
):
    """
    Advanced decorator that prints and logs the execution time, memory usage, and other details of the function it decorates.

    Args:
        threshold (float): If the execution time exceeds this value (in seconds), a warning is logged.
        log_to_console (bool): If True, logs are also printed to the console.
        log_return_value (bool): If True, the return value of the function is logged.
        log_file (str): The file where logs will be saved.
    """
    # Configure logging to file
    logging.basicConfig(
        filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s"
    )

    def decorator(func):
        execution_count = 0
        total_time = 0
        lock = Lock()

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal execution_count, total_time

            # Start tracking memory usage
            tracemalloc.start()
            start_mem = tracemalloc.take_snapshot()

            start_time = time.time()
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                logging.error(
                    f"\n Function '{func.__name__}' raised an error: {e}", exc_info=True
                )
                raise
            end_time = time.time()

            # Stop tracking memory usage
            end_mem = tracemalloc.take_snapshot()
            tracemalloc.stop()
            mem_diff = end_mem.compare_to(start_mem, "lineno")

            elapsed_time = end_time - start_time

            with lock:
                execution_count += 1
                total_time += elapsed_time
                average_time = total_time / execution_count

                log_message = (
                    f"\n Function '{func.__name__}' took {elapsed_time:.4f} seconds to execute. "
                    f"\n Called {execution_count} times."
                    f"\n Average execution time: {average_time:.4f} seconds."
                    f"\n Arguments: {args} {kwargs}. "
                )

                if threshold and elapsed_time > threshold:
                    log_message += f"\n WARNING: Execution time exceeded threshold of {threshold} seconds. "

                if log_return_value:
                    log_message += f"\n Return value: {result}. "

                # Log memory usage details
                for stat in mem_diff[:5]:  # log top 5 memory usage differences
                    log_message += f"\n Memory usage: {stat.size_diff / 1024:.1f} KiB in {stat.count_diff} blocks ({stat.traceback}) "

                logging.info(log_message)

                if log_to_console:
                    log.info(log_message)

            return result

        return wrapper

    return decorator
