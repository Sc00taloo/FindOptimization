import random
from random import uniform
from operator import itemgetter

# scouts = 5
# new_scouts = dict()
# def func(x,y):
#     return x+y - 2
#
# for i in range(scouts):
#     po_x = uniform(-3, 3)
#     po_y = uniform(-3, 3)
#     new_scouts[i] = [po_x, po_y, func(po_x, po_y)]
# # scouts = [[random.uniform(-3, 3), random.uniform(-3, 3), float(0.0)] for _ in
# #                range(scouts)]
#
#
# print(new_scouts)
# max_b = max(new_scouts.items(), key=lambda item: item[1][2])
# print(max_b)
#
# first_key = next(iter(new_scouts))
# first_value = new_scouts[first_key]
#
# #print(first_value)
#
# new = {1:[1,1,2],2:[4,3,2],3:[6,4,1]}
# old = {1:[1,2,3],2:[4,3,2],3:[6,4,1]}
#
# bees = {**new, **old}
# print(bees)
# print(bees[1][2])
#
# #my_dict = {1: [1,2,3], 2: [3,4,5], 3: [5,6,7], 4: [7,8,9], 5: [9,10,11]}
#
# # Параметры e и p
# e = 2
# p = 1
#
# # Создание подмножества словаря
# #selected_dict = {k: my_dict[k] for k in list(my_dict.keys())[:e + p]}
# #print(selected_dict)
#
#
#
# def get_best(best_bees, bees):
#     if (best_bees):
#         for b in best_bees:
#             for n in bees:
#                 if (b[2] < n[2]):
#                     return best_bees[0]
#                 else:
#                     return bees[0]
#     else:
#         best_bees = bees[:2]
#         return bees[0]
#
# a = [[1,2,3],[3,4,5],[5,6,7],[5,6,8]]
# b = [[3,4,1],[4,1,2]]
# b = get_best(b, a)
# print(a,b)


my_list = [[1, 2, 3], [5, 6, 7], [9, 10, 11]]
multa = my_list[1][0]
print(multa)

# Получить первые и вторые числа из каждого кортежа
first_numbers = [item[0] for item in my_list]
second_numbers = [item[1] for item in my_list]

print("Первые числа:", first_numbers)
print("Вторые числа:", second_numbers)

# Обратиться к первому кортежу и взять первые два числа
first_tuple = my_list[0]
first_two_numbers = first_tuple[:2]  # первые два элемента

print("Первый кортеж:", first_tuple)
print("Первые два числа из первого кортежа:", first_two_numbers)