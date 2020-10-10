import asyncio
import urllib.parse
import cgi
import secrets
import mimetypes
import os
import aiohttp
from .utils import human_size, gen_uuid, getspeed

import aiofiles
from time import time
import socket
from contextlib import suppress


class PrivateDl:
    """
    Downloader Class
    Example :
                dl = downloader()
                task = dl.download(url)
                task.cancel()
                or dl.cancel()
    """

    def __init__(self, fake_useragent: bool = False, chunk_size = None, download_path=None):
        self.chunk_size = chunk_size
        self.total_size = 0
        self.downloaded = 0
        #get full path of file
        self.download_path = download_path
        self.download_speed = 0
        self.eta = "NaN"
        self.filename = "Unknown"
        self.url = None
        self.file_type = None
        self.session = None
        # incase if download is cancelled  we can check it here

        # both are protected bcz we don't need mutiple value to check status
        self._cancelled = False
        self._complete = False
        self.uuid = None
        self.task = None
        self.fake_useragent = fake_useragent

        self.conn = aiohttp.TCPConnector(
            family=socket.AF_INET,
            verify_ssl=False)

        # TODO add retry
        self.max_tries = 3
        self.start_time = 0
        # basically i will hold only one uuid ;)
        self.__toatal_downloads = {}
        self.real_url = None
        # error goes here
        self.iserror = None
        self.downloadedstr = 0  # 10MiB
        if fake_useragent:
            from fake_useragent import UserAgent
            ua = UserAgent(cache=False)
            self.userAgent = ua.random

        self.progress = 0

    async def download(self, url: str) -> str:

        try:
            download_obj = PrivateDl()
            __uuid = gen_uuid()
            self.uuid = __uuid
            self.url = url
            __task = asyncio.ensure_future(self.__down())

            self.__toatal_downloads[__uuid] = {}
            self.__toatal_downloads[__uuid]["obj"] = download_obj
            self.__toatal_downloads[self.uuid]["task"] = __task
            self.task = __task

            return self.uuid
        except Exception as e:
            await self.mark_done(e)
            return

    async def __down(self) -> None:

        downloaded_chunk = 0

        # incase need we need some fake User-agent
        if self.fake_useragent:
            headers = {
                "User-Agent": self.userAgent
            }
            self.session = aiohttp.ClientSession(
                headers=headers, raise_for_status=True, connector=self.conn)
        else:
            self.session = aiohttp.ClientSession(
                raise_for_status=True, connector=self.conn)
        try:
            self.filename, self.total_size, self.content_type, self.real_url = await self.__getinfo()
        except Exception as e:
            await self.mark_done(e)
            return

        try:
            async with self.session.get(self.url) as r:
                self.start_time = time()
                if self.download_path:
                    if not os.path.isdir(self.download_path):
                        try:
                            os.makedirs(self.download_path)
                        except Exception as e:
                            await self.mark_done(e)
                            return

                    self.download_path = os.path.join(
                        self.download_path, self.filename)
                else:
                    self.download_path = self.filename

                async with aiofiles.open(self.download_path, mode="wb") as f:
                    
                    if self.chunk_size:
                        async for chunk in r.content.iter_chunked(self.chunk_size):
                            await f.write(chunk)
                            downloaded_chunk += len(chunk)
                            await self.__updateStatus(downloaded_chunk)
                    else:
                        async for chunk in r.content.iter_any():
                            await f.write(chunk)
                            downloaded_chunk += len(chunk)
                            await self.__updateStatus(downloaded_chunk)
                            
        except Exception as e:

            await self.mark_done(e)
            return

        # session close
        self._complete = True

        # incase aiohtttp can't grab file size :P
        if self.total_size == 0:
            self.total_size = self.downloaded

        await self.session.close()

    async def __updateStatus(self, downloaded_chunks):
        self.downloaded = downloaded_chunks

        #update Download Speed
        self.download_speed = getspeed(self.start_time, self.downloaded)

        # Update Download progress
        try:
            self.progress = round((self.downloaded / self.total_size) * 100)
        except:
            self.progress = 0

    # @retry
    async def __getinfo(self) -> tuple:
        """ get Url Info like filename ,size and filetype """

        async with self.session.get(
                self.url,
                allow_redirects=True

        ) as response:
            # print(response)

            # Use redirected URL
            self.url = str(response.url)
            try:
                content_disposition = cgi.parse_header(
                    response.headers['Content-Disposition'])
                filename = content_disposition[1]['filename']
                filename = urllib.parse.unquote_plus(filename)
            except KeyError:
                    filename = response._real_url.name

                    if not filename:
                        guessed_extension = mimetypes.guess_extension(
                            response.headers["Content-Type"].split(";")[0])
                        filename = f"{gen_uuid(size=5)}{guessed_extension}"

            try:
                size = int(response.headers['Content-Length'])
            except KeyError:
                size = 0
            return (
                filename,
                size,
                response.headers['Content-Type'],
                response._real_url
            )

    async def getStatus(self) -> dict:
        """ :get current status:
        filename:str
        file_type :str
        total_size :int
        total_size_str : str
        downloaded :int
        downloaded_str :str
        progress:int
        download_speed:str
        complete :bool
        download_path:str

        """

        return {
            "filename": self.filename,
            "file_type": self.file_type,
            "total_size": self.total_size,
            "total_size_str": human_size(self.total_size),
            "downloaded": self.downloaded,
            "downloaded_str": human_size(self.downloaded),
            "progress": self.progress,
            "download_speed": self.download_speed,
            "complete": self._complete,
            "download_path": self.download_path,


        }

    async def mark_done(self, error):

        self.iserror = error
        await self.session.close()

        self.task.cancel()

        # supress CanceledError raised by asyncio cancel task
        with suppress(asyncio.CancelledError):
            await self.task


    async def cancel(self, uuid) -> bool:
        """ provide uuid returned by download method to cancel it
        return : bool
        """
        await self.session.close()
        # check task is active or cancelled

        if not self.task.done():
            
            __task = self.__toatal_downloads[uuid]["task"]
            __iscancel: bool = __task.cancel()

            return __iscancel
        else:
            return True
