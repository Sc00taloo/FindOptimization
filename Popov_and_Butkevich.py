import time
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import lab1, lab2, lab3, lab4, lab5, lab6, lab7, lab8

stop_flag = True

def toggle_optionmenu(event):
    if notebook.index(notebook.select()) == 1:
        function_dropdown.set_menu("График для 2 лабы")
        function_dropdown.config(state=tk.DISABLED)
        draw("График для 2 лабы")
    elif notebook.index(notebook.select()) == 6:
        function_dropdown.set_menu("Обратная сфера")
        function_dropdown.config(state=tk.DISABLED)
        draw("Обратная сфера")
    else:
        function_dropdown.set_menu("...", "Била", "Сферы", "Обратная сфера", "Изома", "Растригина", "График для 2 лабы", "Розенброкк", "Химмельблау")
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
        case 4:
            search5()
        case 5:
            search6()
        case 6:
            search7()
        case 7:
            search8()

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
        case "Обратная сфера":
            function = lab7.inverse_spherical_function
            #gradient = lab1.gradient_sphere
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
        case "Обратная сфера":
            function = lab7.inverse_spherical_function
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
        case "Обратная сфера":
            function = lab7.inverse_spherical_function
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

def search5():
    global stop_flag
    stop_flag = True
    points_text.delete(1.0, tk.END)
    selected_function = function_var.get()
    tru_delay = delay_var5.get()
    num_iter = points_var5.get()
    invest = investigators_var5.get()
    bip = bee_in_persp_var5.get()
    bib = bee_in_best_var5.get()
    persp_uch = persp_uchastki_var5.get()
    uchastok = uchastki_var5.get()
    razmer = razmer_var5.get()

    minnX = minX_var.get()
    maxxX = maxX_var.get()
    minnY = minY_var.get()
    maxxY = maxY_var.get()
    osiX = osiX_var.get()
    osiY = osiY_var.get()

    match selected_function:
        case "Изома":
            function = lab1.easom_function
        case "Била":
            function = lab1.beale_function
        case "Сферы":
            function = lab1.sphere_function
        case "Обратная сфера":
            function = lab7.inverse_spherical_function
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

    bees_swarm = lab5.Bees(function, invest, uchastok, persp_uch, bib, bip, razmer)
    #Генерирует начальных разведчиков
    bees_swarm.generate_start_scouts(maxxX, maxxY)
    #Соритрует их
    bees_swarm.sorted_scouts()
    #Выводим их на экран
    for new_scouts in bees_swarm.new_scouts:
        ax.scatter(new_scouts[0], new_scouts[1], new_scouts[2], c="black", alpha=0.8, s=3)

    #Находим участки
    bees_swarm.best_uchastochek()
    bees_swarm.persp_uchastochek()

    #Проверяем на близость
    bees_swarm.proferka()
    #Определяем популярность пчёл
    bees_swarm.razmer_bees()

    canvas.draw()
    root.update()

    # Итерируем N раз (num_iter)
    for i in range(num_iter):
        if (stop_flag):
            #Выпускате пчёл на лучшие участки
            bees_swarm.best_in_uchastki()
            for b in bees_swarm.bees[:uchastok]:
                ax.scatter(b[0], b[1], b[2], c="red")
            #Выпускате пчёл на перспективные участки
            bees_swarm.persp_in_uchastki()

            #Отправялем разведчиков искать новые участки
            bees_swarm.go_bees_scouts(maxxX, maxxY)
            #Соритруем пчёл
            bees_swarm.sorted_bees_in_hive()
            #Выводим на экран всех пчёл
            for new_scouts in bees_swarm.bees:
                ax.scatter(new_scouts[0], new_scouts[1], new_scouts[2], c="black", alpha=0.8, s=3)
            #Выпускате пчёл на лучшие участки
            bees_swarm.best_uchastochek()
            bees_swarm.persp_uchastochek()
            #Выпускате пчёл на перспективные участки
            bees_swarm.proferka()
            #Получаем лучшую пчелу
            b = bees_swarm.get_best()
            points_text.insert(tk.END, f"Итерация {i+1}:({b[0]:.4f}, {b[1]:.4f}) f= {b[2]:.4f}\n")
            points_text.see(tk.END)
            canvas.draw()
            root.update()
            time.sleep(float(tru_delay))

            ax.cla()
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.plot_surface(X, Y, Z, cmap='twilight', alpha=0.8)
            canvas.draw()
        else:
            break

    for b in bees_swarm.bees[:uchastok]:
        ax.scatter(b[0], b[1], b[2], c="red")
    for new_scouts in bees_swarm.bees:
        ax.scatter(new_scouts[0], new_scouts[1], new_scouts[2], c="black", alpha=0.8, s=3)
    # Вывод окончательного результата
    b = bees_swarm.get_best()
    points_text.insert(tk.END, f"Итог ({b[0]:.4f}, {b[1]:.4f}) f= {b[2]:.4f}\n")
    points_text.see(tk.END)
    canvas.draw()
    root.update()

