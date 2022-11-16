import lxml
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from parser import Parser

class PageParser(Parser):
    async def get(self, url):
        self.url = url
        async with aiohttp.ClientSession() as session:
            headers = {
                "Accept": "*/*",
                "User-Agent": self.get_user_agent()
            }
            print(url)
            response = await session.get(url,headers=headers)
            page_link_list = await self.get_page_number(await response.text())
            # print(page_link_list)
            return page_link_list
            

    async def get_page_number(self, response_text):
        soup = BeautifulSoup(response_text, "lxml")
        page_number_list = soup.find_all(class_='cCuVgYkar')
        page_links = [page_number.get('href') for page_number in page_number_list if page_number.get('href') is not None]
        page_links_modify = list(map(self.add_site, page_links))
        page_links_modify.extend([self.url])
        return list(set(page_links_modify))