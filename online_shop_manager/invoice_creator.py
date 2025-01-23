import json
from abc import ABC, abstractmethod


# Реализуем абстрактный класс извлечения данных из .json файлов
class ReadData(ABC):
    @staticmethod
    @abstractmethod
    def read_data(*args):
        pass


# Извлекаем данные из файла о продавце
class ReadDataFromTemplateSeller(ReadData):
    @staticmethod
    def read_data():
        with open('template_seller.json', 'r', encoding='utf-8') as file:
            data = file.read()
            data = json.loads(data)
        return data


# Извлекаем данные из файла о заказе (инфо о клиенте + инфо о товарах)
class ReadDataFromClientOrder(ReadData):
    @staticmethod
    def read_data(order_id):
        with open(order_id, 'r', encoding='utf-8') as file:
            data = file.read()
            data = json.loads(data)
        return data


# Создаем класс, для просчета стоимости товаров (с учетом скидки и общую сумму заказа) Можно было сделать два разных
# класса, но в данной версии за это будет отвечать просто два разных статичных метода одного класса.
class ProductsCost:
    # amount тоже флоат, потому что может быть товар на развес, и кол-во будет 0.506, например.
    @staticmethod
    def count_sum_for_one_product(price, discount, amount):
        return "{:.2f}".format(float(price) * ((100 - float(discount)) / 100) * float(amount))

    @staticmethod
    def count_sum_for_all_products(*args):
        final_sum = []
        for x in args:
            final_sum.append(float(x))
        return "{:.2f}".format(sum(final_sum))


# Собираем всю инфу для счета в формат, который будет устраивать нас счет.
# Создаем счет для .txt форматф, в дальнейшем можно создать класс, для сохранения счета в .exel/.pdf/.word/etc.
# Данные о продавце.
class SellerDataTXT:
    @staticmethod
    def seller_data():
        data = ReadDataFromTemplateSeller.read_data()
        text = 'Seller info: \n'
        for x, y in data.items():
            text += x.capitalize().replace('_', ' ') + ': ' + y + '\n'
        return text


# Данные о клиенте + заказе. Реализовал их в одном классе, так как подтягивает инфу из номера заказа, а там у нас
# сохранена информация именно в формате данные о клиенте + данные о товарах.
class ClientDataTXT:
    def __init__(self, order_id):
        self.order_path = str(order_id) + '.json'
        self.client_data = ReadDataFromClientOrder.read_data(self.order_path)

    # В дальнейших двух методах может показаться сложный синтаксис str формата, но это сделано, чтоб в конечном счете
    # были ровно выставленны столбики и напоминали таблицу.
    def client_info(self):
        client_info = self.client_data[0]
        text = f'\nClient info: \nClient name:   {client_info["f_name"]} {client_info["l_name"]}\n' \
               f'Client phone:  {client_info["tel"]}\nClient email:  {client_info["email"]}\n'
        return text

    def client_products_data(self):
        products_data = self.client_data[1]
        totals = []
        text = ''
        for x in products_data:
            totals.append(ProductsCost.count_sum_for_one_product(x["price"], x["discount"], x["amount"]))
        for x in products_data:
            text += f'|| {x["product name"] + (" " * (15 - len(x["product name"])))} ' \
                    f'|| {x["price"] + (" " * (6 - len(x["price"])))} ' \
                    f'|| {x["discount"] + (" " * (6 - len(x["discount"])))} ' \
                    f'|| {x["amount"] + (" " * (6 - len(x["amount"])))} ' \
                    f'|| {ProductsCost.count_sum_for_one_product(x["price"], x["discount"], x["amount"])}  ||\n'
        text += 'Total price:' + (' ' * 40) + ProductsCost.count_sum_for_all_products(*totals)
        return text


# Создаем абстрактный класс, для создания счета. Далее будет класс, для сохранения счета в .txt формате, в дальнейшем
# можно создать класс, для сохранения счета в .exel/.pdf/.word/etc.
class InvoiceCreator(ABC):
    @staticmethod
    @abstractmethod
    def create_invoice(*args):
        pass


class InvoiceCreatorTXT(InvoiceCreator):
    @staticmethod
    def create_invoice(order_id):
        invoice_path = 'invoice_' + order_id + '.txt'
        with open(invoice_path, 'w', encoding='utf-8') as file:
            file.write(SellerDataTXT.seller_data())
            client_temp = ClientDataTXT(order_id)
            file.write(client_temp.client_info())
            file.write('\n|| Product name    || price  ||  disc  || amount || Total  ||\n')
            file.write(client_temp.client_products_data())


# Выставляем 3 счета по нашим заказам и сохраняем в соответствующие файлы 'invoice_000001.txt' и тд
InvoiceCreatorTXT.create_invoice('000001')
InvoiceCreatorTXT.create_invoice('000002')
InvoiceCreatorTXT.create_invoice('000003')
