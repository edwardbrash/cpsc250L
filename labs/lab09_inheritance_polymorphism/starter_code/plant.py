class Plant:
    def __init__(self, name, height_cm):
        self.name = name
        self.height_cm = height_cm

    def care_instructions(self):
        return "Water regularly and provide adequate sunlight."

    def __str__(self):
        return f'Plant: {self.name}, Height: {self.height_cm} cm'


class Flower(Plant):
    def __init__(self, name, height_cm, color):
        super().__init__(name, height_cm)
        self.color = color

    def care_instructions(self):
        return "Water regularly, provide full sun, and deadhead spent blooms."

    def __str__(self):
        return f'Flower: {self.name}, Height: {self.height_cm} cm, Color: {self.color}'


class Vegetable(Plant):
    def __init__(self, name, height_cm, harvest_days):
        super().__init__(name, height_cm)
        self.harvest_days = harvest_days

    def care_instructions(self):
        return "Water regularly, provide full sun, and fertilize every two weeks."

    def __str__(self):
        return f'Vegetable: {self.name}, Height: {self.height_cm} cm, Harvest in: {self.harvest_days} days'
