import random


def flip_coin(times):
    results = {"орел": 0, "решка": 0}
    for _ in range(times):
        results[random.choice(["орел", "решка"])] += 1
    return results


def run():
    print("Одне підкидання:", random.choice(["орел", "решка"]))

    for times in (100, 1000):
        res = flip_coin(times)
        print(f"{times} підкидань: орел — {res['орел']}, решка — {res['решка']}")