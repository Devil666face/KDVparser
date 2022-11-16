import asyncio
from parser import Parser
from parser import PageParser
from parser import CardTextParser


async def get_all_categories():
    parser = Parser()
    response_text = await parser.get('https://kdvonline.ru/catalog/vafli-11')
    categories = await parser.get_categories(response_text)
    return categories


async def get_all_card_text(categories):
    card_text_list = list()
    task_list = list()
    for index,category_url in enumerate(categories):
        card = PageParser()
        task = asyncio.create_task(card.get(category_url))
        task_list.append(task)

        if int(index)%3==0:
            card_text = await asyncio.gather(*task_list)
            for card_url in card_text:
                card_text_list.append(card_url) 
            task_list.clear()

        if len(categories)-index<3:
            card_text = await asyncio.gather(*task_list)
            for card_url in card_text:
                card_text_list.append(card_url) 
            task_list.clear()

    return card_text_list

async def get_all_good_on_pages(card_page_list):
    goods_for_category = {}
    for page_list in card_page_list:
        goods_list = list()
        for page in page_list:
            # parse all goods in page_list
            pass


        goods_for_category[get_category_name(page_list=page_list)] = goods_list
    return goods_for_category
        
def get_category_name(page_list):
    cat_with_page = str(page_list[0]).split('/')[-1]
    line_split_cat = str(cat_with_page).split('-')
    return '-'.join(line_split_cat[0:len(line_split_cat)-1])

async def main():
    categories = await get_all_categories()
    card_page_list = await get_all_card_text(categories=categories)
    goods_list = await get_all_good_on_pages(card_page_list=card_page_list)
    print(goods_list)
    
    

if __name__=='__main__':
    asyncio.run(main())