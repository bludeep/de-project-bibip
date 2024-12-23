from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from datetime import datetime
from decimal import Decimal


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
                       ].replace(' ', '').split('=')[1].replace('datetime.', '')
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
            date = f'{
                date[:-5]})'.replace('datetime.datetime(', '').replace(')', '')
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
                            date = car.split(';')[3].split(
                                '(')[1].replace(')', '')
                            year, month, day = date.split(',')
                            if cur_stat != 'CarStatus.sold':
                                result = f'{car[:car.find('CarStatus')]}{
                                    new_stat}'.ljust(500)
                                c.write(f'{result}\n')

    # Задание 3. Доступные к продаже

    def get_cars(self, status: CarStatus) -> list[Car]:
        # Открываем файл с данными автомобилей
        with open('D:/DEV/de-project-bibip/tables/cars.txt', 'r') as f:
            # Считываем строки файла в список
            lines = f.readlines()
            # Убираем символы новой строки из строк
            lines = list(map(str.strip, lines))

            # Создаём пустой список для хранения доступных автомобилей
            available_list = []

            # Проходимся по каждой строке файла
            for line in lines:
                # Разделяем строку на поля
                vi = line.split(';')[0]
                mod = line.split(';')[1]
                pric = Decimal(line.split(';')[2].replace(
                    'Decimal', '').replace('("', '').replace('")', ''))
                date = line.split(';')[3].split('(')[1].replace(')', '')
                year, month, day = date.split(',')
                stat = line.split(';')[-1].split('.')[1]

                # Проверяем, соответствует ли статус автомобиля заданному
                if stat == status:
                    # Добавляем автомобиль в список доступных
                    available_list.append(
                        Car(vin=str(vi), 
                            model=int(mod), 
                            price=float(pric), 
                            date_start=datetime(int(year), int(month), int(day)),
                              status=stat))

        # Сортируем список по VIN-номеру
        available_list = sorted(available_list, key=lambda car: car.vin)

        return available_list

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        line_number_car = None
        sales_date = None
        cost = None
        dat = None
        dat_1 = None

        with open(
                'D:/DEV/de-project-bibip/tables/cars_index.txt', 'r') as f:
            entries = f.readlines()
            entries = list(map(str.strip, entries))
            for entry in entries:
                car_vin = entry.split(';')[1]
                if car_vin == vin:
                    line_number_car = int(entry.split(';')[0])
                    break
        if line_number_car:
            with open('D:/DEV/de-project-bibip/tables/cars.txt', 'r') as f:
                f.seek((line_number_car - 1) * 502)
                lst_car = f.read(501).strip().split(';')
                model_ind = lst_car[1]
                dat = lst_car[3]
                stat = lst_car[-1].split('.')[1]
                pric = lst_car[2].replace('Decimal', '').replace(
                    '("', '').replace('")', '').replace("'", '')
                dat = lst_car[-2].strip().replace('datetime(',
                                                  '').replace(')', '').split(',')
                year_1, month_1, day_1 = dat[0], dat[1], dat[2]
                dat = datetime(int(year_1), int(month_1), int(day_1))

            with open('D:/DEV/de-project-bibip/tables/models_index.txt', 'r') as f:
                entries = f.readlines()
                entries = list(map(str.strip, entries))
                for entry in entries:
                    model_index = entry[entry.find(';') + 1:]
                    if model_ind == model_index:
                        line_number_model = int(entry[:entry.find(';')])
                        break
            with open('D:/DEV/de-project-bibip/tables/models.txt', 'r') as f:
                f.seek((line_number_model - 1) * (502))
                lst_model = f.read(501).strip().split(';')
                mode = lst_model[1]
                bran = lst_model[2]
            if stat == 'sold':
                with open('D:/DEV/de-project-bibip/tables/sales.txt', 'r') as f:
                    entries = f.readlines()
                    for entry in entries:
                        entry = entry.strip().split(';')
                        sales_date = entry[-2].strip().split(',')
                        if vin == entry[1]:
                            year, month, day = sales_date[0], sales_date[1], sales_date[2]
                            dat_1 = datetime(int(year), int(month), int(day))
                            cost = entry[3].replace('Decimal(', '').replace(
                                "'", '').replace(')', '').replace("'", '')
        else:
            return None
        return CarFullInfo(vin=car_vin, car_model_name=mode, car_model_brand=bran, price=Decimal(pric), date_start=dat, status=stat, sales_date=dat_1, sales_cost=cost)

    # Задание 5. Обновление ключевого поля

    def update_vin(self, vin: str, new_vin: str) -> Car:
        lines = None

        # Открываем файл с индексом автомобилей
        with open(
                'D:/DEV/de-project-bibip/tables/cars_index.txt', 'r+') as f:
            # Считываем строки файла в список
            lines = f.readlines()
            # Убираем символы новой строки из строк и получаем список
            lines = list(map(str.strip, lines))

            # Ищем строку и индекс с текущим VIN-номером
            for line in lines:
                ind = int(line.split(';')[0])
                old_vin = line.split(';')[1].strip()
                if vin == old_vin:
                    # Открываем файл с данными автомобиля
                    with open(
                            'D:/DEV/de-project-bibip/tables/cars.txt', 'r+') as d:

                        # Перемещаемся на нужную позицию в файле
                        d.seek((ind - 1) * 502)
                        # Читаем строку
                        cur_line = d.read(501)
                        cur_line = cur_line.split(';')
                        # Перемещаемся на нужную позицию в файле
                        d.seek((ind - 1) * 502)


                        # Записываем новый VIN-номер в файл
                        new_vins = f'{new_vin};{cur_line[1]};{cur_line[2]};{
                            cur_line[3]};{cur_line[4]}'.ljust(500)
                        d.write(f'{new_vins}')
                        # Исправляем VIN в индексе
                        new_ind = f'{ind};{new_vin}'
                        lines[ind - 1] = new_ind
        # Сортируем cars_index перед записью в файл                
        lines = sorted(lines, key=lambda x: int(x.split(';')[0]))
        # Открываем cars_index для записи
        with open(
                'D:/DEV/de-project-bibip/tables/cars_index.txt', 'w+') as c:
            for line in lines:
                line = line.ljust(500)
                c.write(f'{line}\n')

    # Задание 6. Удаление продажи

    def revert_sale(self, sales_number: str) -> Car:
        # Инициализация списков
        sales_list = []
        index_list = []
        car_vin = None

        # Чтение данных из файла sales_index
        with open('D:/DEV/de-project-bibip/tables/sales_index.txt', 'r+') as i:
            lines = i.readlines()
            lines = list(map(str.strip, lines))
            for line in lines:
                ind = int(line.split(';')[0])
                cur_num = line.split(';')[1].strip()

                # Если номер продажи не совпадает с текущим номером добавляем валидные строки
                if sales_number != cur_num:
                    with open('D:/DEV/de-project-bibip/tables/sales.txt', 'r+') as d:
                        d.seek((ind - 1) * 501)
                        cur_line = d.read(500)
                        d.seek((ind - 1) * 501)
                        cur_line = cur_line.strip()
                        sales_list.append(cur_line)
                        index_list.append(cur_num)
                else:
                    # Поиск  автомобиля в файле sales и получение VIN-номера
                    with open('D:/DEV/de-project-bibip/tables/sales.txt', 'r+') as d:
                        d.seek((ind - 1) * 501)
                        cur_line = d.read(500)
                        car_vin = cur_line.strip().split(';')[1]

            # Открытие файла cars_index для поиска индекса.
            with open('D:/DEV/de-project-bibip/tables/cars_index.txt', 'r+') as c:
                cars = c.readlines()
                for car in cars:
                    ind = int(car.split(';')[0])
                    vin = car.strip().split(';')[1]
                    # Если SALES_VIN == CAR_VIN то меняем статус
                    if vin == car_vin:
                        # Открытие файла cars для смены статуса
                        with open('D:/DEV/de-project-bibip/tables/cars.txt', 'r+') as t:
                            t.seek((ind - 1) * 502)
                            car_line = t.read(501)
                            t.seek((ind - 1) * 502)
                            car_line = car_line.strip().split(';')
                            final_str = f'{car_line[0]};{car_line[1]};{car_line[2]};{
                                car_line[3]};CarStatus.available'.ljust(500)
                            # Меняем статус автомобиля
                            t.write(f'{final_str}\n')
        # Запись данных в файл sales_index с новыми индексами
        with open('D:/DEV/de-project-bibip/tables/sales_index.txt', 'w+') as i:
            for ind, v in enumerate(index_list, 1):
                new_str = f'{ind};{v}'.ljust(500)
                i.write(f'{new_str}\n')
        # Запись валидных данных в таблицу sales
        with open('D:/DEV/de-project-bibip/tables/sales.txt', 'w+') as i:
            for v in sales_list:
                new_str = f'{v}'.ljust(500)
                i.write(f'{new_str}\n')

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        top_models = dict()
        result_list = dict()
        final_list = []


        #### Получаем машины
        cars_list = open('D:/DEV/de-project-bibip/tables/cars.txt', 'r+')
        cars = cars_list.readlines()
        cars_list.close()
        cars = list(map(str.strip, cars))
        # получаем продажи
        sales_list = open('D:/DEV/de-project-bibip/tables/sales.txt', 'r+')
        sales = sales_list.readlines()
        sales_list.close()
        sales = list(map(str.strip, sales))

        # Получаем модели
        models_list = open('D:/DEV/de-project-bibip/tables/models.txt', 'r+')
        models = models_list.readlines()
        models_list.close()
        models = list(map(str.strip, models))

        for car in cars:
            car = car.strip().split(';')
            model = car[1]
            model_2 = car[1]
            status = car[-1]
            vin = car[0]
            if model == model_2 and status != 'CarStatus.available' and status != 'CarStatus.delivery':
                if model not in top_models:
                    for sale in sales:
                        sale = sale.strip().split(';')
                        sale_vin = sale[1]
                        price = sale[3].replace("Decimal('", '').replace("')", '')
                        if sale_vin == vin:
                            top_models[model] = [Decimal(price)]
                else:
                    for sale in sales:
                        sale = sale.strip().split(';')
                        sale_vin = sale[1]
                        price = sale[3].replace("Decimal('", '').replace("')", '')
                        if sale_vin == vin:
                            top_models[model].append(Decimal(price))
        for line in models:
            line = line.strip().split(';')
            ind = line[0]
            model = line[1]
            brand = line[2]
            for key, values in top_models.items():
                if key == ind:
                    result_list[f'{model};{brand};{len(values)}'] = values

        
        
        sorted_sales_dict = {}
        for k, v in result_list.items():
            total_price = len(v)
            sorted_sales_dict[k] = {'total_sales': total_price, 'prices': v}
        sorted_sales_dict = sorted(sorted_sales_dict.items(), key=lambda x: (x[1]['total_sales'], x[1]['prices']), reverse=True)
        
        
        for i in range(3):
            # model_name, brand_name, count = sorted_sales_dict[i].split(';')
            model_nam, brand_name, count = sorted_sales_dict[i][0].split(';')
            final_list.append(ModelSaleStats(car_model_name=model_nam, brand=brand_name, sales_number=Decimal(count)))
        return final_list

