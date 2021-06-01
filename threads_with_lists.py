import random
import threading
import time


class IntQueue:
    def __init__(self, maxsize=100):
        self.queue = []
        self.maxsize = maxsize
        self.closed = False
        self.rejected = []

    def add(self, item: int):
        time.sleep(0.001)
        if type(item) != int:
            raise TypeError('This is an integer queue - please only add integers')
        if len(self.queue) < self.maxsize:
            self.queue.append(item)
        else:
            self.rejected.append(item)

    def get(self):
        time.sleep(0.001)
        if len(self.queue) > 0:
            return self.queue.pop(0)
        else:
            if not self.closed:
                time.sleep(0.01)

    def close(self):
        self.closed = True


class Producer:
    def __init__(self, q: IntQueue, evnt: threading.Event, minimum=1, maximum=10, amount=50):
        self.Q = q
        self.stop = evnt
        self.minimum = minimum
        self.maximum = maximum
        self.produced = []
        self.counter = 0
        self.amount = amount

    def produce(self):
        while not self.Q.closed:
            num = random.randint(self.minimum, self.maximum)
            self.Q.add(num)
            self.produced.append(num)
            self.counter += 1
            if self.counter >= self.amount:
                self.Q.close()


class Consumer:
    def __init__(self, q: IntQueue, evnt: threading.Event, name=''):
        self.name = name
        self.Q = q
        self.stop = evnt
        self.consumed = []

    def consume(self):
        while not self.stop.is_set():
            num = self.Q.get()
            if type(num) == int:
                self.consumed.append(num)
            else:
                if self.Q.closed:
                    return


def main():
    q = IntQueue(maxsize=50)
    prod_stopper = threading.Event()
    cons_stopper = threading.Event()
    prod = Producer(q, prod_stopper, 1, 5, 100)
    cons1 = Consumer(q, cons_stopper, "Thread 1")
    cons2 = Consumer(q, cons_stopper, "Thread 2")

    threads = [threading.Thread(target=prod.produce, args=[]),
               threading.Thread(target=cons1.consume, args=[]),
               threading.Thread(target=cons2.consume, args=[])
               ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print(f'producer produced {len(prod.produced)} items: {prod.produced}')
    print(
        f'consumer1 consumed {len(cons1.consumed)} items that summed up to {sum(cons1.consumed)}:\n consumer1 items:'
        f' {cons1.consumed}')
    print(
        f'consumer2 consumed {len(cons2.consumed)} items that summed up to {sum(cons2.consumed)}:\n consumer2 items:'
        f' {cons2.consumed}')
    if sum(cons1.consumed) > sum(cons2.consumed):
        print("Consumer1 wins!")
    elif sum(cons1.consumed) < sum(cons2.consumed):
        print("Consumer2 wins!")
    else:
        print("It's a tie!")


if __name__ == "__main__":
    main()
