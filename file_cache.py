import json
import functools
import hashlib
import time
from pathlib import Path
from typing import Any, Callable


# caches data to a local file
# for re-use between runs when working with urls
# assumes all arguments can be turned into a string
# and that the returned data is JSON serializable
def file_cache(
    log_misses: bool = False, log_hits: bool = False, log_time: bool = False
) -> Callable:
    def file_cache_wrapper(func: Callable[..., str]) -> Callable[..., str]:
        namespace = func.__module__ + ":" + func.__name__
        cache_dir = Path(".file-cache") / namespace
        cache_dir.mkdir(exist_ok=True, parents=True)
        hits = 0
        misses = 0

        @functools.wraps(func)
        def wrapped_func(*arg: Any, **kwargs: Any) -> str:
            nonlocal hits
            nonlocal misses

            t0 = time.time()
            hasher = hashlib.new("sha1")
            for a in arg:
                hasher.update(str(a).encode("utf8"))

            for k, v in kwargs.items():
                hasher.update(f"{k}={v}".encode("utf8"))

            key = hasher.hexdigest()
            path = cache_dir / key

            log_message = None
            if path.exists():
                hits += 1
                if log_hits:
                    log_message = (namespace, "Cached", key)

                output = json.loads(path.read_text())
            else:
                misses += 1
                if log_misses:
                    log_message = (namespace, "Not cached:", key)

                result = func(*arg, **kwargs)
                path.write_text(json.dumps(result))
                output = result

            hit_rate = 100 * (hits / (hits + misses))

            elapsed_time = time.time() - t0
            if log_message:
                print(*log_message, f"{hit_rate=:.2f}%", f"{elapsed_time=}")
            return output

        return wrapped_func

    return file_cache_wrapper
