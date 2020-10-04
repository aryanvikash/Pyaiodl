__all__ = ['Downloader']

# import logging
# logging.basicConfig(level=logging.DEBUG)
# log = logging.getLogger(__name__)

# Temp. removed Custom chunk size will add it later

# TODO
#  Multi-part Downloading (i don't know if it will work on every links)
#  queue Download (parallel download limiter)
# Better + Custom Error Handling


from .pyaiodl import PrivateDl


class Downloader:
    def __init__(self, chunk_size=10000, download_path=None):
        self._alldownloads = {}
        self.download_path = download_path
        # custom chunk size
        self.chunk_size = chunk_size

    async def download(self, url):
        try:
            _down = PrivateDl(chunk_size=self.chunk_size,
                              download_path=self.download_path)
            _uuid = await _down.download(url)
            self._alldownloads[_uuid] = {}
            self._alldownloads[_uuid] = {"obj": _down}

        except Exception as e:
            raise Exception(e)
        return _uuid

    async def is_active(self, uuid):
        _tempobj = self._alldownloads[uuid]["obj"]
        return _tempobj.isActive

    async def status(self, uuid):
        _tempobj = self._alldownloads[uuid]["obj"]
        return await _tempobj.getStatus()

    async def cancel(self, uuid):
        _tempobj = self._alldownloads[uuid]["obj"]
        return await _tempobj.cancel(uuid)