def search6():
    global stop_flag
    stop_flag = True
    points_text.delete(1.0, tk.END)
    selected_function = function_var.get()
    tru_delay = delay_var6.get()
    num_iter = points_var6.get()
    antibodie = antibodie_var6.get()
    notb = numb_of_the_best_var6.get()
    nra = numb_rand_anti_var6.get()
    clons = clons_var6.get()
    mutation = mutation_var6.get()

    minnX = minX_var.get()
    maxxX = maxX_var.get()
    minnY = minY_var.get()
    maxxY = maxY_var.get()
    osiX = osiX_var.get()
    osiY = osiY_var.get()

    match selected_function:
        case "Изома":
            function = lab1.easom_function
        case "Била":
            function = lab1.beale_function
        case "Сферы":
            function = lab1.sphere_function
        case "Обратная сфера":
            function = lab7.inverse_spherical_function
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

    immunity = lab6.Immunity(function, antibodie, notb, nra, clons, mutation)
    #Генерирует начальные антитела
    immunity.generate_start_antibodies(maxxX, maxxY)
    #Сортирует их
    immunity.sorted_antibodies()
    for ag in immunity.new_antibodies:
        ax.scatter(ag[0], ag[1], ag[2], c="black", s=1, marker="s")

    #Находит лучшую антитело
    immunity.get_best()
    b = immunity.best_best()
    ax.scatter(b[0], b[1], b[2], c="red")

    canvas.draw()
    root.update()

    ax.cla()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.plot_surface(X, Y, Z, cmap='twilight', alpha=0.8)
    canvas.draw()
    #Клонирует лучшие антитела
    immunity.create_clones()
    #Мутирует антитела
    immunity.mutation_clone(maxxX, maxxY)
    #Сортирует клонов
    immunity.sorted_clones()
    #Генерирует новую популяцию антител
    immunity.uniting_populations(maxxX, maxxY)
    #Сортирует антитела
    immunity.sorted_n_anti()
    #Выводит на экрна новые антитела
    for ag in immunity.next_antibodies:
        ax.scatter(ag[0], ag[1], ag[2], c="black", s=1, marker="s")

    canvas.draw()
    root.update()

    ax.cla()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.plot_surface(X, Y, Z, cmap='twilight', alpha=0.8)
    canvas.draw()

    for i in range(num_iter):
        if (stop_flag):
            immunity.get_best_next()
            immunity.create_clones()
            immunity.mutation_clone(maxxX, maxxY)
            immunity.sorted_clones()
            immunity.uniting_populations(maxxX, maxxY)
            immunity.sorted_n_anti()
            for ag in immunity.next_antibodies:
                ax.scatter(ag[0], ag[1], ag[2], c="black", s=1, marker="s")

            b = immunity.best_best()
            ax.scatter(b[0], b[1], b[2], c="red")
            points_text.insert(tk.END, f"Итерация {i+1}:({b[0]:.4f}, {b[1]:.4f}) f= {b[2]:.4f}\n")
            points_text.see(tk.END)
            canvas.draw()
            root.update()
            time.sleep(float(tru_delay))

            ax.cla()
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.plot_surface(X, Y, Z, cmap='twilight', alpha=0.8)
            canvas.draw()
        else:
            break

    immunity.get_best_next()
    immunity.create_clones()
    immunity.mutation_clone(maxxX, maxxY)
    immunity.sorted_clones()
    immunity.uniting_populations(maxxX, maxxY)
    immunity.sorted_n_anti()
    for ag in immunity.next_antibodies:
        ax.scatter(ag[0], ag[1], ag[2], c="black", s=1, marker="s")

    # Вывод окончательного результата
    b = immunity.best_best()
    ax.scatter(b[0], b[1], b[2], c="red")
    points_text.insert(tk.END, f"Итог ({b[0]:.4f}, {b[1]:.4f}) f= {b[2]:.4f}\n")
    points_text.see(tk.END)
    canvas.draw()
    root.update()

