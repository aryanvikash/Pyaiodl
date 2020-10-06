# Python Asynchronous Downloader  - pyaoidl

### Don't Use it in Production or Live Projects Currently Its Unstable
___
 [![Python 3.6](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/aryanvikash/pyaiodl)
[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://github.com/aryanvikash/pyaiodl)
[![Open Source Love png3](https://badges.frapsoft.com/os/v3/open-source.png?v=103)](https://github.com/aryanvikash/pyaiodl)
![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https://github.com/aryanvikash/pyaiodl)
___
## Version
[![Beta badge](https://img.shields.io/badge/STATUS-BETA-red.svg)](https://github.com/aryanvikash/pyaiodl)

[![PyPI version](https://badge.fury.io/py/pyaiodl.svg)](https://pypi.org/project/pyaiodl/)


## installation
pypi Method (Recommended)

    pip3 install pyaiodl

Github repo method
    
    pip3 install git+https://github.com/aryanvikash/pyaiodl.git


# Available Methods
- Downloader class Instance
   `Non-blocking , params = [fake_useragent:bool,chunk_size:int ,download_path:str] optinals`
   
        dl = Downloader()
-   Download [ `download(self,url)` ]  

        uuid = await dl.download(url)
- Errors [` iserror(self, uuid) `]
    ` : Returns -  Error Or None
    , Even On cancel It returns an error "{uuid} Cancelled"`

    ```
    await dl.iserror(uuid)
    ```


- cancel [ `cancel(self, uuid)` ]

       await dl.cancel(uuid)
- Get Status [ `status(self, uuid)` ]  
    
        response = await dl.status(uuid)
        


        returns a dict

        """
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

- is_active returns : bool [ `is_active( self,uuid )` ]` - on cancel ,error , download complete  return False`
    
        result = await dl.is_active(uuid)


## Usage
Example :
___

```py

from pyaiodl import Downloader, errors
import asyncio
url = "https://speed.hetzner.de/100MB.bin"


async def main():
    dl = Downloader()
    # you can pass your
    # custom chunk size and Download Path
    # dl = Downloader(download_path="/your_dir/", chunk_size=10000)
    uuid = await dl.download(url)
    try:
        while await dl.is_active(uuid):

            r = await dl.status(uuid)

               #cancel
            if r['progress'] > 0:
                try:
                    await dl.cancel("your_uuid")
                except errors.DownloadNotActive as na:
                    print(na)


            print(f"""
            Filename: {r['filename']}
            Total : {r['total_size_str']}
            Downloaded : {r['downloaded_str']}
            Download Speed : {r['download_speed']}
            progress: {r['progress']}
             """)

            # let him breath  for a second:P
            await asyncio.sleep(1)

    # If You are putting uuid  manually Than its better handle This Exception
    except errors.InvalidId:
        print("not valid uuid")
        return

    # when loop Breaks There are 2 Possibility
    # either Its An error Or Download Complete
    # Cancelled Is also count as error
    if await dl.iserror(uuid):
        print(await dl.iserror(uuid))

    else:
        # Final filename / path
       print("Download completed : ", r['download_path'])


asyncio.get_event_loop().run_until_complete(main())

```

___
### known Bugs -
 - None Please Report :)

___
# TODO

- Multipart Download
- Queue Download / Parallel Downloads Limit
- [x] Better Error Handling





## Thanks ❤️
- [aiodl](https://github.com/cshuaimin/aiodl)
- [Hasibul Kobir](https://github.com/HasibulKabir)
- [W4RR10R](https://github.com/CW4RR10R)
- [Ranaji](https://t.me/ranaji1425)

___

[![Powered badge](https://img.shields.io/badge/Powered-Aiohttp-green.svg)](https://shields.io/)