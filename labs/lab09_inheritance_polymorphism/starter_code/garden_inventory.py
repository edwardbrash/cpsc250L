from plant import Plant, Flower, Vegetable


def main():
    plants = [
        Plant("Fern", 35),
        Flower("Rose", 45, "red"),
        Flower("Marigold", 25, "orange"),
        Vegetable("Tomato", 80, 70),
        Vegetable("Lettuce", 20, 45),
    ]

    print("Garden Inventory")
    print("----------------")

    for plant in plants:
        print(plant)
        print("Care:", plant.care_instructions())
        print()


main()
