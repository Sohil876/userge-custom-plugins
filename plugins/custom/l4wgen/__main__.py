""" Generate streaming links from live4wap.xyz page """

# By @Sohil876

from requests import get
from bs4 import BeautifulSoup
from pyrogram.enums import ParseMode
from userge import userge, Message


async def gen_links(page_url):
    page = await get(page_url)
    soup = BeautifulSoup(page.text, "html.parser")
    soup = soup.find("div", {"class": "vdo-ct"})
    soup = soup.find("source")
    soup = soup["src"]
    base_url = soup.split("master", 1)[0]
    url = await get(soup)
    data = url.text.split('\n')
    msg = "<strong>Generated Links:</strong>\n"
    # Generate real urls
    for idx, item in enumerate(data):
        if "1920x1080" in item:
            msg = msg + f"<a href={base_url + data[idx + 1]}  * 1920x1080 (1080p):\n>"
        if "1280x720" in item:
            msg = msg + f"<a href={base_url + data[idx + 1]}  * 1280x720 (720p):\n>"
        if "640x360" in item:
            msg = msg + f"<a href={base_url + data[idx + 1]}  * 640x360:\n>"
        if "480x270" in item:
            msg = msg + f"<a href={base_url + data[idx + 1]}  * 480x270:\n>"
        if "320x180" in item:
            msg = msg + f"<a href={base_url + data[idx + 1]}  * 320x180:\n>"
    return msg


@userge.on_cmd(
    "l4wgen",
    about={
        "header": "Generate streaming links from live4wap.xyz page",
        "usage": "{tr}l4wgen https://live4wap.xyz/SomepageContainingMediaStream",
    },
)
async def servers_(message: Message):
    arg_url = message.filtered_input_str
    if not arg_url:
        await message.err(text="You need to send a link from live4wap to proceed, see usage.")
        return
    if "live4wap" not in arg_url:
        await message.err(text="Invalid url! Only send live4wap link.")
        return
    await message.edit("Generating links ...")
    msg = await gen_links(page_url=arg_url)
    await message.edit(msg, parse_mode=ParseMode.HTML, disable_web_page_preview=True)