from brownie import Contract, interface
from queue import Queue
from threading import Thread
bank = Contract.from_abi(
    name='Alpha', address='0xba5eBAf3fc1Fcca67147050Bf80462393814E54B', abi=interface.IBank.abi)
collaterals = Queue()
tasks = Queue()
KILL = 'KILL'
def query(tasks, collaterals):
    while True:
        i = tasks.get()
        if i == KILL:
            break
        debtTokens, debtAmounts = bank.getPositionDebts(i)
        if len(debtTokens) > 0:
            try:
                coll_value = bank.getCollateralETHValue(i)
                print(i, coll_value)
                collaterals.put(coll_value)
            except Exception as e:
                print(i, e)
        tasks.task_done()


def main():
    next_position_id = bank.nextPositionId()
    total = 0
    threads = []
    for i in range(next_position_id):
        tasks.put(i)
    for _ in range(30):
        t = Thread(target=query, args=(tasks,collaterals,))
        t.start()
        threads.append(t)
    tasks.join()
    tasks.put(KILL)
    while not collaterals.empty():
        coll_value = collaterals.get()
        total += coll_value
    print(total)

if __name__ == "__main__":
    main()
