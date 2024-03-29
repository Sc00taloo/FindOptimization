import time
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import lab1
import lab2
import lab3
import lab4

stop_flag = True

def toggle_optionmenu(event):
    if notebook.index(notebook.select()) == 1:
        function_dropdown.set_menu("График для 2 лабы")
        function_dropdown.config(state=tk.DISABLED)
        draw("График для 2 лабы")
    else:
        function_dropdown.set_menu("...", "Била", "Сферы", "Изома", "Растригина", "График для 2 лабы", "Розенброкк", "Химмельблау")
        function_dropdown.config(state=tk.NORMAL)

def button_click():
    match notebook.index(notebook.select()):
        case 0:
            search()
        case 1:
            search2()
        case 2:
            search3()
        case 3:
            search4()

#Рисует и выводит результаты
def search():
    global stop_flag
    stop_flag = True
    points_text.delete(1.0, tk.END)
    selected_function = function_var.get()
    step = step_var.get()
    tru_delay = delay_var.get()
    num_iter = points_var.get()
    startX = X_var.get()
    startY = Y_var.get()
    minnX = minX_var.get()
    maxxX = maxX_var.get()
    minnY = minY_var.get()
    maxxY = maxY_var.get()
    osiX = osiX_var.get()
    osiY = osiY_var.get()

    match selected_function:
        case "Изома":
            function = lab1.easom_function
            gradient = lab1.gradient_easom
        case "Била":
            function = lab1.beale_function
            gradient = lab1.gradient_beale
        case "Сферы":
            function = lab1.sphere_function
            gradient = lab1.gradient_sphere
        case "Растригина":
            function = lab1.rastrigin_function
            gradient = lab1.gradient_rastrigin
        case "График для 2 лабы":
            function = lab2.f
        case "Химмельблау":
            function = lab1.himmelblau_function

    x = np.linspace(minnX, maxxX, 100)
    y = np.linspace(minnY, maxxY, 100)
    X, Y = np.meshgrid(x, y)
    Z = function(X, Y)

    ax.cla()
    ax.plot_surface(X, Y, Z, cmap='twilight', alpha=0.8)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(selected_function)
    ax.set_xlim(-osiX, osiX)
    ax.set_ylim(-osiY, osiY)

    fi=function(startX, startY)
    point=ax.scatter(startX, startY, function(np.array(startX), np.array(startY)), c='r', alpha=1.0)
    canvas.draw()
    root.update()
    for i in range(num_iter-1):
        if stop_flag:
            xip,yip,fip=startX,startY,fi
            point.remove()
            grad_x, grad_y = gradient(startX, startY)
            startX -= step * grad_x
            startY -= step * grad_y
            # Сохранение результатов и обновление графика
            fi=function(startX, startY)
            point=ax.scatter(startX, startY, fi, c='r', alpha=1.0)
            points_text.insert(tk.END,f"Итерация {i + 1}:({startX:.4f}, {startY:.4f}) f= {fi:.4f}\n")
            points_text.see(tk.END)
            canvas.draw()
            root.update()
            if np.sqrt((startX - xip) ** 2 + (startY - yip) ** 2) < 0.0001 and abs(fi - fip) < 0.0001:
                break
            time.sleep(tru_delay)
        else:
            break
    # Вывод окончательного результата
    points_text.insert(tk.END, f"Итог ({startX:.4f}, {startY:.4f}) f= {fi:.4f}\n")
    points_text.see(tk.END)

