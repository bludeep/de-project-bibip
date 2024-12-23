def get_cars(sale_num):

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
            if sale_num != cur_num:
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


result = get_cars('20240903#KNAGM4A77D5316538')
print(result)
