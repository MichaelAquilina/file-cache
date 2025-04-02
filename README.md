# Description

Function decorator you can use to cache the results of your function calls. Works similarly to the `functools.cache` decorator but maintains state between different runs.

# Usage

```python
from file_cache import file_cache


@file_cache()
def my_io_intensive_function():
    ...
```

# How does it work?

When a function call is made, the input arguments are hashed. If that hash exists on your local file cache, the contents are deserialized and the function returns those values. If the hash does not exist, then the function is called as normal and the result is stored for the next time.

Cache content is stored in the `.file-cache` local directory of your project. You probably want to add that to your `.gitignore`!

# How stable is this?

Its not been tested by any unit tests but I've used this quite frequently during various hackathons without much issue.

# What is this useful for?

This decorator is particularly useful to avoid making requests where you are performing network requests (e.g. API calls) and want to avoid being throttled or being charged for what is essentially the exact same request you made before.
