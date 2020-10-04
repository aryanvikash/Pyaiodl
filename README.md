# Python Asynchronous Downloader  - pyaoidl

### Don't Use it in Production or Live Projects Currently Its Unstable
___
 [![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/aryanvikash/pyaiodl)
[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://github.com/aryanvikash/pyaiodl)
[![Open Source Love png3](https://badges.frapsoft.com/os/v3/open-source.png?v=103)](https://github.com/aryanvikash/pyaiodl)
![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https://github.com/aryanvikash/pyaiodl)
___
## Version
[![Beta badge](https://img.shields.io/badge/STATUS-BETA-red.svg)](https://github.com/aryanvikash/pyaiodl)

[![PyPI version](https://badge.fury.io/py/pyaiodl.svg)](https://badge.fury.io/py/pyaiodl)


## installation
pypi Method (recommanded)

    pip3 install pyaiodl

Github repo method
    
    pip3 install git+https://github.com/aryanvikash/pyaiodl.git


# Avalible Methods
- Downloader class Instance
   `Non-blocking , params = [fake_useragent:bool,chunk_size:int ,download_path:str] optinals`
   
        dl = Downloader()
-   Download [ `download(self.url)` ]  

        uuid = await dl.download(url)
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
        active: bool
        complete :bool
        download_path:str
        """

- is_active returns : bool [ `is_active( self,uuid )` ]` on cancel and download complete it will return False` 
    
        result = await dl.is_active(uuid)


## Usage
Example :
___

```py

import asyncio
from pyaiodl import Downloader

url = "https://speed.hetzner.de/100MB.bin"

async def main(url):
    dl = Downloader()

    try:
            #Non-blocking
        uuid = await dl.download(url)


        
        #progress
        while await dl.is_active(uuid):
        
            r = await dl.status(uuid)
            #cancel
            # await dl.cancel(uuid)
            print(f"""
        Filename: {r['filename']}
        Total : {r['total_size_str']}
        Downloaded : {r['downloaded_str']}
        Download Speed : {r['download_speed']}
        progress: {r['progress']}
         """)

            await asyncio.sleep(1)
        
        # Final filename / path
        print( "download completed : ",r['download_path'])


    except Exception as e:
        print(e)

asyncio.get_event_loop().run_until_complete(main(url))
```

___
### known Bugs -
 - Error is Not Handled Correctly

___
# TODO

- Multipart Download
- Queue Download / Parallel Downloads Limit
- Better Error Handling





## Thanks ❤️
- [aiodl](https://github.com/cshuaimin/aiodl)
- [Hasibul Kobir](https://github.com/HasibulKabir)
- [W4RR10R](https://github.com/CW4RR10R)
- [Ranaji](https://t.me/ranaji1425)

___

[![Powered badge](https://img.shields.io/badge/Powered-Aiohttp-green.svg)](https://shields.io/)