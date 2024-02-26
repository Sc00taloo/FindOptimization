from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import time

stop_flag = True

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
            function = easom_function
            gradient = gradient_easom
        case "Била":
            function = beale_function
            gradient = gradient_beale
        case "Сферы":
            function = sphere_function
            gradient = gradient_sphere
        case "Растригина":
            function = rastrigin_function
            gradient = gradient_rastrigin

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
    points_text.insert(tk.END, f"Итог ({startX:.4f}, {startY:.4f}) f= {fi:.4f}\n")
    points_text.see(tk.END)

#Рисует выбранный график
def draw(function_var):
    minnX = minX_var.get()
    maxxX = maxX_var.get()
    minnY = minY_var.get()
    maxxY = maxY_var.get()
    osiX = osiX_var.get()
    osiY = osiY_var.get()

    match function_var:
        case "Изома":
            function = easom_function
        case "Била":
            function = beale_function
        case "Сферы":
            function = sphere_function
        case "Растригина":
            function = rastrigin_function

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
for i in range(8):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=f"Лаба {i+1}")
notebook.grid(row=0, column=0, sticky="nsew")
style = ttk.Style()
style.configure("TNotebook.Tab", font=("Arial", 12))

# Начальное меню
start_label = tk.Label(root, text="Начальная настройка", font=("Arial", 16))
start_label.grid(column=1, row=0, columnspan=2)

start_labelX = tk.Label(root, text="Начальное X:", font=("Arial", 12))
start_labelX.grid(column=1, row=1)
X_var=tk.DoubleVar(value=1)
X_entry = ttk.Entry(root, textvariable=X_var)
X_entry.grid(column=2,row=1)

start_labelY = tk.Label(root, text="Начальное Y:", font=("Arial", 12))
start_labelY.grid(column=1, row=2)
Y_var=tk.DoubleVar(value=1)
Y_entry = ttk.Entry(root, textvariable=Y_var)
Y_entry.grid(column=2,row=2)

step = tk.Label(root, text="Шаг:", font=("Arial", 12))
step.grid(column=1, row=3)
step_var=tk.DoubleVar(value=0.01)
step_entry = ttk.Entry(root, textvariable=step_var)
step_entry.grid(column=2,row=3)

points_label = tk.Label(root, text="Количество итераций:", font=("Arial", 12))
points_label.grid(column=1,row=4)
points_var = tk.IntVar(value=100)
points_entry = ttk.Entry(root, textvariable=points_var)
points_entry.grid(column=2,row=4)

delay_label = tk.Label(root, text="Задержка:", font=("Arial", 12))
delay_label.grid(column=1,row=5)
delay_var = tk.DoubleVar(value=0.05)
delay_entry = ttk.Entry(root, textvariable=delay_var)
delay_entry.grid(column=2,row=5)

# Функции и их отображения
end_label = tk.Label(root, text="Функции и их отображения", font=("Arial", 16))
end_label.grid(column=1, row=8, columnspan=2)

function_label = tk.Label(root, text="Функция:", font=("Arial", 12))
function_label.grid(column=1,row=9)
function_var = tk.StringVar(value="...")
function_dropdown = ttk.OptionMenu(root, function_var, "...", "Била", "Сферы", "Изома", "Растригина", command=draw)
function_dropdown.grid(column=2,row=9)

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
tru_button = tk.Button(root, text="Выполнить", command=search)
tru_button.grid(column=1, row=18, columnspan=1)

#Кнопка стоп
tru_close = tk.Button(root, text="Стоп", command=stop)
tru_close.grid(column=2, row=18, columnspan=1)

root.mainloop()