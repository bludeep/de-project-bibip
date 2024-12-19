from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale


class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        file = open('D:/DEV/de-project-bibip/tables/models.txt', 'a+')
        new_value = str(model).replace(' ', ';')
        idx = 0
        # Проверка наличия дубликата перед записью
        with open('D:/DEV/de-project-bibip/tables/models.txt', 'r') as f:
            duplicate = f.readlines()
            f.close()
        for line in duplicate:
            line = line.strip()
            new_value = new_value.strip()
            if new_value == line:
                file.close()
                return model
        file.write(f'{new_value}\n')
        file.close()

        file_index = open(
            'D:/DEV/de-project-bibip/tables/models_index.txt', 'a+')

        index_value = str(model).split()[0].split('=')[-1]
        # Проверка наличия дубликата для index.txt перед записью
        duplicate_index = file_index.readlines()
        for line_index in duplicate_index:
            idx += 1
            if index_value.strip() == line_index.strip():
                file_index.close()
                return model
        file_index.write(f'{idx} {index_value}\n')
        file_index.close()

        return model

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        raise NotImplementedError

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        raise NotImplementedError

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        raise NotImplementedError

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



def sell_car(self, sale: Sale) -> Car:
        file = open('D:/DEV/de-project-bibip/tables/sales.txt', 'a+')
        new_value = str(sale).replace(' ', ';')
        with open('D:/DEV/de-project-bibip/tables/sales.txt', 'r') as f:
            duplicate = f.readlines()
            f.close()
        for line in duplicate:
            line = line.strip()
            new_value = new_value.strip()
            if new_value == line:
                file.close()
                return sale
        file.write(f'{new_value}\n')
        file.close()

        file_index = open(
            'D:/DEV/de-project-bibip/tables/sales_index.txt', 'a+')
        sale_vin = file_index.readlines()
        print(sale_vin)
        index_value = str(sale).split()[0].split('=')[-1]
        file_index.write(f'{len(duplicate)+1} {index_value}\n')