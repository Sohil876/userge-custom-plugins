""" Generate streaming links from live4wap.xyz page """

# By @Sohil876

from aiohttp import ClientSession, TCPConnector
from bs4 import BeautifulSoup
from pyrogram.enums import ParseMode
from userge import userge, Message


user_agent = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.465 (Edition Yx GX)",
    "Referer": "https://ww1.live4wap.xyz",
    "Accept-encoding": "identity"
}


async def gen_data(page_url):
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        async with session.get(f"{page_url}", headers=user_agent) as response:
            if response.status != 200: return f"Something went wrong, aiohttp could not connect to server. Error Code: {response.status}"
            soup = BeautifulSoup(await response.text(), "html.parser")
            soup = soup.find("div", {"class": "vdo-ct"})
            soup = soup.find("source")
            soup = soup["src"]
            base_url = f"https://iptvcdn.fastdl.in/t/fp/{soup.split('=ch', 1)[1]}/"
            return soup, base_url

async def gen_links(page_url, base_url):
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        async with session.get(f"{page_url}", headers=user_agent) as response:
            if response.status != 200: return f"Something went wrong, aiohttp could not connect to server. Error Code: {response.status}"
            soup = BeautifulSoup(await response.text(), "html.parser")
            data = soup.text.split('\n')
            msg = "<strong>Generated Links:</strong>\n"
            # Generate real urls
            for idx, item in enumerate(data):
                if "1920x1080" in item:
                    msg = msg + f"  * <a href={base_url + data[idx + 1]}>1920x1080 (1080p)</a>:\n"
                if "1280x720" in item:
                    msg = msg + f"  * <a href={base_url + data[idx + 1]}>1280x720 (720p)</a>:\n"
                if "640x360" in item:
                    msg = msg + f"  * <a href={base_url + data[idx + 1]}>640x360</a>:\n"
                if "480x270" in item:
                    msg = msg + f"  * <a href={base_url + data[idx + 1]}>480x270</a>:\n"
                if "320x180" in item:
                    msg = msg + f"  * <a href={base_url + data[idx + 1]}>320x180</a>:\n"
            return msg


@userge.on_cmd(
    "l4wgen",
    about={
        "header": "Generate streaming links from live4wap.xyz page",
        "usage": "{tr}l4wgen https://live4wap.xyz/SomepageContainingMediaStream",
    },
)
async def l4wgen_(message: Message):
    arg_url = message.filtered_input_str
    if not arg_url:
        await message.err(text="You need to send a link from live4wap to proceed, see usage.")
        return
    if "live4wap" not in arg_url:
        await message.err(text="Invalid url! Only send live4wap link.")
        return
    await message.edit("Generating links ...")
    url, base_url = await gen_data(page_url=arg_url)
    msg = await gen_links(page_url=url, base_url=base_url)
    await message.edit(msg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)