def search2():
    global stop_flag
    stop_flag = True
    points_text.delete(1.0, tk.END)
    minnX = minX_var.get()
    maxxX = maxX_var.get()
    minnY = minY_var.get()
    maxxY = maxY_var.get()
    osiX = osiX_var.get()
    osiY = osiY_var.get()
    delay = delay_var2.get()

    x = np.linspace(minnX, maxxX, 100)
    y = np.linspace(minnY, maxxY, 100)
    X, Y = np.meshgrid(x, y)
    Z = lab2.f(X, Y)

    ax.cla()
    ax.plot_surface(X, Y, Z, cmap='twilight', alpha=0.8)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('График для 2 лабы')
    ax.set_xlim(-osiX, osiX)
    ax.set_ylim(-osiY, osiY)

    #Инициализация списка для хранения результатов оптимизации
    results = []

    #Вывод результатов в текстовое поле
    points_text.config(state=tk.NORMAL)
    points_text.delete(1.0, tk.END)

    x_point = []
    y_point = []
    z_point = []
    for i, point in lab2.simplex_method(5,5):
        if stop_flag:
            x_point.append(point[0])
            y_point.append(point[1])
            z_point.append(point[2])
        # Сохранение результатов и обновление графика
            results.append((point[0], point[1], i, point[2]))
            ax.scatter(point[0], point[1], point[2], c='r', alpha=1.0)
            points_text.insert(tk.END,f"Итерация {i + 1}:({point[0]:.4f}, {point[1]:.4f}) f= {point[2]:.4f}\n")
            points_text.see(tk.END)
            canvas.draw()
            root.update()
            time.sleep(delay)
        else:
            break
    # Вывод окончательного результата
    length = len(results) - 1
    points_text.insert(tk.END, f"Итог ({results[length][0]:.4f}, {results[length][1]:.4f}) f= {results[length][3]:.4f}\n")
    points_text.see(tk.END)

def search3():
    global stop_flag
    stop_flag = True
    points_text.delete(1.0, tk.END)
    minnX = minX_var.get()
    maxxX = maxX_var.get()
    minnY = minY_var.get()
    maxxY = maxY_var.get()
    osiX = osiX_var.get()
    osiY = osiY_var.get()
    delay = delay_var3.get()
    selected_function = function_var.get()
    individuals = individuals_var3.get()
    points = points_var3.get()

    match selected_function:
        case "Изома":
            function = lab1.easom_function
        case "Била":
            function = lab1.beale_function
        case "Сферы":
            function = lab1.sphere_function
        case "Растригина":
            function = lab1.rastrigin_function
        case "График для 2 лабы":
            function = lab2.f
        case "Розенброкк":
            function = lab3.rosenbrock
        case "Химмельблау":
            function = lab1.himmelblau_function

    x = np.linspace(minnX, maxxX, 100)
    y = np.linspace(minnY, maxxY, 100)
    X, Y = np.meshgrid(x, y)
    Z = function(X, Y)

    ax.cla()
    ax.plot_surface(X, Y, Z, cmap='twilight', alpha=0.8)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(selected_function)
    ax.set_xlim(-osiX, osiX)
    ax.set_ylim(-osiY, osiY)

    #Создаёт объект genetic класса GeneticAlgorithm
    genetic = lab3.GeneticAlgorithm(function, points, True, 0.6, 0.6, individuals)
    #Генерирует начальную популяцию особей
    genetic.generate_start_population(5, 5)

    for j in range(individuals):
        ax.scatter(genetic.population[j][0], genetic.population[j][1], genetic.population[j][2],c='black', alpha=0.8)
    #Находит лучшую особь
    best_individual = genetic.get_best_individual()

    ax.scatter(best_individual[1][0], best_individual[1][1], best_individual[1][2],c='red', alpha=0.8)
    canvas.draw()
    root.update()

    ax.cla()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.plot_surface(X, Y, Z, cmap='twilight', alpha=0.8)
    canvas.draw()

    #Проходит по всем поколениям points
    for i in range(points):
        if stop_flag:
            for j in range(individuals):
                ax.scatter(genetic.population[j][0], genetic.population[j][1], genetic.population[j][2], c='black', alpha=0.8)

            #Производим селекцию (отбор) особей
            genetic.select()
            #Мутируем поколение i
            genetic.mutation(i)
            #Находит лучшую особь
            best_individual = genetic.get_best_individual()
            ax.scatter(best_individual[1][0], best_individual[1][1], best_individual[1][2], c='red', alpha=0.8)
            #Сохранение результатов и обновление графика
            points_text.insert(tk.END, f"Поколение {i+1}:({best_individual[1][0]:.4f}, {best_individual[1][1]:.4f}) f= {best_individual[1][2]:.4f}\n")
            points_text.see(tk.END)
            canvas.draw()
            root.update()
            time.sleep(delay)

            ax.cla()
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.plot_surface(X, Y, Z, cmap='twilight', alpha=0.8)
            canvas.draw()
            for j in range(individuals):
                ax.scatter(genetic.population[j][0], genetic.population[j][1], genetic.population[j][2], c='black', alpha=0.8)

            #Находит лучшую особь
            best_individual = genetic.get_best_individual()
            ax.scatter(best_individual[1][0], best_individual[1][1], best_individual[1][2], c='red', alpha=0.8)
            canvas.draw()
            root.update()
        else:
            break
    # Вывод окончательного результата
    points_text.insert(tk.END,f"Итог ({best_individual[1][0]:.4f}, {best_individual[1][1]:.4f}) f= {best_individual[1][2]:.4f}\n")
    points_text.see(tk.END)

