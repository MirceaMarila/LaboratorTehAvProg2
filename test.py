a = {1:1, 2:20}
b = {5:5, 30:30, 1:3}


a.update(b)

a = [1, 2, 3]

b = [a for _ in a]


a[0] = 2


class Coco():
    def __init__(self, x) -> None:
        self.x = x

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

from multiprocessing import Process, Lock
from multiprocessing.managers import BaseManager

class CustomManager(BaseManager):
    pass


def worker(shared_coco:Coco, lock:Lock):
    for _ in range(10):
        with lock:
            shared_coco.set_x(shared_coco.get_x() + 1)


def main():
    CustomManager.register("Coco", Coco)

    with CustomManager() as m_d:

        shared_coco = m_d.Coco(0)
        lock = Lock()

        processes = list()
        for _ in range(10):
            processes.append(Process(target=worker, args=(shared_coco, lock)))
        
        for p in processes:
            p.start()

        for p in processes:
            p.join()

        print("CEAPA")
        print(shared_coco.get_x())


if __name__ == "__main__":
    main()