def search7():
    global stop_flag
    stop_flag = True
    points_text.delete(1.0, tk.END)
    selected_function = function_var.get()
    tru_delay = delay_var7.get()
    num_iter = points_var7.get()
    bacterii = bacterii_var7.get()
    chemotaxis = chemotaxis_steps_var7.get()
    elimination = elimination_step_var7.get()
    elimination_numb = elimination_numb_var7.get()

    minnX = minX_var.get()
    maxxX = maxX_var.get()
    minnY = minY_var.get()
    maxxY = maxY_var.get()
    osiX = osiX_var.get()
    osiY = osiY_var.get()

    match selected_function:
        case "Изома":
            function = lab1.easom_function
        case "Била":
            function = lab1.beale_function
        case "Сферы":
            function = lab1.sphere_function
        case "Обратная сфера":
            function = lab7.inverse_spherical_function
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

    bacterias = lab7.Bacteria(function, bacterii, chemotaxis, elimination, elimination_numb)
    bacterias.generate_start_bacteria(maxxX, maxxY)
    for i in range(num_iter):
        if (stop_flag):
            bacterias.chemotaxis(1 /(i+1))
            bacterias.reproduction(maxxX,maxxY)
            if ((i + 1) % elimination == 0):
                bacterias.elimnination(maxxX,maxxY)

            bacterias.sorted_health()
            for bac in bacterias.new_bacteria:
                ax.scatter(bac[0], bac[1], bac[2], c="black", s=1, marker="s")

            b = bacterias.get_best()
            ax.scatter(b[0], b[1], b[2], c="red")

            points_text.insert(tk.END, f"Итерация {i+1}:({b[0]:.4f}, {b[1]:.4f}) f= {b[2]:.4f}\n")
            points_text.see(tk.END)

            canvas.draw()
            root.update()
            time.sleep(float(tru_delay))

            ax.cla()
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.plot_surface(X, Y, Z, cmap='twilight', alpha=0.8)
            canvas.draw()
        else:
            break

    for bac in bacterias.new_bacteria:
        ax.scatter(bac[0], bac[1], bac[2], c="black", s=1, marker="s")

    b = bacterias.get_best()
    ax.scatter(b[0], b[1], b[2], c="red")

    points_text.insert(tk.END, f"Итог ({b[0]:.4f}, {b[1]:.4f}) f= {b[2]:.4f}\n")
    points_text.see(tk.END)

    canvas.draw()
    root.update()

