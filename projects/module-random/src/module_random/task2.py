import random

group = ["Олена", "Іван", "Марія", "Андрій", "Софія", "Дмитро"]


def run():
    chosen = random.sample(group, 3)
    print("Обрані студенти:", chosen)