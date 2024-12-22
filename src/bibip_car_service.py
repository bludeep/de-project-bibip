from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from datetime import datetime

class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        # Открываем файл для записи
        with open('D:/DEV/de-project-bibip/tables/models.txt', 'a+') as f:

            # Разделяем строку на части
            id = str(model).split(' ')[0].split('=')[1]
            model_name = str(model).split(
                ' ')[1].split('=')[1].replace("'", '')
            brand = str(model).split(' ')[2].split('=')[1].replace("'", '')

            # Формируем строку с данными о модели
            car_data = f'{id};{model_name};{brand}'.ljust(500)

            # Открываем файл для чтения
            with open('D:/DEV/de-project-bibip/tables/models.txt', 'r+') as d:

                # Читаем содержимое файла
                lines = d.readlines()

                # Удаляем лишние символы из строк и получаем список
                lines = list(map(str.strip, lines))

                # Проверяем, есть ли данные о модели в файле
                if car_data.strip() not in lines:
                    f.write(f'{car_data}\n')

                    # Создаём индекс для модели
                    with open('D:/DEV/de-project-bibip/tables/models_index.txt', 'a+') as i:
                        index = len(lines) + 1
                        result = f'{index};{id}'.ljust(500)
                        i.write(f'{result}\n')

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        # Открываем файл для записи
        with open('D:/DEV/de-project-bibip/tables/cars.txt', 'a+') as f:

            # Разделяем строку на части
            car = str(car)
            vin = car.split()[0].split('=')[1].replace("'", '')
            model = car.split()[1].split('=')[1]
            price = car.split()[2].split('=')[1].replace("'", '"')
            date = car[car.find('date'):car.find(car.split()[-2])
                    ].replace(' ', '').split('=')[1]
            date = f'{date[:-5]})'
            status = car.split('=')[5].split(':')[0].replace('<', '')

            # Формируем строку с данными о машине
            final_str = f'{vin};{model};{price};{date};{status}'.ljust(500)

            # Открываем файл для чтения
            with open('D:/DEV/de-project-bibip/tables/cars.txt', 'r+') as d:

                # Читаем содержимое файла
                lines = d.readlines()

                list_vins = []

                line_vin = list(map(str.strip, lines))

                for line in line_vin:
                    vins = line.split(';')[0]
                    if line not in list_vins:
                        list_vins.append(vins)

                if vin not in list_vins:
                    f.write(f'{final_str}\n')

                    # Создаём индекс для машины
                    with open('D:/DEV/de-project-bibip/tables/cars_index.txt', 'a+') as i:
                        index = len(lines) + 1
                        result = f'{index};{vin}'.ljust(500)
                        i.write(f'{result}\n')

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        # Открываем файл для записи
        with open('D:/DEV/de-project-bibip/tables/sales.txt', 'a+') as f:

            # Разделяем строку на части
            raw = str(sale)
            sale_num = raw.split(' ')[0].split(
                '=')[1].replace('"', '').replace("'", '')
            sale_vin = raw.split(' ')[1].split(
                '=')[1].replace('"', '').replace("'", '')
            date = raw[raw.find('sales_date'):raw.find(
                ' cost')].replace(' ', '').split('=')[1]
            cost = raw.split(' ')[-1].split('=')[1]

            # Формируем строку с данными о продаже
            sale_data = f'{sale_num};{sale_vin};{date};{cost}'.ljust(500)

            # Открываем файл для чтения
            with open('D:/DEV/de-project-bibip/tables/sales.txt', 'r+') as d:

                # Читаем содержимое файла
                lines = d.readlines()

                # Удаляем лишние символы из строк и получаем список
                lines = list(map(str.strip, lines))

                # Проверяем, есть ли данные о продаже в файле
                if sale_data.strip() not in lines:
                    f.write(f'{sale_data}\n')

                    # Создаём индекс для продажи
                    with open('D:/DEV/de-project-bibip/tables/sales_index.txt', 'a+') as i:
                        index = len(lines) + 1
                        result = f'{index};{sale_num}'.ljust(500)
                        i.write(f'{result}\n')

            # Открываем файл для чтения и ищем индекс по vin автомобиля
            with open('D:/DEV/de-project-bibip/tables/cars_index.txt', 'r') as t:
                lines = t.readlines()
                lines = list(map(str.strip, lines))

                for line in lines:
                    idx = int(line.split(';')[0])
                    vin = line.split(';')[1]
                    if vin == sale_vin:
                        with open('D:/DEV/de-project-bibip/tables/cars.txt', 'r+') as c:
                            c.seek((idx - 1) * 502)
                            car = c.read(501)
                            c.seek((idx - 1) * 502)

                            # Меняем статус авто на sold
                            status = car.split(';')[-1].split('.')
                            new_stat = f'{status[0]}.sold'
                            cur_stat = car.split(';')[-1].strip()
                            date = car.split(';')[3].split('(')[1].replace(')', '')
                            year, month, day = date.split(',')
                            if cur_stat != 'CarStatus.sold':
                                result = f'{car[:car.find('CarStatus')]}{
                                    new_stat}'.ljust(500)
                                c.write(f'{result}\n')
    

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        status = str(status)
        available_list = []
        with open(
                'D:/DEV/de-project-bibip/tables/cars.txt', 'r') as f:
            lines = f.readlines()
            lines = list(map(str.strip, lines))

            for line in lines:
                vi = line.split(';')[0]
                mod = line.split(';')[1]
                pric = line.split(';')[2].replace('Decimal', '').replace('("', '').replace('")', '')
                date = line.split(';')[3].split('(')[1].replace(')', '')
                year, month, day = date.split(',')
                stat = line.split(';')[-1].split('.')[1]
                print(stat, status)
                if stat == status:
                    available_list.append(
                        Car(vin=str(vi), model=int(mod), price=pric, date_start=datetime(int(year), int(month), int(day)), status=stat))
        available_list = sorted(available_list, key=lambda car: car.vin)
        return available_list

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        raise NotImplementedError

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        raise NotImplementedError

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        raise NotImplementedError

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        raise NotImplementedError
