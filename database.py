import django
from db.models import Category, Good


class Database:
    def __init__(self, goods_list) -> None:
        self.clear_tables()

        for category in goods_list:
            print(category)
            try:
                Category(title=category).save()
            except Exception as ex:
                    print(f'Ошибка добавления объекта {ex}')

            goods_for_category = goods_list[category]
            for goods in goods_for_category:
                for good in goods:
                    try:
                        Good(title=good[0], href=good[1], price=good[2], prefix=good[3], category=Category.objects.get(title=category)).save()
                    except Exception as ex:
                        print(f'Ошибка добавления объекта {good[0]} {good[1]} объект уже создан')

    def clear_tables(self):
        Category.objects.all().delete()
        Good.objects.all().delete()