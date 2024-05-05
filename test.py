# from random import uniform
#
#
# # Функция для вычисления значения функции
def inverse_spherical_function(x, y):
    return x**2 + y**2
#
#
# # Алгоритм роя частиц (PSO)
# def particle_swarm_optimization(objective_function, num_particles=10, max_iter=100, w=0.5, c1=0.5, c2=0.5):
#     # Инициализация частиц
#     particles = [{'position': uniform(-10, 10), 'velocity': uniform(-1, 1)} for _ in range(num_particles)]
#     best_global_position = particles[0]['position']
#
#     for _ in range(max_iter):
#         for particle in particles:
#             particle['position'] += particle['velocity']
#             particle['fitness'] = objective_function(particle['position'])
#             if particle['fitness'] < objective_function(best_global_position):
#                 best_global_position = particle['position']
#
#         for particle in particles:
#             particle['velocity'] = w * particle['velocity'] + c1 * uniform(0, 1) * (
#                         best_global_position - particle['position']) + c2 * uniform(0, 1) * (
#                                                best_global_position - particle['position'])
#
#     return best_global_position
#
#
# # Бактериальный алгоритм (BA)
# class Bacteria:
#     def __init__(self, position):
#         self.position = position
#         self.health = objective_function(position)
#
#
# def hybrid_algorithm(objective_function, num_particles=10, max_iter_pso=100, w=0.5, c1=0.5, c2=0.5,
#                      num_bacteria=10, num_iterations_ba=100, swim_length=0.1, tumble_rate=0.1):
#     # Выполняем PSO для получения начального приближения
#     initial_position = particle_swarm_optimization(objective_function, num_particles, max_iter_pso, w, c1, c2)
#
#     # Используем начальное приближение в качестве начальной популяции для BA
#     initial_bacteria = [Bacteria(initial_position) for _ in range(num_bacteria)]
#
#     # Выполняем BA для уточнения результата
#     best_position = bacterial_algorithm(objective_function, initial_bacteria, num_iterations_ba, swim_length,
#                                         tumble_rate)
#
#     return best_position
#
#
# # Измененный bacterial_algorithm с использованием начальной популяции
# def bacterial_algorithm(objective_function, initial_bacteria, num_iterations=100, swim_length=0.1, tumble_rate=0.1):
#     bacteria = initial_bacteria
#
#     for _ in range(num_iterations):
#         for bact in bacteria:
#             for _ in range(int(swim_length * 100)):
#                 new_position = bact.position + uniform(-tumble_rate, tumble_rate)
#                 new_position = max(min(new_position, 10), -10)  # Гарантируем, что позиция остается в пределах [-10, 10]
#                 new_health = objective_function(new_position)
#
#                 if new_health < bact.health:
#                     bact.position = new_position
#                     bact.health = new_health
#
#     return min(bacteria, key=lambda x: x.health).position