def search4():
    global stop_flag
    stop_flag = True
    points_text.delete(1.0, tk.END)
    minnX = minX_var.get()
    maxxX = maxX_var.get()
    minnY = minY_var.get()
    maxxY = maxY_var.get()
    osiX = osiX_var.get()
    osiY = osiY_var.get()
    selected_function = function_var.get()
    delay = delay_var4.get()
    points = points_var4.get()
    particles = particles_var4.get()
    alpha = alpha_var4.get()
    beta = beta_var4.get()
    inertia = inertia_var4.get()

    match selected_function:
        case "Изома":
            function = lab1.easom_function
        case "Била":
            function = lab1.beale_function
        case "Сферы":
            function = lab1.sphere_function
        case "Растригина":
            function = lab1.rastrigin_function
        case "График для 2 лабы":
            function = lab2.f
        case "Розенброкк":
            function = lab3.rosenbrock
        case "Химмельблау":
            function = lab1.himmelblau_function

    x = np.linspace(minnX, maxxX, 100)
    y = np.linspace(minnY, maxxY, 100)
    X, Y = np.meshgrid(x, y)
    Z = function(X, Y)

    ax.cla()
    ax.plot_surface(X, Y, Z, cmap='twilight', alpha=0.8)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(selected_function)
    ax.set_xlim(-osiX, osiX)
    ax.set_ylim(-osiY, osiY)

    particle = lab4.ParticleAlgorithm(function, particles, alpha, beta, inertia)
    #Генерирует начальную популяцию частиц
    particle.generate_start(5, 5)

    for j in range(particles):
        ax.scatter(particle.new_particles[j][0], particle.new_particles[j][1], particle.new_particles[j][2],c='black', alpha=0.8)
    #Находит лучшую частицу
    best_particles = particle.get_best_position()
    ax.scatter(best_particles[1][0], best_particles[1][1], best_particles[1][2],c='red', alpha=0.8)
    canvas.draw()
    root.update()

    ax.cla()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.plot_surface(X, Y, Z, cmap='twilight', alpha=0.8)
    canvas.draw()

    #Получаем начальную скорость для всех частиц
    particle.generate_velosity()

    #Итерируем N раз (points)
    for i in range(points):
        if stop_flag:
            for j in range(particles):
                ax.scatter(particle.new_particles[j][0], particle.new_particles[j][1], particle.new_particles[j][2], c='black', alpha=0.8)
            #Двигает частицы
            particle.update_particles()
            #Находит лучшую частицу
            best_particles = particle.get_best_position()
            ax.scatter(best_particles[1][0], best_particles[1][1], best_particles[1][2], c='red', alpha=0.8)
            #Сохранение результатов и обновление графика
            points_text.insert(tk.END, f"Итерация {i+1}:({best_particles[1][0]:.4f}, {best_particles[1][1]:.4f}) f= {best_particles[1][2]:.4f}\n")
            points_text.see(tk.END)
            canvas.draw()
            root.update()
            time.sleep(delay)

            ax.cla()
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.plot_surface(X, Y, Z, cmap='twilight', alpha=0.8)
            canvas.draw()
            for j in range(particles):
                ax.scatter(particle.new_particles[j][0], particle.new_particles[j][1], particle.new_particles[j][2], c='black', alpha=0.8)

            #Находит лучшую частицу
            best_particles = particle.get_best_position()
            ax.scatter(best_particles[1][0], best_particles[1][1], best_particles[1][2], c='red', alpha=0.8)
            canvas.draw()
            root.update()
        else:
            break
    # Вывод окончательного результата
    points_text.insert(tk.END,f"Итог ({best_particles[1][0]:.4f}, {best_particles[1][1]:.4f}) f= {best_particles[1][2]:.4f}\n")
    points_text.see(tk.END)

