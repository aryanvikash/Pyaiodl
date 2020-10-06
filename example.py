from pyaiodl import Downloader, errors
import asyncio
url = "https://speed.hetzner.de/100MB.bin"


async def main():
    dl = Downloader()

    # or
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

    # when loop Breaks There are 2 Possibility either Its An error Or Download Complete
    # Cancelled Is also count as error
    if await dl.iserror(uuid):
        print(await dl.iserror(uuid))

    else:
        # Final filename / path
       print("Download completed : ", r['download_path'])


asyncio.get_event_loop().run_until_complete(main())

