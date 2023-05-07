from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def add(self, name: str, amount: int):
        pass

    @abstractmethod
    def remove(self, name, amount):
        pass

    @abstractmethod
    def get_free_space(self):
        pass

    @abstractmethod
    def get_items(self):
        pass

    @abstractmethod
    def get_unique_items_count(self):
        pass


class Store(Storage):
    def __init__(self, capacity=100):
        self._items = {}
        self._capacity = capacity

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items):
        self._items = items

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        self._items = capacity

    def add(self, name: str, amount: int):
        if self.get_free_space() > amount:
            self.items[name] = self.items.get(name, 0) + amount
        else:
            self.items[name] = self.items.get(name, 0) + self.get_free_space()

    def remove(self, name, amount):
        if self.items.get(name, 0) - amount > 0:
            self.items[name] = self.items.get(name, 0) - amount
        else:
            self.items[name] = 0

    def get_free_space(self):
        use_space = 0
        for v in self.items.values():
            use_space += v

        return self.capacity - use_space

    def get_items(self):
        return self._items

    def get_unique_items_count(self):
        unique_items = {}
        for k, v in self.items.items():
            if v == 1:
                unique_items[k] = v

        return unique_items


class Shop(Storage):
    def __init__(self, capacity=20):
        self._items = {}
        self._capacity = capacity

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items):
        self._items = items

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        self._capacity = capacity

    def add(self, name: str, amount: int):
        if self.get_free_space() > amount and len(self.items) < 5:
            self.items[name] = self.items.get(name, 0) + amount
        elif len(self.items) < 5:
            self.items[name] = self.items.get(name, 0) + self.get_free_space()


    def remove(self, name, amount):
        if self.items.get(name, 0) - amount > 0:
            self.items[name] = self.items.get(name, 0) - amount
        else:
            self.items[name] = 0

    def get_free_space(self):
        use_space = 0
        for v in self._items.values():
            use_space += v

        return self.capacity - use_space

    def get_items(self) -> dict:
        return self.items

    def get_unique_items_count(self) -> dict:
        unique_items = {}
        for k, v in self.items.items():
            if v == 1:
                unique_items[k] = v

        return unique_items


class Request:
    def __init__(self, line: str):
        list_of_data = self.parse_line(line)
        self._fromm = list_of_data[4]
        self._to = list_of_data[6]
        self._amount = int(list_of_data[1])
        self._product = list_of_data[2]

    @property
    def fromm(self):
        return self._fromm

    @property
    def to(self):
        return self._to

    @property
    def product(self):
        return self._product

    @property
    def amount(self):
        return self._amount

    def parse_line(self, line) -> list[str]:
        return line.split()

    def __repr__(self):
        return f'Доставить** {self._amount} {self._product} из {self._fromm} в {self._to}'


if __name__ == '__main__':
    shop = Shop()
    shop.add("печеньки", 3)
    shop.add("вафли", 3)
    shop.add("помидоры", 3)
    shop.add("сок", 3)
    store = Store()
    store.add("печеньки", 5)

    user_str = input()
    user_str_list = user_str.split(" ")
    user_str_list[1] = int(user_str_list[1])
    r = Request(user_str)
    for k, v in store.get_items().items():
        if k == r.product and v > r.amount:
            print("Нужное количество есть на складе")
            if len(shop.items) < 5 and shop.get_free_space() > v:
                shop.add(r.product, r.amount)
                store.remove(r.product, r.amount)
                print(f"Курьер забрал {r.amount} {r.product} со {r.fromm}")
                print(f"Курьер везет {r.amount} {r.product} со {r.fromm} в {r.to}")
                print(f"Курьер доставил {r.amount} {r.product} в {r.to}")
            else:
                print("В магазин недостаточно места, попобуйте что то другое")
        elif k == r.product:
            print("Не хватает на складе, попробуйте заказать меньше!")
        else:
            print("Такого на складе нет!")
    print("В склад хранится:")
    for k, v in store.get_items().items():
        print(f"{v} {k}")

    print("В магазин хранится:")
    for k, v in shop.get_items().items():
        print(f"{v} {k}")

