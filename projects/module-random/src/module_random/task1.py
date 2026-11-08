import random

group = ["Олена", "Іван", "Марія", "Андрій", "Софія", "Дмитро"]


def run():
    for i in range(1, 6):
        print(f"Спроба {i}: {random.choice(group)}")