# #Рисует выбранный график
def draw(function_var):
   global stop_flag
   stop_flag = False
   minnX = minX_var.get()
   maxxX = maxX_var.get()
   minnY = minY_var.get()
   maxxY = maxY_var.get()
   osiX = osiX_var.get()
   osiY = osiY_var.get()

   match function_var:
       case "Изома":
           function = lab1.easom_function
       case "Била":
           function = lab1.beale_function
       case "Сферы":
           function = lab1.sphere_function
       case "Растригина":
           function = lab1.rastrigin_function
       case "График для 2 лабы":
           function = lab2.f
       case "Розенброкк":
           function = lab3.rosenbrock
       case "Химмельблау":
           function = lab1.himmelblau_function

   x = np.linspace(minnX, maxxX, 100)
   y = np.linspace(minnY, maxxY, 100)
   X, Y = np.meshgrid(x, y)
   Z = function(X, Y)

   ax.cla()
   ax.plot_surface(X, Y, Z, cmap='twilight', alpha=0.8)
   ax.set_xlabel('X')
   ax.set_ylabel('Y')
   ax.set_zlabel('Z')
   ax.set_title(function_var)
   ax.set_xlim(-osiX, osiX)
   ax.set_ylim(-osiY, osiY)
   canvas.draw()
   root.update()

def stop():
    global stop_flag
    stop_flag = False

# Создание окна
root = tk.Tk()
root.title("Search Engine Optimization Methods")

# Создание трехмерного графика
fig = plt.figure()
ax = plt.axes(projection='3d')

# Вставка графика в окно
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0,rowspan=30)

#Создание вкладок Лаб
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=1, columnspan=2, sticky="nsew")
style = ttk.Style()
style.configure("TNotebook.Tab", font=("Arial", 12))
frame1 = ttk.Frame(notebook)
notebook.add(frame1, text=f"Лаба 1")
frame2 = ttk.Frame(notebook)
notebook.add(frame2, text=f"Лаба 2")
frame3 = ttk.Frame(notebook)
notebook.add(frame3, text=f"Лаба 3")
frame4 = ttk.Frame(notebook)
notebook.add(frame4, text=f"Лаба 4")

##################### 1 laba #####################

start_label = tk.Label(frame1, text="Начальная настройка", font=("Arial", 16))
start_label.grid(column=1, row=0, columnspan=2)

start_labelX = tk.Label(frame1, text="Начальное X:", font=("Arial", 12))
start_labelX.grid(column=1, row=1)
X_var = tk.DoubleVar(value=1)
X_entry = ttk.Entry(frame1, textvariable=X_var)
X_entry.grid(column=2, row=1)

