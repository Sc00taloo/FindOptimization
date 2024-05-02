from random import uniform

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