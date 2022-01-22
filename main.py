import math
import time

from cuckoo_search import CuckooSearch

fitness_functions = (
    lambda point: -(0.1 * point[0]**2 + 0.1 * point[1]**2) + 10,
    lambda point: 10 * (math.sin(0.1 * point[0]) + math.sin(0.1 * point[1]))
)

search_bounds = (
    ((-100, -100), (100, 100)),
    ((-100, -100), (100, 100))
)

right_answers = (
    10,
    20
)

results = []
for i in range(2):
    cuckoo_search = CuckooSearch(
        population_size=50,
        dimension=2,
        fitness_function=fitness_functions[i],
        dead_part=0.25,
        search_bounds=search_bounds[i],
        generations_limit=2000,
        livable_fitness=right_answers[i]
    )
    start_time = time.time()
    res = cuckoo_search.fit()
    fin_time = time.time()
    results.append((res, fin_time - start_time))

with open('results.txt', 'w', encoding='utf-8') as f:
    for i in range(2):
        f.write(f'#{i + 1}\n')
        f.write(f'Лучший результат: {round(results[i][0][1], 2)}\n')
        f.write(f'Правильный ответ: {right_answers[i]}\n')
        f.write(f'Коэффициенты: {", ".join([str(round(c, 2)) for c in results[i][0][0]])}\n')
        f.write(f'Время вычислений: {(results[i][1]) // 60} min {round(results[i][1] % 60, 2)} sec\n')
        f.write(f'\n')
