from tkinter import *
from tkinter import messagebox
from itertools import groupby
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

ar = [[0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 3],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
      [0, 0, 0, 0, 4, 0, 5, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
      [2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
      [3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


def set_dim_click():
    global empty_cell_list, fill_cell_list, dim, height, ar
    try:
        empty_cell_list = []
        fill_cell_list = []
        temp = []
        dim = int(dim_box.get())
        if dim == 0 or dim < 0:
            messagebox.showinfo(message='Неверный формат ввода размерности!')
            window.focus()
            dim_box.focus_set()
            return
        if dim > 25:
            messagebox.showinfo(message='Размерность не может быть больше 25!')
            window.focus()
            dim_box.focus_set()
            return
        slaves = window.place_slaves()
        if slaves:
            for el in slaves:
                el.destroy()
        Label(window, text='Матрица смежности исходного графа').place(x=40, y=50)
        for i in range(dim):
            Label(window, text=i + 1).place(x=40 + i * 30, y=80)
            Label(window, text=i + 1).place(x=8, y=110 + i * 30)
        for i in range(dim):
            for j in range(dim):
                if dim == 17:
                    v1 = StringVar()
                    v1.set(ar[i][j])
                    temp.append(Entry(window, width=3, textvariable=v1))
                else:
                    v1 = StringVar()
                    temp.append(Entry(window, width=3, textvariable=v1))
            empty_cell_list.append(temp)
            temp = []
        for i in range(dim):
            for j in range(dim):
                empty_cell_list[i][j].place(x=33 + j * 30, y=113 + i * 30)
        apply_btn = Button(window, text='Применить', command=apply_click)
        apply_btn.place(x=(33 + dim * 30) / 2 - 30, y=120 + dim * 30)
    except ValueError:
        messagebox.showinfo(message='Размерность может быть только числом!')
        window.focus()
        dim_box.focus_set()


def apply_click():
    global empty_cell_list, fill_cell_list, dim, result, fill_cell_list_0, renum_list
    try:
        temp = []
        for i in range(dim):
            for j in range(dim):
                temp.append(int(empty_cell_list[i][j].get()))
                if int(empty_cell_list[i][j].get()) < 0:
                    messagebox.showinfo(message='Значения матрицы не могут быть отрицательными!')
                    empty_cell_list[i][j].focus_set()
                    return
                if i == j and int(empty_cell_list[i][j].get()) != 0:
                    messagebox.showinfo(message='На диагонали должны быть нули!')
                    empty_cell_list[i][j].focus_set()
                    return
            fill_cell_list.append(temp)
            temp = []
        levels(fill_cell_list)
        Label(window, text='Уровни графа').place(x=70 + dim * 30, y=80)
        for i in range(len(result)):
            Label(window, text=f'N{i}=').place(x=70 + dim * 30, y=110 + i * 30)
            temp1 = []
            for j in range(len(result[i])):
                temp1.append(result[i][j])
            Label(window, text='{ ' + f'{i + 1} ' + f'{temp1}' + ' }').place(x=105 + dim * 30, y=110 + i * 30)
        stok = []
        istok = []
        fill_cell_list_0 = fill_cell_list.copy()
        for i in range(dim):
            for j in range(dim):
                if fill_cell_list_0[i][j] == math.inf:
                    fill_cell_list_0[i][j] = 0
        for i in range(dim):
            if sum(fill_cell_list_0[i]) == 0:
                stok.append(i + 1)
        for i in range(dim):
            summa = 0
            for j in range(dim):
                summa += fill_cell_list_0[j][i]
            if summa == 0:
                istok.append(i + 1)
        Label(window, text='Стоки:').place(x=70 + dim * 30, y=105 + len(result) * 30)
        for i in range(len(stok)):
            Label(window, text=stok[i]).place(x=70 + dim * 30, y=130 + len(result) * 30 + i * 20)
        height_1 = 130 + len(result) * 30 + len(stok) * 20
        Label(window, text='Истоки:').place(x=70 + dim * 30, y=height_1 + 20)
        for i in range(len(istok)):
            Label(window, text=istok[i]).place(x=70 + dim * 30, y=height_1 + 40 + i * 20)
        height_2 = height_1 + 50 + len(istok) * 20
        Button(window, text='Показать упорядочивание вершин', command=renum).place(x=60 + dim * 30, y=height_2)
        Button(window, text='Построить матрицу смежности       \n упорядоченного графа',
               command=new_matrix).place(x=60 + dim * 30, y=height_2 + 40)
        Button(window, text='        Показать исходный граф          ', command=source_graph).place(x=60 + dim * 30,
                                                                                                    y=height_2 + 100)
        counter = 0
        renum_list = []
        for i in range(len(result)):
            for j in range(len(result[i])):
                counter += 1
                renum_list.append([counter, result[i][j]])
    except ValueError:
        messagebox.showinfo(message='Элементы матрицы могут быть только числами!')
        window.focus()


def renum():
    global result, renum_list
    window_2 = Tk()
    window_2.geometry('300x800')
    window_2.title('Упорядочивание вершин')
    counter = 0
    renum_list = []
    for i in range(len(result)):
        for j in range(len(result[i])):
            counter += 1
            renum_list.append([counter, result[i][j]])

    Label(window_2, text='Упорядочивание вершин').place(x=10, y=10)
    for i in range(len(renum_list)):
        for j in range(0, len(renum_list[i]), 2):
            Label(window_2, text=f'{renum_list[i][j]} --> {renum_list[i][j + 1]}').place(x=10, y=30 + i * 20)


def levels(fill_cell_list):
    global result
    for i in range(len(fill_cell_list)):
        for j in range(len(fill_cell_list)):
            if fill_cell_list[i][j] == 0:
                fill_cell_list[i][j] = math.inf

    digs = []
    temp = []
    for i in range(len(fill_cell_list)):
        for j in range(len(fill_cell_list)):
            if fill_cell_list[j][i] != math.inf:
                temp.append(j + 1)

        digs.append(temp)
        temp = []

    lvl = []
    for i in range(len(digs)):
        for j in range(len(digs)):
            if len(digs[i]) == j:
                lvl.append(digs)
    del lvl[1:]
    lvl = lvl[0]
    ind = []
    temp_ind = []
    lvl_check = lvl.copy()
    min_len = min(lvl_check, key=len)
    for i in range(len(lvl_check)):
        if lvl_check[i] == min_len:
            ind.append(i + 1)

    temp_ind.append(ind)
    for j in range(1, len(lvl)):
        flat_list = [item for sublist in temp_ind for item in sublist]
        ind = [i + 1 for i, q in enumerate(lvl) if q and not set(q) - set(flat_list)]
        for k in range(len(ind)):
            if ind[k] in flat_list:
                ind[k] -= 999
        temp_ind.append(ind)
    final_ind = [[] * i for i in range(len(temp_ind))]
    for i in range(len(temp_ind)):
        for j in range(len(temp_ind[i])):
            if temp_ind[i][j] > 0:
                final_ind[i].append(temp_ind[i][j])
    result = []
    for i in final_ind:
        if i:
            result.append(i)


def new_matrix():
    global fill_cell_list_0, dim, renum_list, new_matr, size
    temp_i, temp_j = 0, 0
    new_matr = []
    size = 380 + dim * 30
    Label(window, text='Матрица смежности упорядоченного графа').place(x=size, y=50)
    Button(window, text='Найти путь и его минимальную\n длину', command=min_path).place(
         x=size, y=120 + dim * 30)
    Button(window, text='Показать упорядоченный граф', command=trans_graph).place(x=size+260, y=120+dim*30)
    for i in range(dim):
        Label(window, text=i + 1).place(x=size + i * 30, y=80)
        Label(window, text=i + 1).place(x=size - 25, y=111 + i * 30)
    istok.place(x=size, y=180+dim*30)
    Label(window, text='Из:').place(x=size-30, y=180+dim*30)
    stok.place(x=size+75, y=180+dim*30)
    Label(window, text='В:').place(x=size+50, y=180+dim*30)
    for i in range(dim):
        temp = []
        for j in range(dim):
            for k in range(len(renum_list)):
                if i + 1 == renum_list[k][0]:
                    temp_i = renum_list[k][1]
                if j + 1 == renum_list[k][0]:
                    temp_j = renum_list[k][1]
            v2 = StringVar()
            if fill_cell_list_0[temp_i - 1][temp_j - 1] == 0:
                v2.set('')
            else:
                v2.set(fill_cell_list_0[temp_i - 1][temp_j - 1])
            temp.append(Entry(window, width=3, textvariable=v2))
        new_matr.append(temp)
    for i in range(dim):
        for j in range(dim):
            new_matr[i][j].place(x=size + j * 30, y=113 + i * 30)


def min_path():
    global new_matr, dim, size, istok, stok, m
    temp = []
    m = []
    for i in range(dim):
        for j in range(dim):
            temp.append(new_matr[i][j].get())
        m.append(temp)
        temp = []
    for i in range(dim):
        for j in range(dim):
            if m[i][j] == '':
                m[i][j] = '0'
            m[i][j] = int(m[i][j])
    G = nx.from_numpy_matrix(np.matrix(m), create_using=nx.DiGraph)
    summa = 0
    try:
        path = nx.dijkstra_path(G, int(istok.get())-1, int(stok.get())-1)
        if path != None:
            for i in range(len(path) - 1):
                summa += G[path[i]][path[i + 1]]['weight']
        Label(window, text='                                                                                        ').place(
            x=size + 40 + i * 40, y=240 + dim * 30)
        Label(window,
              text='                                                                                                ').place(
            x=size, y=270 + dim * 30)
        path = [i+1 for i in path]
        Label(window, text='Путь: ').place(x=size, y=240 + dim * 30)
        Label(window, text='Длина пути: ').place(x=size, y=270 + dim * 30)
        Label(window, text=summa).place(x=size + 90, y=270 + dim * 30)
        Label(window, text=path).place(x=size+90, y=240 + dim * 30)
    except:
        messagebox.showinfo(message='Нет пути или неправильно указаны вершины')
        window.focus()
        istok.focus_set()
        return

def source_graph():
    global dim, COLORS, fill_cell_list_0
    G = nx.from_numpy_matrix(np.matrix(fill_cell_list_0), create_using=nx.DiGraph)
    layout = nx.spring_layout(G)
    nx.draw(G, layout, with_labels=True)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)
    plt.show()
    # window_3 = Tk()
    # window_3.title('Исходный граф')
    # g = Canvas(window_3, width=1900, height=900)
    # g.pack()
    # print(fill_cell_list_0[0][0])
    # start_x, start_y = 10, 140
    # kord = []
    # for i in range(dim):
    #     g.create_oval((start_x, start_y), (start_x + 90, start_y + 90), width=3, outline=random.choice(COLORS))
    #     g.create_text(start_x + 45, start_y + 45, text=f'{i + 1}')
    #     kord.append([start_x + 90, start_y + 45])
    #     start_y += 200
    #     r = 5
    #     r1 = 670
    #     if (i + 1) % 3 == 0:
    #         start_x += 250
    #         start_y = 140
    # for i in range(dim):
    #     for j in range(dim):
    #         color = random.choice(COLORS)
    #         if fill_cell_list_0[i][j] != 0:
    #             ur_i = math.ceil((i + 1) / 3)
    #             ur_j = math.ceil((j + 1) / 3)
    #             if ur_i == ur_j and (i == j + 2 or i == j - 2):
    #                 g.create_line((kord[i][0] - 5, kord[i][1] + 10), (kord[i][0] + 20, kord[i][1] + 10),
    #                               (kord[j][0] + 20, kord[j][1]), (kord[j][0], kord[j][1]), width=5, arrow=LAST,
    #                               arrowshape="10 20 10")
    #                 g.create_text((kord[i][0] + 20 + kord[j][0] + 20) / 2 + 9, (kord[i][1] + 10 + kord[j][1]) / 2,
    #                               text=fill_cell_list_0[i][j],
    #                               font="Verdana 14")
    #             elif ur_i == ur_j and i == j + 1:
    #                 g.create_line((kord[i][0] - 45, kord[i][1] - 45), (kord[j][0] - 45, kord[j][1] + 45), arrow=LAST,
    #                               width=5,
    #                               arrowshape="10 20 10")
    #                 g.create_text((kord[i][0] - 45 + kord[j][0] - 45) / 2 + 9, (kord[i][1] - 45 + kord[j][1] + 45) / 2,
    #                               text=fill_cell_list_0[i][j],
    #                               font="Verdana 14")
    #
    #             elif ur_i == ur_j and i == j - 1:
    #                 g.create_line((kord[i][0] - 45, kord[i][1] + 45), (kord[j][0] - 45, kord[j][1] - 45), arrow=LAST,
    #                               width=5,
    #                               arrowshape="10 20 10")
    #                 g.create_text((kord[i][0] - 45 + kord[j][0] - 45) / 2 + 9, (kord[i][1] + 45 + kord[j][1] - 45) / 2,
    #                               text=fill_cell_list_0[i][j],
    #                               font='Verdana 14')
    #             elif ur_i == ur_j + 1:
    #                 g.create_line((kord[i][0] - 90, kord[i][1]), (kord[j][0], kord[j][1]), arrow=LAST, width=5,
    #                               arrowshape="10 20 10")
    #                 g.create_text((kord[i][0] - 90 + kord[j][0]) / 2, (kord[i][1] + kord[j][1]) / 2 - 16,
    #                               text=fill_cell_list_0[i][j],
    #                               font='Verdana 14')
    #             elif ur_i == ur_j - 1:
    #                 g.create_line((kord[i][0], kord[i][1]), (kord[j][0] - 90, kord[j][1]), arrow=LAST, width=5,
    #                               arrowshape="10 20 10")
    #                 g.create_text((kord[i][0] + kord[j][0] - 90) / 2, (kord[i][1] + kord[j][1]) / 2 - 18,
    #                               text=fill_cell_list_0[i][j],
    #                               font='Verdana 14')
    #             for k in range(2, math.ceil(dim / 3) + 1):
    #                 if ur_i == ur_j - k and ((i + 1) % 3 == 1 or (i + 1) % 3 == 2):
    #                     if k >= 4:
    #                         g.create_line((kord[i][0] - 5, kord[i][1] - 20), (kord[i][0] + 60, r),
    #                                       (kord[i][0] + 60 + 250 * k, r),
    #                                       (kord[j][0] - 5, kord[j][1] - 20), arrow=LAST, width=3,
    #                                       fill=color, arrowshape="10 20 10")
    #                         g.create_text((kord[i][0] + 60 + kord[i][0] + 60 + 250 * k) / 2, r - 16,
    #                                       text=fill_cell_list_0[i][j], font='Verdana 14', fill=color)
    #                         r += 15
    #                     else:
    #                         g.create_line((kord[i][0] - 5, kord[i][1] - 20), (kord[i][0] + 60, r),
    #                                       (kord[i][0] + 60 + 150 * k, r),
    #                                       (kord[j][0] - 80, kord[j][1] - 20), arrow=LAST, width=3, fill=color,
    #                                       arrowshape="10 20 10")
    #                         g.create_text((kord[i][0] + 60 + kord[i][0] + 60 + 150 * k) / 2, r - 16,
    #                                       text=fill_cell_list_0[i][j],
    #                                       font='Verdana 14', fill=color)
    #                         r += 15
    #                 elif ur_i == ur_j - k and (i + 1) % 3 == 0:
    #                     if k >= 4:
    #                         g.create_line((kord[i][0] + 5, kord[i][1] + 20), (kord[i][0] + 60, r1),
    #                                       (kord[i][0] + 60 + 250 * k, r1),
    #                                       (kord[j][0] + 5, kord[j][1] + 20), arrow=LAST, width=3,
    #                                       fill=color,
    #                                       arrowshape="10 20 10")
    #                         g.create_text((kord[i][0] + 60 + kord[i][0] + 60 + 250 * k) / 2, r1 - 16,
    #                                       text=fill_cell_list_0[i][j], font='Verdana 14', fill=color)
    #                         r1 += 15
    #                     else:
    #                         g.create_line((kord[i][0], kord[i][1] + 10), (kord[i][0] + 60, r1),
    #                                       (kord[i][0] + 60 + 150 * k, r1),
    #                                       (kord[j][0] - 80, kord[j][1] + 20), arrow=LAST, width=3, fill=color,
    #                                       arrowshape="10 20 10")
    #                         g.create_text((kord[i][0] + 60 + kord[i][0] + 60 + 150 * k) / 2, r1 - 16,
    #                                       text=fill_cell_list_0[i][j],
    #                                       font='Verdana 14', fill=color)
    #                         r1 += 15
    #                 elif ur_i == ur_j + k and ((i + 1) % 3 == 1 or (i + 1) % 3 == 2):
    #                     if k>= 4:
    #                         g.create_line((kord[i][0]-5, kord[i][1]-20), (kord[i][0]-60, r),
    #                                       (kord[i][0] - 70 - 250 * k, r), (kord[j][0]+5, kord[j][1]+20),
    #                                       arrow=LAST, width=3, fill=color, arrowshape='10 20 10')
    #                         g.create_text((kord[i][0]-60 + kord[i][0] - 60 - 250 * k)/2, r-16,
    #                                       text=fill_cell_list_0[i][j], font='Verdana 14', fill=color)
    #                         r += 15
    #                     else:
    #                         g.create_line((kord[i][0]-90, kord[i][1]), (kord[i][0]-130, r),
    #                                       (kord[i][0] -120 - 150 * k, r), (kord[j][0], kord[j][1]),
    #                                       fill=color, arrow=LAST, arrowshape='10 20 10', width=3)
    #                         g.create_text((kord[i][0]-30 + kord[i][0] -60 - 150 * k)/2, r-16,
    #                                       text=fill_cell_list_0[i][j], fill=color, font='Verdana 14')
    #                         r += 15
    #                 elif ur_i == ur_j + k and (i + 1) % 3 == 0:
    #                     if k >= 4:
    #                         g.create_line((kord[i][0] - 90, kord[i][1]), (kord[i][0] - 80, r1),
    #                                       (kord[i][0] - 90 - 250 * k, r1),
    #                                       (kord[j][0], kord[j][1]), arrow=LAST, width=3,
    #                                       fill=color,
    #                                       arrowshape="10 20 10")
    #                         g.create_text((kord[i][0] - 90 + kord[i][0] - 70 - 250 * k) / 2, r1 - 16,
    #                                       text=fill_cell_list_0[i][j], font='Verdana 14', fill=color)
    #                         r1 += 15
    #                     else:
    #                         g.create_line((kord[i][0], kord[i][1]), (kord[i][0] - 80, r1),
    #                                       (kord[i][0] - 90 - 150 * k, r1),
    #                                       (kord[j][0], kord[j][1]), arrow=LAST, width=3, fill=color,
    #                                       arrowshape="10 20 10")
    #                         g.create_text((kord[i][0] - 80 + kord[i][0] - 60 - 150 * k) / 2, r1 - 16,
    #                                       text=fill_cell_list_0[i][j],
    #                                       font='Verdana 14', fill=color)
    #                         r1 += 15


def trans_graph():
    global dim, result, new_matr, m
    temp = []
    m = []
    for i in range(dim):
        for j in range(dim):
            temp.append(new_matr[i][j].get())
        m.append(temp)
        temp = []
    for i in range(dim):
        for j in range(dim):
            if m[i][j] == '':
                m[i][j] = '0'
            m[i][j] = int(m[i][j])
    G = nx.from_numpy_matrix(np.matrix(fill_cell_list_0), create_using=nx.DiGraph)
    layout = nx.spring_layout(G)
    nx.draw(G, layout, with_labels=True)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)
    try:
        zukl = nx.find_cycle(G)
        messagebox.showinfo(message=f'В графе найден цикл {zukl}')
    except:
        plt.show()
    # window_4 = Tk()
    # window_4.title('Упорядоченный граф')
    # d = Canvas(window_4, width=1800, height=700)
    # d.pack()
    # new_matr1 = []
    # temp = []
    # for i in range(dim):
    #     for j in range(dim):
    #         s = new_matr[i][j].get()
    #         temp.append(s)
    #     new_matr1.append(temp)
    #     temp = []
    # start_x, start_y = 10, 100
    # n = 1
    # kord = []
    # dict1 = {}
    # for i in range(len(result)):
    #     for j in range(len(result[i])):
    #         d.create_oval((start_x, start_y), (start_x + 70, start_y + 70), width=3, outline=random.choice(COLORS))
    #         d.create_text(start_x + 35, start_y + 35, text=f'{n} ( {result[i][j]} )')
    #         dict1.update({n: result[i][j]})
    #         kord.append([start_x + 70, start_y + 35])
    #         start_y += 150
    #         n += 1
    #     start_x += 250
    #     start_y = 100
    # ur_i = 0
    # ur_j = 0
    # print(result)
    # print(dict)
    # for i in range(dim):
    #     random.seed(17)
    #     for j in range(dim):
    #         c = random.choice(COLORS)
    #         if new_matr1[i][j] != '':
    #             for k in range(len(result)):
    #                 if dict1[i + 1] in result[k]:
    #                     ur_i = k + 1
    #             for k in range(len(result)):
    #                 if dict1[j + 1] in result[k]:
    #                     ur_j = k + 1
    #             if ur_i == ur_j - 1:
    #                 d.create_line((kord[i][0], kord[i][1]), (kord[j][0] - 70, kord[j][1]),
    #                               width=3, arrowshape="10 20 10", arrow=LAST, fill=c)
    #                 d.create_text(((kord[i][0] - random.randint(-35, 35) + kord[j][0] - 70) / 2),
    #                               ((kord[i][1] - random.randint(-35, 35) + kord[j][1]) / 2 - 10), text=new_matr1[i][j],
    #                               fill=c, font='Verdana 14')
    #             if ur_i - ur_j >= 2:
    #                 r = 15
    #                 for s in range(2, len(result)):
    #                     d.create_line((kord[i][0], kord[i][1]), (kord[i][0] + 50, r), (230 * s, r),
    #                                   (kord[j][0], kord[j][1]),
    #                                   width=3, arrowshape='10 20 10', arrow=LAST, fill=c)
    #                     d.create_text((kord[i][0] + 50 + 230 * s) / 2, (r + r) / 2 - 16, text=new_matr1[i][j], fill=c)
    #                     r += 15


#main

m = []
result, fill_cell_list_0, new_matr = [], [], []
empty_cell_list, fill_cell_list, renum_list = [], [], []
dim, height, size = 0, 0, 0
window = Tk()
window.geometry('1440x900')
window.title('Упорядочивание графов')
v = StringVar()
v1 = StringVar()
v2 = StringVar()
stok = Entry(window, width=5, textvariable=v1)
istok = Entry(window, width=5, textvariable=v2)
dim_label = Label(window, text='Введите размерность матрицы  ')
dim_box = Entry(window, width=5, textvariable=v)
dim_label.grid(column=0, row=0)
dim_box.grid(column=1, row=0)
Label(window, text='  ').grid(column=2, row=0)
dim_set_btn = Button(window, text='Применить', command=set_dim_click)
dim_set_btn.grid(column=3, row=0)
COLORS = ['gainsboro', 'bisque', 'peach puff', 'lavender', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
          'gray', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue', 'slate blue', 'medium slate blue',
          'medium blue', 'royal blue', 'blue',
          'dodger blue', 'deep sky blue', 'sky blue', 'steel blue', 'powder blue', 'pale turquoise', 'dark turquoise',
          'medium turquoise', 'turquoise',
          'cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green', 'dark sea green',
          'sea green', 'medium sea green', 'pale green', 'spring green',
          'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green', 'forest green',
          'olive drab', 'dark khaki', 'khaki', 'pale goldenrod',
          'gold', 'goldenrod', 'dark goldenrod', 'rosy brown', 'indian red', 'saddle brown', 'sandy brown',
          'dark salmon', 'salmon', 'orange', 'dark orange', 'coral', 'tomato', 'orange red', 'red', 'hot pink',
          'deep pink', 'pink',
          'pale violet red', 'maroon', 'medium violet red', 'violet red', 'medium orchid', 'dark violet', 'blue violet',
          'purple', 'medium purple',
          'thistle', 'SlateBlue1', 'RoyalBlue1', 'SteelBlue1', 'SkyBlue1', 'SlateGray1', 'CadetBlue1',
          'turquoise1', 'DarkSlateGray1', 'SeaGreen1', 'PaleGreen1', 'OliveDrab1', 'DarkOliveGreen1', 'khaki1',
          'yellow2', 'goldenrod1', 'DarkGoldenrod1', 'RosyBrown1', 'IndianRed1', 'sienna1', 'burlywood1', 'wheat1',
          'tan1',
          'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
          'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
          'salmon3', 'salmon4', 'orange2', 'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3',
          'DarkOrange4',
          'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
          'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
          'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4', 'PaleVioletRed1',
          'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2', 'maroon3', 'maroon4',
          'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
          'magenta2', 'magenta3', 'magenta4', 'orchid1', 'plum1', 'MediumOrchid1', 'DarkOrchid1', 'purple1', 'gray1']
window.mainloop()