def search8():
    global stop_flag
    stop_flag = True
    points_text.delete(1.0, tk.END)
    selected_function = function_var.get()
    tru_delay = delay_var8.get()
    num_iter = points_var8.get()
    bacterii = bacterii_var8.get()
    chemotaxis = chemotaxis_steps_var8.get()
    elimination = elimination_step_var8.get()
    elimination_numb = elimination_numb_var8.get()
    alpha = alpha_var8.get()
    beta = beta_var8.get()
    inertia = inertia_var8.get()

    minnX = minX_var.get()
    maxxX = maxX_var.get()
    minnY = minY_var.get()
    maxxY = maxY_var.get()
    osiX = osiX_var.get()
    osiY = osiY_var.get()

    match selected_function:
        case "Изома":
            function = lab1.easom_function
        case "Била":
            function = lab1.beale_function
        case "Сферы":
            function = lab1.sphere_function
        case "Обратная сфера":
            function = lab7.inverse_spherical_function
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

    hubrid = lab8.HybridAlgorithm(function, bacterii, alpha, beta, inertia, chemotaxis, elimination, elimination_numb)
    hubrid.generate_start(maxxX, maxxY)
    for j in range(bacterii):
        ax.scatter(hubrid.bacteria_data[j][0], hubrid.bacteria_data[j][1], hubrid.bacteria_data[j][2],
                   c='black', alpha=0.8)
    hubrid.sorted()
    best_particles = hubrid.get_best_position()
    ax.scatter(best_particles[0], best_particles[1], best_particles[2], c='red', alpha=0.8)

    canvas.draw()
    root.update()

    ax.cla()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.plot_surface(X, Y, Z, cmap='twilight', alpha=0.8)
    canvas.draw()

    for i in range(num_iter):
        if stop_flag:
            hubrid.chemotaxis(1 / (i + 1))
            hubrid.update_particles()
            #hubrid.reproduction(maxxX, maxxY)
            if ((i + 1) % elimination == 0):
                 hubrid.elimination(maxxX,maxxY)
            for bac in hubrid.particles_data:
                ax.scatter(bac[0], bac[1], bac[2], c="black", s=1, marker="s")

            hubrid.sorted()
            b = hubrid.get_best()
            ax.scatter(b[0], b[1], b[2], c="red")

            points_text.insert(tk.END, f"Итерация {i + 1}:({b[0]:.4f}, {b[1]:.4f}) f= {b[2]:.4f}\n")
            points_text.see(tk.END)

            canvas.draw()
            root.update()
            time.sleep(float(tru_delay))

            ax.cla()
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.plot_surface(X, Y, Z, cmap='twilight', alpha=0.8)
            canvas.draw()
        else:
            break

    hubrid.sorted()
    for bac in hubrid.particles_data:
        ax.scatter(bac[0], bac[1], bac[2], c="black", s=1, marker="s")
    b = hubrid.get_best()
    ax.scatter(b[0], b[1], b[2], c="red")

    points_text.insert(tk.END, f"Итог ({b[0]:.4f}, {b[1]:.4f}) f= {b[2]:.4f}\n")
    points_text.see(tk.END)

    canvas.draw()
    root.update()

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
       case "Обратная сфера":
            function = lab7.inverse_spherical_function
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
notebook.grid(row=0, column=1, columnspan=2)
style = ttk.Style()
style.configure("TNotebook.Tab", font=("Arial", 12))
frame1 = ttk.Frame(notebook)
notebook.add(frame1, text=f"1")
frame2 = ttk.Frame(notebook)
notebook.add(frame2, text=f"2")
frame3 = ttk.Frame(notebook)
notebook.add(frame3, text=f"3")
frame4 = ttk.Frame(notebook)
notebook.add(frame4, text=f"4")
frame5 = ttk.Frame(notebook)
notebook.add(frame5, text=f"5")
frame6 = ttk.Frame(notebook)
notebook.add(frame6, text=f"6")
frame7 = ttk.Frame(notebook)
notebook.add(frame7, text=f"7")
frame8 = ttk.Frame(notebook)
notebook.add(frame8, text=f"8")

##################### 1 laba #####################

start_label = tk.Label(frame1, text="Начальная настройка", font=("Arial", 16))
start_label.grid(column=1, row=0, columnspan=2)

start_labelX = tk.Label(frame1, text="Начальное X:", font=("Arial", 12))
start_labelX.grid(column=1, row=1, columnspan=1)
X_var = tk.DoubleVar(value=1)
X_entry = ttk.Entry(frame1, textvariable=X_var)
X_entry.grid(column=2, row=1, columnspan=1)

