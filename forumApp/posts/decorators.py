import time


def measure_execution_time(view_function):
    def _wrapper(request, *args, **kwargs):
        start = time.time()
        result = view_function(request, *args, **kwargs)
        end = time.time()
        print(f"Execution time for {view_function.__name__}: {end - start}")

        return result
    return _wrapper
