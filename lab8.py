import math
import random
from operator import itemgetter
from random import uniform

class HybridAlgorithm:
    def __init__(self, func, barticles=10, alpha=1.1, beta=1.1, inertia=0.73, chemotaxis=10, elimination=10, elimination_numb=5):
        self.func = func
        self.barticles = barticles
        self.alpha = alpha
        self.beta = beta
        self.inertia = inertia
        self.chemotaxis_steps = chemotaxis
        self.elimination_rate = elimination
        self.elimination_numb = elimination_numb
        self.particles_data = []
        self.bacteria_data = []
        self.old_particles = []
        self.best_solution = None

    def generate_start(self, x, y):
        # Initialize particle swarm
        for i in range(self.barticles):
            po_x = uniform(-x, x)
            po_y = uniform(-y, y)
            velocity_x = 0.0
            velocity_y = 0.0
            self.particles_data.append([po_x, po_y, self.func(po_x, po_y), velocity_x, velocity_y])
        self.old_particles = self.particles_data.copy()

        # Initialize bacteria colony
        for i in range(self.barticles):
            po_x = uniform(-x, x)
            po_y = uniform(-y, y)
            chemo_x = uniform(-1, 1)
            chemo_y = uniform(-1, 1)
            self.bacteria_data.append([po_x, po_y, self.func(po_x, po_y), self.func(po_x, po_y), chemo_x, chemo_y])

    def update_particles(self):

        # Update particle swarm
        for i in range(self.barticles):
            best_global = min(self.bacteria_data, key=lambda x: x[3])
            best_particle = min(self.particles_data, key=lambda x: x[2])
            particle = self.particles_data[i]
            r1 = uniform(0.0, self.alpha)
            r2 = uniform(0.0, self.beta)
            new_velocity_x = self.inertia * particle[3] + r1 * (best_particle[0] - particle[0]) + r2 * (best_global[0] - particle[0])
            new_velocity_y = self.inertia * particle[4] + r1 * (best_particle[1] - particle[1]) + r2 * (best_global[1] - particle[1])
            new_x = particle[0] + new_velocity_x
            new_y = particle[1] + new_velocity_y
            particle[0] = new_x
            particle[1] = new_y
            particle[2] = self.func(new_x, new_y)
            particle[3] = new_velocity_x
            particle[4] = new_velocity_y

    def chemotaxis(self, coef):
        # Chemotaxis for bacteria colony
        for i in range(self.barticles):
            bacteria = self.bacteria_data[i]
            for _ in range(self.chemotaxis_steps):
                norm = math.sqrt(bacteria[4] * bacteria[4] + bacteria[5] * bacteria[5])
                new_x = bacteria[0] + coef * (bacteria[4] / norm)
                new_y = bacteria[1] + coef * (bacteria[5] / norm)
                if self.func(new_x, new_y) < bacteria[2]:
                    bacteria[0] = new_x
                    bacteria[1] = new_y
                    bacteria[2] = self.func(new_x, new_y)
                    bacteria[3] += self.func(new_x, new_y)
                else:
                    bacteria[4] = uniform(-1, 1)
                    bacteria[5] = uniform(-1, 1)

    def elimination(self, x, y):
        # Elimination-dispersal for bacteria colony
        for _ in range(self.elimination_numb):
            ver = random.random()
            idx = random.randint(0, len(self.bacteria_data) - 1)
            if ver > 0.4:
                po_x = -x + 2 * random.random() * x
                po_y = -y + 2 * random.random() * y
                self.bacteria_data[idx] = [po_x, po_y, self.func(po_x, po_y), self.func(po_x, po_y), uniform(-1, 1), uniform(-1, 1)]

    def sorted(self):
        self.bacteria_data = sorted(self.bacteria_data, key=itemgetter(3), reverse=False)
    def get_best_position(self):
        return self.bacteria_data[0]
    def get_best(self):
        return sorted(self.bacteria_data, key=itemgetter(3), reverse=True)[0]