start_labelY = tk.Label(frame1, text="Начальное Y:", font=("Arial", 12))
start_labelY.grid(column=1, row=2, columnspan=1)
Y_var = tk.DoubleVar(value=1)
Y_entry = ttk.Entry(frame1, textvariable=Y_var)
Y_entry.grid(column=2, row=2, columnspan=1)

step = tk.Label(frame1, text="Шаг:", font=("Arial", 12))
step.grid(column=1, row=3, columnspan=1)
step_var = tk.DoubleVar(value=0.01)
step_entry = ttk.Entry(frame1, textvariable=step_var)
step_entry.grid(column=2, row=3, columnspan=1)

points_label = tk.Label(frame1, text="Кол-во итераций:", font=("Arial", 12))
points_label.grid(column=1, row=4, columnspan=1)
points_var = tk.IntVar(value=100)
points_entry = ttk.Entry(frame1, textvariable=points_var)
points_entry.grid(column=2, row=4, columnspan=1)

delay_label = tk.Label(frame1, text="Задержка:", font=("Arial", 12))
delay_label.grid(column=1, row=5, columnspan=1)
delay_var = tk.DoubleVar(value=0.05)
delay_entry = ttk.Entry(frame1, textvariable=delay_var)
delay_entry.grid(column=2, row=5, columnspan=1)

##################### 2 laba #####################

start_label = tk.Label(frame2, text="Начальная настройка", font=("Arial", 16))
start_label.grid(column=1, row=0, columnspan=2)

delay_label = tk.Label(frame2, text="Задержка:", font=("Arial", 12))
delay_label.grid(column=1, row=1, columnspan=1)
delay_var2 = tk.DoubleVar(value=0.5)
delay_entry = ttk.Entry(frame2, textvariable=delay_var2)
delay_entry.grid(column=2, row=1, columnspan=1)

#####################  3 laba  #####################

start_label = tk.Label(frame3, text="Начальная настройка", font=("Arial", 16))
start_label.grid(column=1, row=0, columnspan=2)

points_label = tk.Label(frame3, text="Количество итераций:", font=("Arial", 12))
points_label.grid(column=1, row=1, columnspan=1)
points_var3 = tk.IntVar(value=100)
points_entry = ttk.Entry(frame3, textvariable=points_var3)
points_entry.grid(column=2, row=1, columnspan=1)

individuals_label = tk.Label(frame3, text="Количество особей:", font=("Arial", 12))
individuals_label.grid(column=1, row=2, columnspan=1)
individuals_var3 = tk.IntVar(value=20)
individuals_entry = ttk.Entry(frame3, textvariable=individuals_var3)
individuals_entry.grid(column=2, row=2, columnspan=1)

delay_label = tk.Label(frame3, text="Задержка:", font=("Arial", 12))
delay_label.grid(column=1, row=3, columnspan=1)
delay_var3 = tk.DoubleVar(value=0.01)
delay_entry = ttk.Entry(frame3, textvariable=delay_var3)
delay_entry.grid(column=2, row=3, columnspan=1)

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
alpha_var4 = tk.DoubleVar(value=1.1)
alpha_entry = ttk.Entry(frame4, textvariable=alpha_var4)
alpha_entry.grid(column=2, row=3)

beta_label = tk.Label(frame4, text="Бета:", font=("Arial", 12))
beta_label.grid(column=1, row=4)
beta_var4 = tk.DoubleVar(value=1.1)
beta_entry = ttk.Entry(frame4, textvariable=beta_var4)
beta_entry.grid(column=2, row=4)

inertia_label = tk.Label(frame4, text="Инерция:", font=("Arial", 12))
inertia_label.grid(column=1, row=5)
inertia_var4 = tk.DoubleVar(value=0.73)
inertia_entry = ttk.Entry(frame4, textvariable=inertia_var4)
inertia_entry.grid(column=2, row=5)

