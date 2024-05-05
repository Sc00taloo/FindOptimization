import random
from operator import itemgetter
from random import uniform

class Immunity:
    def __init__(self, func, antibodie, numb_of_the_best, numb_rand_anti, clons, mut):
        self.func = func
        self.new_antibodies = list()
        self.next_antibodies = list()
        self.clones_of_best_antibodies = list()
        self.best_antibodies = list()
        self.antibodies = antibodie
        self.best = numb_of_the_best
        self.numb_rand_antibodies = numb_rand_anti
        self.clon_numb = clons
        self.mutation = mut

    #Генерирует начальные антитела
    def generate_start_antibodies(self, x, y):
        for i in range(self.antibodies):
            po_x = uniform(-x, x)
            po_y = uniform(-y, y)
            self.new_antibodies.append([po_x, po_y, self.func(po_x, po_y)])

    #Сортирует антитела от лучших к худшим
    def sorted_antibodies(self):
        self.new_antibodies = sorted(self.new_antibodies, key=itemgetter(2), reverse=False)

    #Создаёт лучших клонов антител
    def create_clones(self):
        self.clones_of_best_antibodies.clear()
        for i in range(self.best):
            for j in range(self.clon_numb):
                self.clones_of_best_antibodies.append(self.best_antibodies[i].copy())

    #Мутация осуществляется путем изменения координаты X и координаты Y
    def mutation_clone(self, max_x, max_y):
        for i in range(self.best):
            for j in range(self.clon_numb):
                ind = i * self.clon_numb + j
                self.clones_of_best_antibodies[ind][0] = self.clones_of_best_antibodies[ind][0] + self.mutation * random.uniform(-0.5, 0.5)
                self.clones_of_best_antibodies[ind][1] = self.clones_of_best_antibodies[ind][1] + self.mutation * random.uniform(-0.5, 0.5)
                self.clones_of_best_antibodies[ind][2] = self.func(self.clones_of_best_antibodies[ind][0], self.clones_of_best_antibodies[ind][1])

    #Сортирует клонов от лучших к худшим
    def sorted_clones(self):
        self.clones_of_best_antibodies = sorted(self.clones_of_best_antibodies, key=itemgetter(2), reverse=False)

    #Создаёт новую популяцию антител из клонов, а так же добавляет новые случайные антитела
    def uniting_populations(self, x,y):
        saved_antibodies = int(round(1 * self.best * self.clon_numb))
        memoried_antibodies = [self.clones_of_best_antibodies[i].copy() for i in range(saved_antibodies)]

        self.next_antibodies.clear()
        self.next_antibodies.extend(self.best_antibodies[:self.best])
        self.next_antibodies.extend(memoried_antibodies)

        for _ in range(self.numb_rand_antibodies):
            po_x = uniform(-x, x)
            po_y = uniform(-y, y)
            self.next_antibodies.append([po_x, po_y, self.func(po_x, po_y)])

    #Сортирует новую популяцию антител от лучших к худшим
    def sorted_n_anti(self):
        self.next_antibodies = sorted(self.next_antibodies, key=itemgetter(2), reverse=False)[:self.antibodies]

    #Получает лучшие антитела
    def get_best(self):
        for i in range(self.best):
            self.best_antibodies.append(self.new_antibodies[i])

    #Получает лучшие антитела, которые были получены из клонов и рандомных антител
    def get_best_next(self):
        self.best_antibodies.clear()
        for i in range(self.best):
            self.best_antibodies.append(self.next_antibodies[i])

    #Возвращает лучшую антитело
    def best_best(self):
        return self.best_antibodies[0]