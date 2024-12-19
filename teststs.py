from datetime import datetime
from decimal import Decimal

import pytest

from bibip_car_service import CarService
from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale

def model_data():
    return [
        Model(id=1, name="Optima", brand="Kia"),
        Model(id=2, name="Sorento", brand="Kia"),
        Model(id=3, name="3", brand="Mazda"),
        Model(id=4, name="Pathfinder", brand="Nissan"),
        Model(id=5, name="Logan", brand="Renault"),
    ]

class TestCarServiceScenarios:
    def _fill_initial_data(self, service: CarService, car_data: list[Car], model_data: list[Model]) -> None:
        for model in model_data:
            service.add_model(model)