delay_label = tk.Label(frame4, text="Задержка:", font=("Arial", 12))
delay_label.grid(column=1, row=6)
delay_var4 = tk.DoubleVar(value=0.01)
delay_entry = ttk.Entry(frame4, textvariable=delay_var4)
delay_entry.grid(column=2, row=6)

#####################  5 laba  #####################

start_label = tk.Label(frame5, text="Начальная настройка", font=("Arial", 16))
start_label.grid(column=1, row=0, columnspan=2)

points_label = tk.Label(frame5, text="Количество итераций:", font=("Arial", 12))
points_label.grid(column=1, row=1)
points_var5 = tk.IntVar(value=200)
points_entry = ttk.Entry(frame5, textvariable=points_var5)
points_entry.grid(column=2, row=1)

investigators_label = tk.Label(frame5, text="Разведчики:", font=("Arial", 12))
investigators_label.grid(column=1, row=2)
investigators_var5 = tk.IntVar(value=20)
investigators_entry = ttk.Entry(frame5, textvariable=investigators_var5)
investigators_entry.grid(column=2, row=2)

bee_in_persp_label = tk.Label(frame5, text="Пчёл в перспективном уч:", font=("Arial", 12))
bee_in_persp_label.grid(column=1, row=3)
bee_in_persp_var5 = tk.IntVar(value=10)
bee_in_persp_entry = ttk.Entry(frame5, textvariable=bee_in_persp_var5)
bee_in_persp_entry.grid(column=2, row=3)

bee_in_best_label = tk.Label(frame5, text="Пчёл в лучшем участке:", font=("Arial", 12))
bee_in_best_label.grid(column=1, row=4)
bee_in_best_var5 = tk.IntVar(value=20)
bee_in_best_entry = ttk.Entry(frame5, textvariable=bee_in_best_var5)
bee_in_best_entry.grid(column=2, row=4)

persp_uchastki_label = tk.Label(frame5, text="Перспективных участков:", font=("Arial", 12))
persp_uchastki_label.grid(column=1, row=5)
persp_uchastki_var5 = tk.IntVar(value=3)
persp_uchastki_entry = ttk.Entry(frame5, textvariable=persp_uchastki_var5)
persp_uchastki_entry.grid(column=2, row=5)

uchastki_label = tk.Label(frame5, text="Лучших участков:", font=("Arial", 12))
uchastki_label.grid(column=1, row=6)
uchastki_var5 = tk.IntVar(value=1)
uchastki_entry = ttk.Entry(frame5, textvariable=uchastki_var5)
uchastki_entry.grid(column=2, row=6)

razmer_label = tk.Label(frame5, text="Размер участков:", font=("Arial", 12))
razmer_label.grid(column=1, row=7)
razmer_var5 = tk.DoubleVar(value=0.5)
razmer_entry = ttk.Entry(frame5, textvariable=razmer_var5)
razmer_entry.grid(column=2, row=7)

delay_label = tk.Label(frame5, text="Задержка:", font=("Arial", 12))
delay_label.grid(column=1, row=8)
delay_var5 = tk.DoubleVar(value=0.01)
delay_entry = ttk.Entry(frame5, textvariable=delay_var5)
delay_entry.grid(column=2, row=8)

#####################  6 laba  #####################

start_label = tk.Label(frame6, text="Начальная настройка", font=("Arial", 16))
start_label.grid(column=1, row=0, columnspan=2)

points_label = tk.Label(frame6, text="Количество итераций:", font=("Arial", 12))
points_label.grid(column=1, row=1)
points_var6 = tk.IntVar(value=200)
points_entry = ttk.Entry(frame6, textvariable=points_var6)
points_entry.grid(column=2, row=1)

antibodie_label = tk.Label(frame6, text="Антител:", font=("Arial", 12))
antibodie_label.grid(column=1, row=2)
antibodie_var6 = tk.IntVar(value=50)
antibodie_entry = ttk.Entry(frame6, textvariable=antibodie_var6)
antibodie_entry.grid(column=2, row=2)

