import lxml
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from parser import Parser

class CardTextParser(Parser):
    async def get(self, url):
        async with aiohttp.ClientSession() as session:
            headers = {
                "Accept": "*/*",
                "User-Agent": self.get_user_agent()
            }
            print(url)
            response = await session.get(url,headers=headers)
            soup = BeautifulSoup(await response.text(), "lxml")
            all_cards = soup.find_all(class_='a6auoGJSo')
            goods_list = list()
            for card in all_cards:
                previos_sibling = card.previous
                if (str(previos_sibling).find('swiper-slide')!=-1):
                    '''Пропускаем все с классом swiper-slide'''
                else:
                    card_title = card.find(class_='f6auoGJSo').text
                    if card_title:
                        card_href = self.add_site(card.find(class_='f6auoGJSo').find('a').get('href'))
                        card_price = card.find(class_='bsLgGFlow').text
                        card_prefix = card.find(class_='csLgGFlow').text
                        # print(card_title, card_href, card_price, card_prefix)
                        goods_list.append([card_title,card_href,card_price,card_prefix])
                
            return goods_list
            