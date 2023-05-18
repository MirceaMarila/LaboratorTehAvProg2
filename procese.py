from multiprocessing import Pool
from multiprocessing import Process
from multiprocessing import Manager


def task(x):
    return x ** 2


def task_m(x, id, m_d):
    m_d[id] = x ** 2


def solve_with_processes(numbers):

    processes = list()
    manager = Manager()
    m_d = manager.dict()

    for id, x in enumerate(numbers):
        p = Process(target=task_m, args=(x, id, m_d))
        processes.append(p)
    
    for p in processes:
        p.start()
    
    for p in processes:
        p.join()

    return [m_d[key] for key in m_d]


def solve_with_pool(numbers):
    with Pool(12) as p:
        result = p.map(task, numbers)

    return result


def main():
    numbers = list(range(10))

    print(f"Patratul numerelor fara procese: {list(map(task, numbers))}")

    print("\n######################################\n")

    print(f"Patratul numerelor cu procese: {solve_with_processes(numbers)}")

    print("\n#######################################\n")

    print(f"Patratul numerelor cu Pool: {solve_with_pool(numbers)}")


if __name__ == "__main__":
    main()