numb_of_the_best_label = tk.Label(frame6, text="Кол-во лучших отбираемых:", font=("Arial", 12))
numb_of_the_best_label.grid(column=1, row=3)
numb_of_the_best_var6 = tk.IntVar(value=10)
numb_of_the_best_entry = ttk.Entry(frame6, textvariable=numb_of_the_best_var6)
numb_of_the_best_entry.grid(column=2, row=3)

numb_rand_anti_label = tk.Label(frame6, text="Число случайных антител:", font=("Arial", 12))
numb_rand_anti_label.grid(column=1, row=4)
numb_rand_anti_var6 = tk.IntVar(value=10)
numb_rand_anti_entry = ttk.Entry(frame6, textvariable=numb_rand_anti_var6)
numb_rand_anti_entry.grid(column=2, row=4)

clons_label = tk.Label(frame6, text="Кол-во клонов:", font=("Arial", 12))
clons_label.grid(column=1, row=5)
clons_var6 = tk.IntVar(value=20)
clons_entry = ttk.Entry(frame6, textvariable=clons_var6)
clons_entry.grid(column=2, row=5)

mutation_label = tk.Label(frame6, text="Коэффициент мутации:", font=("Arial", 12))
mutation_label.grid(column=1, row=6)
mutation_var6 = tk.DoubleVar(value=1.2)
mutation_entry = ttk.Entry(frame6, textvariable=mutation_var6)
mutation_entry.grid(column=2, row=6)

delay_label = tk.Label(frame6, text="Задержка:", font=("Arial", 12))
delay_label.grid(column=1, row=8)
delay_var6 = tk.DoubleVar(value=0.01)
delay_entry = ttk.Entry(frame6, textvariable=delay_var6)
delay_entry.grid(column=2, row=8)

#####################  7 laba  #####################

start_label = tk.Label(frame7, text="Начальная настройка", font=("Arial", 16))
start_label.grid(column=1, row=0, columnspan=2)

points_label = tk.Label(frame7, text="Количество итераций:", font=("Arial", 12))
points_label.grid(column=1, row=1)
points_var7 = tk.IntVar(value=150)
points_entry = ttk.Entry(frame7, textvariable=points_var7)
points_entry.grid(column=2, row=1)

bacterii_label = tk.Label(frame7, text="Бактерий:", font=("Arial", 12))
bacterii_label.grid(column=1, row=2)
bacterii_var7 = tk.IntVar(value=40)
bacterii_entry = ttk.Entry(frame7, textvariable=bacterii_var7)
bacterii_entry.grid(column=2, row=2)

chemotaxis_steps_label = tk.Label(frame7, text="Шагов хемотаксиса:", font=("Arial", 12))
chemotaxis_steps_label.grid(column=1, row=3)
chemotaxis_steps_var7 = tk.IntVar(value=6)
chemotaxis_steps_entry = ttk.Entry(frame7, textvariable=chemotaxis_steps_var7)
chemotaxis_steps_entry.grid(column=2, row=3)

elimination_step_label = tk.Label(frame7, text="Шаг ликвидации:", font=("Arial", 12))
elimination_step_label.grid(column=1, row=4)
elimination_step_var7 = tk.IntVar(value=15)
elimination_step_entry = ttk.Entry(frame7, textvariable=elimination_step_var7)
elimination_step_entry.grid(column=2, row=4)

elimination_numb_label = tk.Label(frame7, text="Число ликвидируемых:", font=("Arial", 12))
elimination_numb_label.grid(column=1, row=5)
elimination_numb_var7 = tk.IntVar(value=25)
elimination_numb_entry = ttk.Entry(frame7, textvariable=elimination_numb_var7)
elimination_numb_entry.grid(column=2, row=5)

