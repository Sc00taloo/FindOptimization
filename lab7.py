import math
from operator import itemgetter
from random import uniform
import random

def inverse_spherical_function(x, y):
    return (x**2 + y**2) * -1

class Bacteria:
    def __init__(self, func, bacteria, chemotaxis, elimination, elimination_numb):
        self.func = func
        self.bacteria = bacteria
        self.new_bacteria = list()
        self.vector_chemo = list()
        self.elimnination_numb = elimination_numb
        self.chemo_step = chemotaxis
        self.licvid = elimination

    def generate_start_bacteria(self, x, y):
        for i in range(self.bacteria):
            po_x = uniform(-x, x)
            po_y = uniform(-y, y)
            chemo_x = uniform(-1, 1)
            chemo_y = uniform(-1, 1)
            self.new_bacteria.append([po_x, po_y, self.func(po_x, po_y), self.func(po_x, po_y)])
            self.vector_chemo.append([chemo_x, chemo_y])

    #Реализует локальную оптимизацию. Бактерии изменяют своё положение, либо плавая, либо кувыркаясь.
    def chemotaxis(self, coef):
        for i in range (self.bacteria):
            for _ in range(self.chemo_step):
                norm = math.sqrt(self.vector_chemo[i][0] * self.vector_chemo[i][0] + self.vector_chemo[i][1] * self.vector_chemo[i][1])
                newX = self.new_bacteria[i][0] + coef * (self.vector_chemo[i][0] // norm)
                newY = self.new_bacteria[i][1] + coef * (self.vector_chemo[i][1] // norm)
                #Если значение новой функции больше старой, всё хорошо, мы плывём. Иначе мы кувыркаемся -
                # перегенерируем направление вектора движения бактерии
                if self.new_bacteria[i][2] < self.func(newX, newY):
                    self.new_bacteria[i][0] = newX
                    self.new_bacteria[i][1] = newY
                    self.new_bacteria[i][2] = self.func(newX, newY)
                    self.new_bacteria[i][3] += self.func(newX, newY)
                else:
                    self.vector_chemo[i][0] = uniform(-1, 1)
                    self.vector_chemo[i][1] = uniform(-1, 1)

    #Заменяет первую половину худших на лучших
    def reproduction(self, x, y):
        self.new_bacteria = sorted(self.new_bacteria, key=itemgetter(3), reverse=False)
        for i in range(self.bacteria // 2):
            self.new_bacteria[i] = self.new_bacteria[i + self.bacteria // 2]
            self.vector_chemo[i] = self.vector_chemo[self.bacteria // 2]

    #Ликвидируем/уничтожаем t - рандомных бактерий (изменяем их значения рандомно)
    def elimnination(self, x, y):
        t = 0
        while t != self.elimnination_numb:
            ver = random.random()
            id = random.randint(0, len(self.new_bacteria) - 1)
            if ver > 0.4:
                t += 1
                po_x = -x + 2 * random.random() * x
                po_y = -y + 2 * random.random() * y
                self.new_bacteria[id] = ([po_x, po_y, self.func(po_x, po_y), self.func(po_x, po_y)])

    #Сортирует бактерий по здоровью
    def sorted_health(self):
        self.new_bacteria = sorted(self.new_bacteria, key=itemgetter(3), reverse=False)

    #Получает лучшую бактери. по здоровью
    def get_best(self):
        return sorted(self.new_bacteria, key=itemgetter(3), reverse=True)[0]