start_labelY = tk.Label(frame1, text="Начальное Y:", font=("Arial", 12))
start_labelY.grid(column=1, row=2)
Y_var = tk.DoubleVar(value=1)
Y_entry = ttk.Entry(frame1, textvariable=Y_var)
Y_entry.grid(column=2, row=2)

step = tk.Label(frame1, text="Шаг:", font=("Arial", 12))
step.grid(column=1, row=3)
step_var = tk.DoubleVar(value=0.01)
step_entry = ttk.Entry(frame1, textvariable=step_var)
step_entry.grid(column=2, row=3)

points_label = tk.Label(frame1, text="Количество итераций:", font=("Arial", 12))
points_label.grid(column=1, row=4)
points_var = tk.IntVar(value=100)
points_entry = ttk.Entry(frame1, textvariable=points_var)
points_entry.grid(column=2, row=4)

delay_label = tk.Label(frame1, text="Задержка:", font=("Arial", 12))
delay_label.grid(column=1, row=5)
delay_var = tk.DoubleVar(value=0.05)
delay_entry = ttk.Entry(frame1, textvariable=delay_var)
delay_entry.grid(column=2, row=5)

##################### 2 laba #####################

start_label = tk.Label(frame2, text="Начальная настройка", font=("Arial", 16))
start_label.grid(column=1, row=0, columnspan=2)

delay_label = tk.Label(frame2, text="Задержка:", font=("Arial", 12))
delay_label.grid(column=1, row=1)
delay_var2 = tk.DoubleVar(value=0.5)
delay_entry = ttk.Entry(frame2, textvariable=delay_var2)
delay_entry.grid(column=2, row=1)

#####################  3 laba  #####################

start_label = tk.Label(frame3, text="Начальная настройка", font=("Arial", 16))
start_label.grid(column=1, row=0, columnspan=2)

points_label = tk.Label(frame3, text="Количество итераций:", font=("Arial", 12))
points_label.grid(column=1, row=1)
points_var3 = tk.IntVar(value=100)
points_entry = ttk.Entry(frame3, textvariable=points_var3)
points_entry.grid(column=2, row=1)

individuals_label = tk.Label(frame3, text="Количество особей:", font=("Arial", 12))
individuals_label.grid(column=1, row=2)
individuals_var3 = tk.IntVar(value=20)
individuals_entry = ttk.Entry(frame3, textvariable=individuals_var3)
individuals_entry.grid(column=2, row=2)

delay_label = tk.Label(frame3, text="Задержка:", font=("Arial", 12))
delay_label.grid(column=1, row=3)
delay_var3 = tk.DoubleVar(value=0.01)
delay_entry = ttk.Entry(frame3, textvariable=delay_var3)
delay_entry.grid(column=2, row=3)

#####################  4 laba  #####################

start_label = tk.Label(frame4, text="Начальная настройка", font=("Arial", 16))
start_label.grid(column=1, row=0, columnspan=2)

points_label = tk.Label(frame4, text="Количество итераций:", font=("Arial", 12))
points_label.grid(column=1, row=1)
points_var4 = tk.IntVar(value=50)
points_entry = ttk.Entry(frame4, textvariable=points_var4)
points_entry.grid(column=2, row=1)

particles_label = tk.Label(frame4, text="Количество частиц:", font=("Arial", 12))
particles_label.grid(column=1, row=2)
particles_var4 = tk.IntVar(value=10)
particles_entry = ttk.Entry(frame4, textvariable=particles_var4)
particles_entry.grid(column=2, row=2)

alpha_label = tk.Label(frame4, text="Альфа:", font=("Arial", 12))
alpha_label.grid(column=1, row=3)
alpha_var4 = tk.DoubleVar(value=0.8)
alpha_entry = ttk.Entry(frame4, textvariable=alpha_var4)
alpha_entry.grid(column=2, row=3)

