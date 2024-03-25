import numpy as np

#Function Easom
def easom_function(x, y):
    return -np.cos(x) * np.cos(y) * np.exp(-(x-np.pi)**2 - (y-np.pi)**2)

#Gradient function Easom
def gradient_easom(x, y):
    dx = 2*np.exp(-(x - np.pi)**2 - (y - np.pi)**2) * np.cos(x) * np.cos(y) * (x - np.pi)
    dy = 2*np.exp(-(x - np.pi)**2 - (y - np.pi)**2) * np.cos(x) * np.cos(y) * (y - np.pi)
    return dx,dy

#Function sphere
def sphere_function(x, y):
    return x**2 + y**2

#Gradeint function sphere
def gradient_sphere(x, y):
    dx = 2 * x
    dy = 2 * y
    return dx, dy

#Beale's function
def beale_function(x, y):
    return ((1.5 - x + x*y)**2 + (2.25 - x + x*(y)**2)**2 + (2.625 - x +x * (y)**3)**2)

#Gradient Beale's function
def gradient_beale(x, y):
    dx = 4 * x *(1.5 - x*y) + 2*x*(2.25 - y**2) + 2*x*(2.625 - y**3)
    dy = 2 * x**2 - 3 + 4*y*(1.5 - x*y) + 4*(y)**3 *(2.625 - x*(y)**3)
    return dx, dy

#Rasttigin's function
def rastrigin_function(x, y):
    return 20 + x**2 - 10 * np.cos(2*np.pi*x) + y**2 - 10 * np.cos(2*np.pi*y)

#Gradient Rastrigin's function
def gradient_rastrigin(x, y):
    dx = 2*x + 20 * np.pi * np.sin(2*np.pi*x)
    dy = 2*y + 20 * np.pi * np.sin(2*np.pi*y)
    return dx, dy

def himmelblau_function(x, y):
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2
