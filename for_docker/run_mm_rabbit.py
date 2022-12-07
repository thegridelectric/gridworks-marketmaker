import time

from gwmm.market_maker import MarketMaker


wait = 5

for i in range(wait):
    print(f"{i}/{wait} ..")

print("1")
mm = MarketMaker()

print("2")
mm.start()

print("3")
