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
from .errors import DownloadNotActive, InvalidId


class Downloader:
    def __init__(self, chunk_size=None, download_path=None):
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

            # just init things otherwise it will throw keyerror :
            self._alldownloads[_uuid]["iscancel"] = False

        except Exception as e:
            raise Exception(e)
        return _uuid

    # To check If Download Is active
    async def is_active(self, uuid):
        try:
            _tempobj = self._alldownloads[uuid]["obj"]
        except KeyError:
            raise InvalidId()

        return not _tempobj.task.done()

    # Get Status
    async def status(self, uuid):
        try:
            _tempobj = self._alldownloads[uuid]["obj"]
        except KeyError:
            raise InvalidId()
        return await _tempobj.getStatus()

    #Cancel your Download

    async def cancel(self, uuid):
        try:
            _tempobj = self._alldownloads[uuid]["obj"]

            # mark as cancelled
            self._alldownloads[uuid]["iscancel"] = True
            _tempobj._cancelled = True

            cancelstatus = await _tempobj.cancel(uuid) or False

        except KeyError:
            raise InvalidId()

        if _tempobj.task.done():

            raise DownloadNotActive(f"{uuid} : Download Not active")

        return cancelstatus

    async def iserror(self, uuid):
        try:
            _tempobj = self._alldownloads[uuid]["obj"]
            _iscancel = self._alldownloads[uuid]["iscancel"]

            if _iscancel:
                return f"{uuid} Cancelled"
        except KeyError:
            raise InvalidId()

        return _tempobj.iserror
