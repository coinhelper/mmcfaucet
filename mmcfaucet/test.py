import random
from decimal import Decimal


def send_to_address(address):
    list1, list2, list3 = random.uniform(0.01, 1), random.uniform(0.01, 0.5), random.uniform(0.01, 0.1)
    all = [list1, list2, list3]
    random.shuffle(all)

    amount = Decimal(str(all[0])[0:7])

    return amount


for i in range(15):
    print send_to_address('asdasd')