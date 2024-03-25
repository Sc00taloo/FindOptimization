import numpy as np
from random import uniform, random
def rosenbrock(x, y):
    return (1 - x)**2 + 100 * (y - x**2)**2

class GeneticAlgorithm:
    def __init__(self, func, generations=50, min_func = True, mut_chance=0.5, survive_cof=0.5, individuals=100):
        self.func = func
        self.population = dict()
        self.mut_chance = mut_chance #вероятность мутации
        self.survive_cof = survive_cof #коэффициент выживаемости
        self.generations = generations #кол-во поколений
        self.individuals = individuals #кол-ао особей
        self.min_func = min_func

    #Создаёт начальную популяцию с произвольными значениями координат для особей и значениями функции для каждой особи.
    def generate_start_population(self, x, y):
        for i in range(self.individuals):
            po_x = uniform(-x, x)
            po_y = uniform(-y, y)
            self.population[i] = [po_x, po_y, self.func(po_x, po_y)]  # Создание начальной популяции

    #Находиться лучшую особь на основе значений функции у особей в популяции.
    def get_best_individual(self):
        return min(self.population.items(), key=lambda item: item[1][2])

    #Функция, которая сортирует особей в популяции и выбирает лучших родителей для скрещивания.
    def select(self):
        #Сортировка
        sorted_pop = dict(sorted(self.population.items(), key=lambda item: item[1][2], reverse=self.min_func))
        #Вычисление количество особей, которые не выживут как процент от общего числа особей, умноженное на выживаемость.
        cof = int(self.individuals * (1 - self.survive_cof))
        #В список parents1 добавляются особи, начиная с позиции cof и заканчивая позицией cof * 2.
        parents1 = list(sorted_pop.items())[cof: cof * 2]
        #В список parents2 добавляются особи, начиная с позиции individuals-cof и до позиции individuals.
        parents2 = list(sorted_pop.items())[self.individuals - cof: self.individuals]

        i = 0
        for pop in sorted_pop.values():
            if random() > 0.5:
                #pop[0] и pop[1] координаты особи в пространстве по оси X и Y
                pop[0] = parents1[i][1][0]
                pop[1] = parents2[i][1][1]
                #pop[2] значение функции цели, вычисленное для данной особи.
                pop[2] = self.func(parents1[i][1][0], parents2[i][1][1])
            else:
                pop[0] = parents2[i][1][0]
                pop[1] = parents1[i][1][1]
                pop[2] = self.func(parents2[i][1][0], parents1[i][1][1])
            i += 1
            if i >= cof:
                break
        self.population = sorted_pop

    #Производит мутацию особей путем изменения значений координат с учетом вероятности мутации и номера текущего поколения cur_gen.
    def mutation(self, cur_gen):
        for pop in self.population.values():
            if random() < self.mut_chance:
                # pop[0] и pop[1] координаты особи в пространстве по оси X и Y
                pop[0] += (random() - 0.5) * ((self.generations - cur_gen) / self.generations)
            if random() < self.mut_chance:
                pop[1] += (random() - 0.5) * ((self.generations - cur_gen) / self.generations)
            #pop[2] значение функции цели, вычисленное для данной особи.
            pop[2] = self.func(pop[0], pop[1])