import tkinter as tk
from functools import partial
import random
#Разрешение окна
WIDTH = 750
HEIGHT = 750
FIELD_ROWS = 10
FIELD_COLUMNS = 10

class Cell:
    """Класс клетки на поле"""
    
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

        #С этими полями работать через гетеры/сеттеры
        self.isbomb = None
        self.value = None

    #TODO при добавлении tkinter
    def click(self):
        """Обработка нажатия"""
        pass


class Field:
    """Класс игрового поля"""

    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.matrix = None
        self.generation()
        self.filler()
    
    def generation(self):
        """Генерация матрицы"""
        matrix = []
        for i in range(self.n):
            buf_matrix = []
            for j in range(self.m):
                buf_matrix.append(Cell(i, j))
            matrix.append(buf_matrix)
        self.matrix = matrix

    def filler(self):
        """Заполнение матрицы данными"""
        
        matrix = self.matrix

        #Логика расстановки бомб на игровом поле
        bomb_counter = 0
        while bomb_counter < (self.n + self.m):
            x_coord, y_coord = random.randint(0, self.n-1), random.randint(0, self.m-1)
            #Если выбранная клетка не бомба, то она станет бомбой
            if not matrix[x_coord][y_coord].isbomb:
                matrix[x_coord][y_coord].isbomb = True
                bomb_counter += 1

        #Логика выставления чисел
        for i in range(self.n):
            for j in range(self.m):
                # Если это не бомба - присваиваем ей значение
                if not matrix[i][j].isbomb:
                    buf_value = 0
                    for a in range(3):
                        for b in range(3):
                            if (0<=(i-1+a)<self.n) and (0<=(j-1+b)<self.m) and (matrix[i-1+a][j-1+b].isbomb):
                                buf_value+=1 #Если клетка внутри поля и это бомба, то считаем
                    matrix[i][j].value = buf_value
        
        self.matrix = matrix
        
    def __str__(self):
        """Вывод матрицы на экран"""
        matrix = self.matrix
        for i in range(self.n):
            for j in range(self.m):
                if matrix[i][j].isbomb:
                    print("*", end=' ')
                else:
                    print(matrix[i][j].value, end=' ')
            print('')
        return ""

def button_click(coords):
    """Обработка начатия на button"""
    x, y = coords
    print("[{},{}] clicked".format(x,y))
    
def main():
    
    #Инициализация канваса
    root = tk.Tk()
    c = tk.Canvas(root, width=WIDTH, heigh=HEIGHT)
    root.title("Сапёр")

    # Ето рабочий пример-демо
    buttons_matrix = []
    for c in range(FIELD_COLUMNS):
        row = []
        for r in range(FIELD_ROWS):
            action = partial(button_click, (c,r))
            button = tk.Button(root, text="{}:{}".format(c,r), command=action, highlightbackground='#3E4149')
            button.grid(row=r, column=c, sticky=tk.NW+tk.NE+tk.SW+tk.SE+tk.W+tk.E+tk.N+tk.S)
            row.append(button)
        buttons_matrix.append(row)
    root.mainloop()
    
    #Ето вызов экземпляра Поля сапёра
    #Field1 = Field(FIELD_COLUMNS,FIELD_ROWS)
    #print(Field1)

if __name__ == "__main__":
    main()