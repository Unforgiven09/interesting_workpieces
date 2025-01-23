from abc import ABC, abstractmethod
import json


# Добавил синглтон класс с номером заказа, который будет увеличивать номер заказа при создании на 1.
class OrderID:
    _order_id = 0
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(OrderID, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def increase_order_id(self):
        self._order_id += 1

    def get_order(self):
        return self._order_id


# Так как может быть несколько типов клиентов (физ лицо, юр лицо, льготники тд) - создаем абстрактный класс для клиента.
class Client(ABC):
    @abstractmethod
    def __init__(self, f_name, l_name, tel):
        pass

    @abstractmethod
    def get_info(self):
        pass


# Реализуем пока что только 1 класс для обычных клиентов.
class RegularClient(Client):
    def __init__(self, f_name, l_name, tel):
        super().__init__(f_name, l_name, tel)
        self._f_name = f_name
        self._l_name = l_name
        self._tel = tel
        self._email = ''

    @property
    def f_name(self):
        return self._f_name

    @f_name.setter
    def f_name(self, f_name):
        self._f_name = f_name

    @property
    def l_name(self):
        return self._l_name

    @l_name.setter
    def l_name(self, l_name):
        self._l_name = l_name

    @property
    def tel(self):
        return self._tel

    @tel.setter
    def tel(self, tel):
        self._tel = tel

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    def get_info(self):
        return {'f_name': self._f_name, 'l_name': self._l_name, 'tel': self._tel, 'email': self._email}


# Создание списка товаров
class ChosenProducts:
    def __init__(self):
        self._products = []

    def add_product(self, product_name, price, discount,  amount):
        self._products.append({'product name': product_name, 'price': price, 'discount': discount, 'amount': amount})

    def get_products(self):
        return self._products


# После создания клиента и добавления товаров в корзину - создаем файл с названием
# номер заказа, данными о клиенте и товарами в json формате.
# Лучше было бы сохранять в базе данных, но в данной версии мы просто сохраняем в файле для дальнейшей работы с заказом.
class OrderCreator:
    @staticmethod
    def save_order(client, products):
        # Создаем новый номер заказа и делаем его формата 6 цифр, пустые значения заполены нулями.
        order_id = OrderID()
        order_id.increase_order_id()
        new_order_id = str(order_id.get_order())
        valid_order_id = (6-len(new_order_id)) * '0' + new_order_id + '.json'
        all_info = [client.get_info(), products.get_products()]
        with open(valid_order_id, 'w', encoding='utf-8') as file:
            json.dump(all_info, file, ensure_ascii=False, indent=4)


# Создадим 3 клиентов, для каждого свою корзину и сохраним заказы
# Специально передал цену, скидку и кол-во в форматах str/int/float, чтоб дальнейший обработчик корректно считывал
client1 = RegularClient('Vladimir', 'Demchuk', '0673645987')
client1.email = 'example@gmaail.com'
chart_client1 = ChosenProducts()
chart_client1.add_product('pizza', '100', '10.5', '1')

client2 = RegularClient('Sam', 'Black', '0676354921')
client2.email = 'example2@gmaail.com'
chart_client2 = ChosenProducts()
chart_client2.add_product('pizza', '100.00', '10', '1.0')
chart_client2.add_product('coke', 10, 5.5, 2.0)

client3 = RegularClient('John', 'White', '0671567492')
client3.email = 'example3@gmaail.com'
chart_client3 = ChosenProducts()
chart_client3.add_product('pizza', '100', 10, '1')
chart_client3.add_product('burger', '80', '5', 1)
chart_client3.add_product('coke', 10.0, '0', '2')

# Сохраняем все наши три заказа в файлы '000001.json' и тд.
OrderCreator.save_order(client1, chart_client1)
OrderCreator.save_order(client2, chart_client2)
OrderCreator.save_order(client3, chart_client3)
