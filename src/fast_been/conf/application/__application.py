from fastapi import FastAPI

from slowapi import Limiter, _rate_limit_exceeded_handler as limited_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# create FastAPI application
app = FastAPI()

limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, limited_handler)
