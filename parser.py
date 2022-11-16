import lxml
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class Parser:
    def __init__(self) -> None:
        pass

    def get_user_agent(self):
            user_agent = UserAgent()
            # print(user_agent.chrome)
            return 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'
            return user_agent.chrome

    async def get(self, url):
        async with aiohttp.ClientSession() as session:
            headers = {
                "Accept": "*/*",
                "User-Agent": self.get_user_agent()
            }
            print(url)
            response = await session.get(url,headers=headers)
            if response.status == 200:
                return await response.text()
            return None

    def add_site(self, category_url):
        return f'https://kdvonline.ru{category_url}'

    async def get_categories(self, response):
        soup = BeautifulSoup(response, "lxml")
        all_a_tags = soup.find_all(class_='a9ki2WaUy')
        categories = [a_tag.get('href') for a_tag in all_a_tags if a_tag.get('href') is not None]
        return list(map(self.add_site, categories))