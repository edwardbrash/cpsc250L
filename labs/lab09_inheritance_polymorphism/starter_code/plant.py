class Plant:
    def __init__(self, name, height_cm=20):
        self.name = name
        self.height_cm = height_cm

    def care_instructions(self):
        return("Water regularly and provide adequate sunlight")

    def __str__(self):
        return(f'Plant: {self.name}, Height: {self.height_cm} cm')


class Flower(Plant):
    def __init__(self, name, height_cm=30, color="Green"):
        self.color = color
        super().__init__(name, height_cm)

    def care_instructions(self):
        return(f'Water regularly, provide full sunlight, and deadhead spent blooms.')

    def __str__(self):
        return(f'Flower: {self.name}, Height: {self.height_cm} cm, Color: {self.color}')


class Vegetable(Plant):
    def __init__(self, name, height_cm=10, harvest_days=90):
        self.harvest_days = harvest_days
        super().__init__(name, height_cm)

    def care_instructions(self):
        return(f'Water regularly and provide full sun, and fertilize every two weeks')

    def __str__(self):
        return(f'Vegetable: {self.name}, Height: {self.height_cm}cm, Harvest Days: {self.harvest_days}')
