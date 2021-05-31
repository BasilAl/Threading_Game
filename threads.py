import concurrent.futures
import time
import random
import threading
import queue


class MyQueue(queue.Queue):
    def __init__(self, maxsize=10):
        super().__init__()
        self.maxsize = maxsize
        self.numbers = []

    def set_number(self, number):
        self.put(number)
        self.numbers.append(number)

    def get_number(self):
        return self.get()


def produce_random_numbers(q: MyQueue, maxcount: int, evnt: threading.Event):
    count = 0
    while not evnt.is_set():
        num = random.randint(1,5)
        q.set_number(num)
        count += 1
        if count > maxcount:
            event.set()


def consume_numbers(q: MyQueue, consumed: list, evnt: threading.Event):
    while not q.empty() or not evnt.is_set():
        num = q.get_number()
        time.sleep(0.1)
        consumed.append(num)


if __name__ == "__main__":
    q = MyQueue(maxsize=10)
    event = threading.Event()
    cons1 = []
    cons2 = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
        ex.submit(produce_random_numbers, q, 50, event)
        ex.submit(consume_numbers, q, cons1, event)
        ex.submit(consume_numbers, q, cons2, event)
    time.sleep(0.5)
    event.set()
    print(f'Generated Numbers: {q.numbers}')
    print(f'Numbers Consumed by Thread1 which summed up to {sum(cons1)} are: {cons1}')
    print(f'Numbers Consumed by Thread2 which summed up to {sum(cons2)} are: {cons2}')
    if (sum(cons1)>sum(cons2)):
        print("Thread1 Wins!")
    elif (sum(cons1)<sum(cons2)):
        print("Thread2 Wins!")
    else:
        print("It's a tie!")
