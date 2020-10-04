# https://github.com/cshuaimin/aiodl/blob/8c2f30eca012cea06ab244916ead569126ac0571/aiodl/utils.py#L44

import asyncio
import aiohttp
import functools
import socket


class AiodlQuitError(Exception):
    'Something caused aiodl to quit.'


class ClosedRange:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    def __iter__(self):
        yield self.begin
        yield self.end

    def __str__(self):
        return '[{0.begin}, {0.end}]'.format(self)

    # Why not __len__() ? See https://stackoverflow.com/questions/47048561/
    @property
    def size(self):
        return self.end - self.begin + 1


def retry(coro_func):
    @functools.wraps(coro_func)
    async def wrapper(self, *args, **kwargs):
        tried = 0
        while True:
            tried += 1
            try:
                return await coro_func(self, *args, **kwargs)
            except (aiohttp.ClientError, socket.gaierror) as exc:
                try:
                    msg = '%d %s' % (exc.code, exc.message)
                    # For 4xx client errors, it's no use to try again :)
                    if 400 <= exc.code < 500:
                        print(msg)
                        raise AiodlQuitError from exc
                except AttributeError:
                    msg = str(exc) or exc.__class__.__name__
                if tried <= self.max_tries:
                    sec = tried / 2
                    print('%s() failed: %s, retry in %.1f seconds (%d/%d)' %
                          (coro_func.__name__, msg,
                           sec, tried, self.max_tries)
                          )
                    await asyncio.sleep(sec)
                else:
                    print(
                        '%s() failed after %d tries: %s ' %
                        (coro_func.__name__, self.max_tries, msg)

                    )
                    raise AiodlQuitError from exc
            except asyncio.TimeoutError:
                # Usually server has a fixed TCP timeout to clean dead
                # connections, so you can see a lot of timeouts appear
                # at the same time. I don't think this is an error,
                # So retry it without checking the max retries.
                print(
                    '%s() timeout, retry in 1 second' % coro_func.__name__
                )
                await asyncio.sleep(1)

    return wrapper
