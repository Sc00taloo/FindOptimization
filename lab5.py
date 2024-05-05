from random import uniform
from operator import itemgetter

class Bees:
    def __init__(self, func, scouts, elite, perspect, bees_to_elite, bees_to_persp, radius):
        self.func = func
        self.new_scouts = list()
        self.workers = list()
        self.bees = list()
        self.best_workers = [0] * bees_to_elite
        self.persp_workers = [0] * bees_to_persp
        self.best_uchastoc = [0] * elite
        self.persp_uchastoc = [0] * perspect
        self.scouts = scouts
        self.e = elite
        self.p = perspect
        self.b_elite = bees_to_elite
        self.b_persp = bees_to_persp
        self.rad = radius
        self.diametr = self.rad ** 2
        self.currect_bees = 0

    #Генерирует начальных пчёл разведчиков
    def generate_start_scouts(self, x, y):
        for i in range(self.scouts):
            po_x = uniform(-x, x)
            po_y = uniform(-y, y)
            self.new_scouts.append([po_x, po_y, self.func(po_x, po_y)])

    #Сортирует разведчиков от лучших к худшим
    def sorted_scouts(self):
        self.new_scouts = sorted(self.new_scouts, key=itemgetter(2), reverse=False)

    #Находит лучшие участки, которые нашли разведчики
    def best_uchastochek(self):
        for i in range (self.e):
            self.best_workers[i] = self.new_scouts[i]
            self.best_uchastoc[i] = self.new_scouts[i]

    #Находит перспективные участки, которые нашли разведчики
    def persp_uchastochek(self):
        for i in range (self.p):
            self.persp_workers[i] = self.new_scouts[i+self.e]
            self.persp_uchastoc[i] = self.new_scouts[i+self.e]

    def evklid(self, best1, best2):
        return ((best1[0] - best2[0]) ** 2 +(best1[1] - best2[1]) ** 2 + (best1[2] - best2[2]) ** 2) ** 0.5

    #Проверяем на близость лучших и перспективных центров
    def proferka(self):
        for i in range(self.e-1):
            for j in range(self.e):
                if (i != j):
                    if (self.evklid(self.best_workers[i], self.best_workers[j]) < ((self.diametr) * 3) ** 0.5):
                        self.best_workers[j] = self.best_workers[i].copy()
                        self.best_uchastoc[j] = self.best_uchastoc[i]

        for i in range(self.p-1):
            for j in range(self.p):
                if (i != j):
                    if (self.evklid(self.persp_workers[i], self.persp_workers[j]) < ((self.diametr) * 3) ** 0.5):
                        self.persp_workers[j] = self.persp_workers[i].copy()
                        self.persp_uchastoc[j] = self.persp_uchastoc[i]

    #Определяет кол-во пчёл
    def razmer_bees(self):
        self.bees = [0] * (len(self.new_scouts) + self.e*self.b_elite + self.p*self.b_persp)

    #Отправляет пчёл на лучшие участки
    def best_in_uchastki(self):
        self.currect_bees = 0
        for i in range(self.e):
            for _ in range(self.b_elite):
                maxX = self.best_workers[i][0] + self.rad
                maxY = self.best_workers[i][1] + self.rad
                minX = self.best_workers[i][0] - self.rad
                minY = self.best_workers[i][1] - self.rad
                po_x = uniform(minX, maxX)
                po_y = uniform(minY, maxY)
                self.bees[self.currect_bees] = [po_x, po_y, self.func(po_x, po_y)]
                self.currect_bees += 1
            #Сортирует пчёл для элитных участков
            for zx in range(i*self.b_elite, ((i+1)*self.b_elite)-1):
                for zy in range(zx, (i + 1) * self.b_elite):
                    if self.bees[zx][2] > self.bees[zy][2]:
                        self.bees[zx], self.bees[zy] = self.bees[zy], self.bees[zx]
            #Проверяет, удалось ли найти решение на данном участке, которое не хуже предыдущего.
            if self.bees[i*self.b_elite][2] > self.best_workers[i][2]:
                self.bees[(i+1)*self.b_elite-1] = self.best_workers[i]

    #Отправляет пчёл на перспективные участки
    def persp_in_uchastki(self):
        for i in range(self.p):
            for _ in range(self.b_persp):
                maxX = self.persp_workers[i][0] + self.rad
                maxY = self.persp_workers[i][1] + self.rad
                minX = self.persp_workers[i][0] - self.rad
                minY = self.persp_workers[i][1] - self.rad
                po_x = uniform(minX, maxX)
                po_y = uniform(minY, maxY)
                self.bees[self.currect_bees] = [po_x, po_y, self.func(po_x, po_y)]
                self.currect_bees += 1
            #Сортирует пчёл для перспективных участков
            for zx in range(self.e * self.b_elite + i * self.b_persp,self.e * self.b_elite + (i + 1) * self.b_persp - 1):
                for zy in range(zx, self.e * self.b_elite + (i + 1) * self.b_persp):
                    if self.bees[zx][2] > self.bees[zy][2]:
                        self.bees[zx], self.bees[zy] = self.bees[zy], self.bees[zx]

            #Проверяет, удалось ли найти решение на данном участке, которое не хуже предыдущего.
            if self.bees[self.e * self.b_elite + i * self.b_persp][2] > self.persp_workers[i][2]:
                self.bees[self.e * self.b_elite + (i+1) * self.b_persp - 1] = self.persp_workers[i]

    #Добавляет к пчёлам новых разведчиков, которые ищёт новые лучшие и перспективные участки
    def go_bees_scouts(self, x, y):
        for i in range(self.scouts):
            po_x = uniform(-x, x)
            po_y = uniform(-y, y)
            self.bees[self.currect_bees] = [po_x, po_y, self.func(po_x, po_y)]
            self.currect_bees += 1

    #Сортирует всех пчёл
    def sorted_bees_in_hive(self):
        self.bees = sorted(self.bees, key=itemgetter(2), reverse=False)

    #Получаем лучшую пчелу
    def get_best(self):
        return self.bees[0]