beta_label = tk.Label(frame4, text="Бета:", font=("Arial", 12))
beta_label.grid(column=1, row=4)
beta_var4 = tk.DoubleVar(value=0.9)
beta_entry = ttk.Entry(frame4, textvariable=beta_var4)
beta_entry.grid(column=2, row=4)

inertia_label = tk.Label(frame4, text="Инерция:", font=("Arial", 12))
inertia_label.grid(column=1, row=5)
inertia_var4 = tk.DoubleVar(value=0.5)
inertia_entry = ttk.Entry(frame4, textvariable=inertia_var4)
inertia_entry.grid(column=2, row=5)

delay_label = tk.Label(frame4, text="Задержка:", font=("Arial", 12))
delay_label.grid(column=1, row=6)
delay_var4 = tk.DoubleVar(value=0.01)
delay_entry = ttk.Entry(frame4, textvariable=delay_var4)
delay_entry.grid(column=2, row=6)

#####################    #####################

# Функции и их отображения
end_label = tk.Label(root, text="Функции и их отображения", font=("Arial", 16))
end_label.grid(column=1, row=8, columnspan=2)

function_label = tk.Label(root, text="Функция:", font=("Arial", 12))
function_label.grid(column=1,row=9)
function_var = tk.StringVar(value="...")
function_dropdown = ttk.OptionMenu(root, function_var, "...", "Била", "Сферы", "Изома", "Растригина", "График для 2 лабы", "Розенброкк", "Химмельблау", command=draw)
function_dropdown.grid(column=2,row=9)
notebook.bind('<<NotebookTabChanged>>', toggle_optionmenu)

minX = tk.Label(root, text="Минимальный интервал X", font=("Arial", 12))
minX.grid(column=1, row=10)
minX_var=tk.DoubleVar(value=-5)
minX_entry = ttk.Entry(root, textvariable=minX_var)
minX_entry.grid(column=2,row=10)
maxX = tk.Label(root, text="Максимальный интервал Y:", font=("Arial", 12))
maxX.grid(column=1, row=11)
maxX_var=tk.DoubleVar(value=5)
maxX_entry = ttk.Entry(root, textvariable=maxX_var)
maxX_entry.grid(column=2,row=11)

minY = tk.Label(root, text="Минимальный интервал Y:", font=("Arial", 12))
minY.grid(column=1, row=12)
minY_var=tk.DoubleVar(value=-5)
minY_entry = ttk.Entry(root, textvariable=minY_var)
minY_entry.grid(column=2,row=12)
maxY = tk.Label(root, text="Максимальный интервал Y:", font=("Arial", 12))
maxY.grid(column=1, row=13)
maxY_var=tk.DoubleVar(value=5)
maxY_entry = ttk.Entry(root, textvariable=maxY_var)
maxY_entry.grid(column=2,row=13)

osiX = tk.Label(root, text="Ось X интервал:", font=("Arial", 12))
osiX.grid(column=1, row=14)
osiX_var=tk.DoubleVar(value=5)
osiX_entry = ttk.Entry(root, textvariable=osiX_var)
osiX_entry.grid(column=2,row=14)
osiY = tk.Label(root, text="Ось Y интервал:", font=("Arial", 12))
osiY.grid(column=1, row=15)
osiY_var=tk.DoubleVar(value=5)
osiY_entry = ttk.Entry(root, textvariable=osiY_var)
osiY_entry.grid(column=2,row=15)

#Поле для вывода результатов
result_label = tk.Label(root, text="Результаты", font=("Arial", 16))
result_label.grid(column=1, row=16, columnspan=2)
points_text = tk.Text(root, height=10, width=40)
points_text.grid(column=1,row=17, columnspan=2)

#Кнопка выполнить
tru_button = tk.Button(root, text="Выполнить", command=button_click)
tru_button.grid(column=1, row=18, columnspan=1)

#Кнопка стоп
tru_close = tk.Button(root, text="Стоп", command=stop)
tru_close.grid(column=2, row=18, columnspan=1)

root.mainloop()