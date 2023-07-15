""" Lists available servers on hax and woiden """

# Based on http://git.aqendo.eu.org/aqendo/hax_woiden_checker_python
# By @Sohil876

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from userge import userge, Message #get_collection, config


workers_url="https://seep.eu.org"


async def grab(host):
    async with ClientSession() as session:
        async with session.get(f"{workers_url}/{host}/create-vps", headers={ "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 OPR/72.0.3815.465 (Edition Yx GX)", "Referer": "{host}" }) as response:
            if response.status != 200:
                return f"Something went wrong, aiohttp could not connect to server. Error Code: {response.status}"
            soup = BeautifulSoup(await response.text(), "html.parser")
            found = soup.find(id="datacenter").find_all("option")[1:]
            if len(found) == 0:
                return "No free seats, check back later."
            else:
                result = ""
                for i in found:
                    result += f"{i.text}\n"
                return result


@userge.on_cmd(
    "servers",
    about={
        "header": "Lists available servers on hax and woiden",
        "usage": "{tr}servers",
    },
)
async def servers_(message: Message):
    await message.edit("Fetching info...")
    hservers = await grab(host="https://hax.co.id")
    wservers = await grab(host="https://woiden.id")
    await message.edit("Hax.co.id:\n" + hservers + "\n\n" + "Woiden.id:\n" + wservers, del_in=25, disable_web_page_preview=True)