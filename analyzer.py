from db.models import Category, Good
import xlsxwriter

class Analazyer:
    def __init__(self) -> None:
        good_list = self.update_wheight_and_price(Good.objects.all())
        self.calculate_coef(good_list)
        self.save_results(Category.objects.all())
                

    def get_wheight(self, wheight, wheight_prefix):
        wheight_return = float(wheight)
        if wheight_prefix=='кг':
            return int(wheight_return*1000)
        return wheight_return

    def get_wheight_from_title(self, wheight_prefix):
        if wheight_prefix.find('кг')!=-1 and wheight_prefix.split()[0].isdigit():
            return str(int(float(wheight_prefix.split()[0])*1000))
        if wheight_prefix.find('г')!=-1 and wheight_prefix.split()[0].isdigit():
            return wheight_prefix.split()[0]
        return 0

    def update_wheight_and_price(self, good_list):
        for good in good_list:
            prefix = str(good.prefix).split()
            if len(prefix)==4:
                '''За упак 1 кг. или За кор 1 кг.'''
                wheight = self.get_wheight(wheight=prefix[2], wheight_prefix=prefix[3])
            else:
                '''За шт.'''
                wheight = self.get_wheight_from_title(wheight_prefix=good.title.split(',')[-1])

            Good.objects.filter(pk=good.pk).update(wheight=wheight, price=str(float(good.price.replace(' ₽','').replace(',','.').replace(' ',''))))
        return Good.objects.all()

    def calculate_coef(self, good_list):
        for good in good_list:
            coef = float(good.wheight)/float(good.price)
            Good.objects.filter(pk=good.pk).update(coef=coef)

    def save_results(self, cat_list):
        def check_worksheet_name(title):
            if len(title)>31:
                return ''.join(list(title)[0:31])
            return title

        def write(worksheet, write_data):
            for i,row in enumerate(write_data):
                for j,cell in enumerate(row):
                    worksheet.write(i,j,cell)

        workbook = xlsxwriter.Workbook('result.xlsx')
        for cat in cat_list:
            worksheet = workbook.add_worksheet(name=check_worksheet_name(cat.title))
            good_for_cat_write_list = [[good.title,good.href,good.price,good.wheight,good.coef] for good in Good.objects.filter(category=cat).order_by('-coef')]

            write(worksheet=worksheet, write_data=good_for_cat_write_list)

        worksheet = workbook.add_worksheet(name='All top') 
        top_of_all_goods = [[good.title,good.href,good.price,good.wheight,good.coef] for good in Good.objects.all().order_by('-coef')]
        write(worksheet=worksheet, write_data=top_of_all_goods)

        workbook.close()

    