from ..utils.logger import CustomLogger
import time


def retry(tries, delay, print_excp=False, message=''):
    """
    this decorator is used to recalling a function in failure cases

    Parameters
    ----------
    tries: int required
        number of retries
    delay: int required
        delay between two consecutive try
    print_excp: bool, optional default False
        flag to whether printing the reason of exception or not
    message: str, optional default ''
        printed message after failure of all tries

    """
    cl = CustomLogger()
    cl.create_logger()

    def actual_decorator(func):
        def inner(*args, **kwargs):
            current_try = 0

            while current_try < tries:
                try:
                    result = func(*args, **kwargs)
                    return result
                    # break

                except Exception as e:
                    if print_excp:
                        cl.logger.warning(str(e))
                    current_try += 1
                    time.sleep(delay)

                if current_try == tries:
                    raise ValueError(message)

        return inner

    return actual_decorator