delay_label = tk.Label(frame7, text="Задержка:", font=("Arial", 12))
delay_label.grid(column=1, row=6)
delay_var7 = tk.DoubleVar(value=0.01)
delay_entry = ttk.Entry(frame7, textvariable=delay_var7)
delay_entry.grid(column=2, row=6)

#####################  8 laba  #####################

start_label = tk.Label(frame8, text="Начальная настройка", font=("Arial", 16))
start_label.grid(column=1, row=0, columnspan=2)

points_label = tk.Label(frame8, text="Количество итераций:", font=("Arial", 12))
points_label.grid(column=1, row=1)
points_var8 = tk.IntVar(value=50)
points_entry = ttk.Entry(frame8, textvariable=points_var8)
points_entry.grid(column=2, row=1)

bacterii_label = tk.Label(frame8, text="Частиц/Бактерий:", font=("Arial", 12))
bacterii_label.grid(column=1, row=2)
bacterii_var8 = tk.IntVar(value=20)
bacterii_entry = ttk.Entry(frame8, textvariable=bacterii_var8)
bacterii_entry.grid(column=2, row=2)

alpha_label = tk.Label(frame8, text="Альфа:", font=("Arial", 12))
alpha_label.grid(column=1, row=3)
alpha_var8 = tk.DoubleVar(value=1.1)
alpha_entry = ttk.Entry(frame8, textvariable=alpha_var8)
alpha_entry.grid(column=2, row=3)

beta_label = tk.Label(frame8, text="Бета:", font=("Arial", 12))
beta_label.grid(column=1, row=4)
beta_var8 = tk.DoubleVar(value=1.1)
beta_entry = ttk.Entry(frame8, textvariable=beta_var8)
beta_entry.grid(column=2, row=4)

inertia_label = tk.Label(frame8, text="Инерция:", font=("Arial", 12))
inertia_label.grid(column=1, row=5)
inertia_var8 = tk.DoubleVar(value=0.73)
inertia_entry = ttk.Entry(frame8, textvariable=inertia_var8)
inertia_entry.grid(column=2, row=5)

chemotaxis_steps_label = tk.Label(frame8, text="Шагов хемотаксиса:", font=("Arial", 12))
chemotaxis_steps_label.grid(column=1, row=6)
chemotaxis_steps_var8 = tk.IntVar(value=6)
chemotaxis_steps_entry = ttk.Entry(frame8, textvariable=chemotaxis_steps_var8)
chemotaxis_steps_entry.grid(column=2, row=6)

elimination_step_label = tk.Label(frame8, text="Шаг ликвидации:", font=("Arial", 12))
elimination_step_label.grid(column=1, row=7)
elimination_step_var8 = tk.IntVar(value=15)
elimination_step_entry = ttk.Entry(frame8, textvariable=elimination_step_var8)
elimination_step_entry.grid(column=2, row=7)

elimination_numb_label = tk.Label(frame8, text="Число ликвидируемых:", font=("Arial", 12))
elimination_numb_label.grid(column=1, row=8)
elimination_numb_var8 = tk.IntVar(value=5)
elimination_numb_entry = ttk.Entry(frame8, textvariable=elimination_numb_var8)
elimination_numb_entry.grid(column=2, row=8)

delay_label = tk.Label(frame8, text="Задержка:", font=("Arial", 12))
delay_label.grid(column=1, row=9)
delay_var8 = tk.DoubleVar(value=0.01)
delay_entry = ttk.Entry(frame8, textvariable=delay_var8)
delay_entry.grid(column=2, row=9)

#####################    #####################

# Функции и их отображения
end_label = tk.Label(root, text="Функции и их отображения", font=("Arial", 16))
end_label.grid(column=1, row=8, columnspan=2)

function_label = tk.Label(root, text="Функция:", font=("Arial", 12))
function_label.grid(column=1,row=9)
function_var = tk.StringVar(value="...")
function_dropdown = ttk.OptionMenu(root, function_var, "...", "Била", "Сферы", "Обратная сфера" , "Изома", "Растригина", "График для 2 лабы", "Розенброкк", "Химмельблау", command=draw)
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