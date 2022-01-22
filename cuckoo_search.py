import numpy as np
import math
import random
import copy


class CuckooSearch:
    def __init__(self, population_size, dimension, fitness_function, dead_part, search_bounds, generations_limit,
                 livable_fitness, step_size=1, lambda_=1.5):
        self._population_size = population_size
        self._dimension = dimension
        self._nests = None
        self._cuckoo = {'eggs': None, 'fitness': None}
        self._fitness_function = fitness_function
        self._dead_count = int(dead_part * population_size)
        self._search_bounds = search_bounds
        self._generations_limit = generations_limit
        self._livable_fitness = livable_fitness
        self._step_size = step_size
        self._lambda_ = lambda_
        self._lambda_inversion_ = 1 / lambda_

    def fit(self):
        self._generate_population()
        self._sort_nests()
        generation_index = 0
        while generation_index < self._generations_limit \
                and self._nests[0]['fitness'] < self._livable_fitness:
            self._cuckoos_flight()
            self._cuckoo_worst_comparison()
            self._sort_nests()
            self._kill()
            self._reborn()
            self._sort_nests()
            generation_index += 1
        return self._nests[0]['eggs'], self._nests[0]['fitness']

    def _reborn(self):
        for i in range(self._dead_count):
            nest = self._generate_nest()
            self._nests.append(nest)

    def _kill(self):
        for i in range(self._dead_count):
            self._nests.pop()

    def _cuckoo_worst_comparison(self):
        if self._cuckoo['fitness'] > self._nests[-1]['fitness']:
            self._nests[-1] = self._cuckoo

    def _cuckoos_flight(self):
        eggs = self._in_bounds(
            self._tuples_sum(
                self._cuckoo['eggs'],
                self._tuple_multi_int(self._levy(),
                                      self._step_size)))
        fitness = self._fitness_function(eggs)
        cuckoo = {
            'eggs': eggs,
            'fitness': fitness
        }
        self._cuckoo = cuckoo

    def _in_bounds(self, coords):
        new_coords = []
        for i, coord in enumerate(coords):
            if coord > self._search_bounds[1][i]:
                new_coord = self._search_bounds[1][i]
            elif coord < self._search_bounds[0][i]:
                new_coord = self._search_bounds[0][i]
            else:
                new_coord = coord
            new_coords.append(new_coord)
        return new_coords

    @staticmethod
    def _tuples_sum(tuple_one, tuple_two):
        list_ = []
        for one, two in zip(tuple_one, tuple_two):
            list_.append(one + two)
        return tuple(list_)

    @staticmethod
    def _tuple_multi_int(tuple_, int_):
        list_ = []
        for item in tuple_:
            list_.append(item * int_)
        return tuple(list_)

    def _generate_population(self):
        some_nest = self._generate_nest()
        self._nests = [some_nest]
        for i in range(self._population_size):
            nest = self._generate_nest()
            self._nests.append(nest)
        self._cuckoo = self._generate_nest()

    def _sort_nests(self):
        self._nests.sort(key=lambda nest: nest['fitness'], reverse=True)

    def _generate_nest(self):
        eggs = self._generate_eggs()
        fitness = self._fitness_function(eggs)
        nest = {
            'eggs': eggs,
            'fitness': fitness
        }
        return nest

    def _generate_eggs(self):
        eggs_flex = []
        for i in range(self._dimension):
            egg = self._generate_random_bounds(i)
            eggs_flex.append(egg)
        return tuple(eggs_flex)

    def _generate_random_bounds(self, dimension_index):
        min_value = self._search_bounds[0][dimension_index]
        max_value = self._search_bounds[1][dimension_index]
        number = self._generate_random(min_value, max_value)
        return number

    @staticmethod
    def _generate_random(left, right):
        return left + random.random() * (right - left)

    def _levy(self):
        sigma_u_square = np.power((math.gamma(1 + self._lambda_) * np.sin(np.pi * self._lambda_ / 2))
                                  / (math.gamma((1 + self._lambda_) / 2) * np.power(2, (self._lambda_ - 1) / 2)),
                                  self._lambda_inversion_)
        sigma_v_square = 1
        u = np.random.normal(0, sigma_u_square, size=self._dimension)
        v = np.random.normal(0, sigma_v_square, size=self._dimension)
        step = u / np.power(np.fabs(v), self._lambda_inversion_)

        return tuple(step)