# Пример использования гибридного алгоритма
# best_solution = hybrid_algorithm(objective_function)
# print("Best solution:", best_solution)
# print("Objective function value:", objective_function(best_solution))


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

    def generate_start_vector(self,x,y):
        for i in range(self.bacteria):
            chemo_x = uniform(-1, 1)
            chemo_y = uniform(-1, 1)
            self.vector_chemo.append([chemo_x, chemo_y])

    def generate_start_bacteria(self, x, y):
        for i in range(self.bacteria):
            po_x = uniform(-x, x)
            po_y = uniform(-y, y)
            # chemo_x = uniform(-1, 1)
            # chemo_y = uniform(-1, 1)
            self.new_bacteria.append([po_x, po_y, self.func(po_x, po_y), self.func(po_x, po_y)])
            #self.vector_chemo.append([chemo_x, chemo_y])

    def chemotaxis(self, coef):
        for i in range (self.bacteria):
            for _ in range(self.chemo_step):
                norm = math.sqrt(self.vector_chemo[i][0] * self.vector_chemo[i][0] + self.vector_chemo[i][1] * self.vector_chemo[i][1])
                newX = self.new_bacteria[i][0] + coef * (self.vector_chemo[i][0] // norm)
                newY = self.new_bacteria[i][1] + coef * (self.vector_chemo[i][1] // norm)
                if self.new_bacteria[i][2] < self.func(newX, newY):
                    self.new_bacteria[i][0] = newX
                    self.new_bacteria[i][1] = newY
                    self.new_bacteria[i][2] = self.func(newX, newY)
                    self.new_bacteria[i][3] += self.func(newX, newY)
                else:
                    self.vector_chemo[i][0] = uniform(-1, 1)
                    self.vector_chemo[i][1] = uniform(-1, 1)

    def reproduction(self, x, y):
        self.new_bacteria = sorted(self.new_bacteria, key=itemgetter(3), reverse=False)
        for i in range(self.bacteria // 2):
            self.new_bacteria[i] = self.new_bacteria[i + self.bacteria // 2]
            self.vector_chemo[i] = self.vector_chemo[self.bacteria // 2]

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

    def sorted_health(self):
        self.new_bacteria = sorted(self.new_bacteria, key=itemgetter(3), reverse=False)
    def get_best(self):
        return sorted(self.new_bacteria, key=itemgetter(3), reverse=True)[0]

class ParticleAlgorithm:
    def __init__(self, func, particles = 10, alpha = 1.1, beta = 1.1, inertia = 0.73):
        self.new_particles = dict()
        self.velocity = dict()
        self.func = func
        self.particles = particles #кол-во частиц
        self.alpha = alpha #Альфа отвечает за локальное влияние на частицу, то есть она направляет ее к лучшему решению, найденному в ее личном опыте
        self.beta = beta #Бета отвечает за глобальное влияние и направляет частицу к лучшему решению, найденному в опыте всего стада
        self.inertia = inertia #Инерция позволяет частицам сохранять определенное направление движения и предотвращает слишком быстрые изменения.

    #Создаёт начальные частицы с произвольными значениями координат для каждой частицы.
    def generate_start(self, x, y):
        for i in range(self.particles):
            po_x = uniform(-x, x)
            po_y = uniform(-y, y)
            self.new_particles[i] = [po_x, po_y, self.func(po_x, po_y)]
        #копируем созданные частицы
        self.old_particles = self.new_particles.copy()

    #Находит лучшую частицу среди всех
    def get_best_position(self):
        return min(self.new_particles.items(), key=lambda item: item[1][2])

    #Создаёт начальную скорость для частиц (для всех начальная скорость будет равна 0.0)
    def generate_velosity(self):
        for i in range(self.particles):
            self.velocity[i] = [0.0, 0.0]

    #Функция возвращает новую скорость для одной частицы
    def new_velocity(self, velocity, particle, point_best, gbest):
        new_vel = dict()
        for i in range(2):
            r1 = uniform(0.0,self.alpha)
            r2 = uniform(0.0,self.beta)
            new_vel[i] = self.inertia * velocity[i] + r1 * (point_best[i] - particle[i]) + r2 * (gbest[1][i] - particle[i])
        return new_vel

    #Функция возвращает новую позицию для одной частицы
    def new_position(self, velocity, particle):
        x = particle[0] + velocity[0]
        y = particle[1] + velocity[1]
        return [x, y, self.func(x, y)]

    #Функция обновляет частицы и даёт им новые параметры
    def update_particles(self):
        point_best = dict()
        for i in range(self.particles):
            if self.old_particles[i][2] < self.new_particles[i][2]:
                point_best[i] = self.old_particles[i]
            else:
                self.old_particles[i] = self.new_particles[i]
                point_best[i] = self.new_particles[i]
            gbest = ParticleAlgorithm.get_best_position(self)
            #Каждая частица перемещается по пространству решений в соответствии с двумя векторами: собственной лучшей позицией и глобальной лучшей позицией
            self.velocity[i] = ParticleAlgorithm.new_velocity(self, self.velocity[i], self.new_particles[i], point_best[i], gbest)
            #Обновляет параметры (позицию) для каждой частицы по i
            self.new_particles[i] = ParticleAlgorithm.new_position(self, self.velocity[i], self.new_particles[i])


# def hybrid_algorithm(objective_function, num_particles=10, max_iter_pso=100, w=0.5, c1=0.5, c2=0.5,
#                      num_bacteria=10, num_iterations_ba=100, swim_length=0.1, tumble_rate=0.1):
#     # Выполняем PSO для получения начального приближения
#     initial_position = particle_swarm_optimization(objective_function, num_particles, max_iter_pso, w, c1, c2)
#
#     # Используем начальное приближение в качестве начальной популяции для BA
#     initial_bacteria = [Bacteria(initial_position) for _ in range(num_bacteria)]
#
#     # Выполняем BA для уточнения результата
#     best_position = bacterial_algorithm(objective_function, initial_bacteria, num_iterations_ba, swim_length,
#                                         tumble_rate)
#     return best_position

pso = ParticleAlgorithm(inverse_spherical_function, 20, 1.1, 1.1, 0.73)
pso.generate_start(5, 5)
pso.get_best_position()
pso.generate_velosity()
for i in range (25):
    pso.update_particles()
bacterias = Bacteria(inverse_spherical_function, 20, 6, 15, 25)
bacterias.generate_start_vector(5,5)
bacterias.new_bacteria = list(pso.new_particles.values())
for sublist in bacterias.new_bacteria:
    sublist.append(sublist[2])
#bacterias.generate_start_bacteria(5, 5)
for i in range(25):
    bacterias.chemotaxis(1 / (i + 1))
    bacterias.reproduction(5, 5)
    if ((i + 1) % 15 == 0):
        bacterias.elimnination(5, 5)
    bacterias.sorted_health()

print("Best solution:", bacterias.new_bacteria[0])
print("Objective function value:", inverse_spherical_function(bacterias.new_bacteria[0][0], bacterias.new_bacteria[0][1]))