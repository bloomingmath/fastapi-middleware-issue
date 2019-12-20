# fastapi-middlware-issue
It looks like there is a problem with starlette.TestClient, Jinja2Templates and BasicHTTPMiddleware working in conjunction.

### A way to bypass the problem
In branch _podhmo_ there is a way to perform the tests without incurring in the error, proposed [here](https://github.com/tiangolo/fastapi/issues/806#issuecomment-567913676).

### A way to produce the error
I tried to make the minimal configuration to reproduce an error I get. It happens only on testing with pytest, when a middleware intercepts a template response. I see it is a rather specific problem... but it prevents me from testing my application.

This is the output of `pytest main.py`:
```python
============================================================================= test session starts ==============================================================================
platform linux -- Python 3.7.5, pytest-5.3.2, py-1.8.0, pluggy-0.13.1
rootdir: ~/fastapi-middleware-issue
collected 1 item                                                                                                                                                               

main.py F                                                                                                                                                                [100%]

=================================================================================== FAILURES ===================================================================================
_______________________________________________________________________________ test_middleware ________________________________________________________________________________

    def test_middleware():
>       response = client.get("/")

main.py:26: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
venv/lib/python3.7/site-packages/requests/sessions.py:546: in get
    return self.request('GET', url, **kwargs)
venv/lib/python3.7/site-packages/starlette/testclient.py:421: in request
    json=json,
venv/lib/python3.7/site-packages/requests/sessions.py:533: in request
    resp = self.send(prep, **send_kwargs)
venv/lib/python3.7/site-packages/requests/sessions.py:646: in send
    r = adapter.send(request, **kwargs)
venv/lib/python3.7/site-packages/starlette/testclient.py:238: in send
    raise exc from None
venv/lib/python3.7/site-packages/starlette/testclient.py:235: in send
    loop.run_until_complete(self.app(scope, receive, send))
/usr/lib/python3.7/asyncio/base_events.py:579: in run_until_complete
    return future.result()
venv/lib/python3.7/site-packages/fastapi/applications.py:140: in __call__
    await super().__call__(scope, receive, send)
venv/lib/python3.7/site-packages/starlette/applications.py:134: in __call__
    await self.error_middleware(scope, receive, send)
venv/lib/python3.7/site-packages/starlette/middleware/errors.py:178: in __call__
    raise exc from None
venv/lib/python3.7/site-packages/starlette/middleware/errors.py:156: in __call__
    await self.app(scope, receive, _send)
venv/lib/python3.7/site-packages/starlette/middleware/base.py:25: in __call__
    response = await self.dispatch_func(request, self.call_next)
main.py:14: in add_process_time_header
    response = await call_next(request)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <starlette.middleware.base.BaseHTTPMiddleware object at 0x7f732ae07510>, request = <starlette.requests.Request object at 0x7f732adba850>

    async def call_next(self, request: Request) -> Response:
        loop = asyncio.get_event_loop()
        queue = asyncio.Queue()  # type: asyncio.Queue
    
        scope = request.scope
        receive = request.receive
        send = queue.put
    
        async def coro() -> None:
            try:
                await self.app(scope, receive, send)
            finally:
                await queue.put(None)
    
        task = loop.create_task(coro())
        message = await queue.get()
        if message is None:
            task.result()
            raise RuntimeError("No response returned.")
>       assert message["type"] == "http.response.start"
E       AssertionError

venv/lib/python3.7/site-packages/starlette/middleware/base.py:47: AssertionError
============================================================================== 1 failed in 0.39s ===============================================================================
```

## A way to bypass the problem
In branch _podhmo_ there is a way to perform the tests without incurring in the error, proposed [here](https://github.com/tiangolo/fastapi/issues/806#issuecomment-567913676).