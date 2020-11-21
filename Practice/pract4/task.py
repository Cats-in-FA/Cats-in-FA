import tkinter as tk
from functools import partial
import random
root = tk.Tk()

#TODO проверка на окончание игры (победа, проигрыш)
#TODO ведение счета

class Cell:
    """Класс клетки на поле"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self._isbomb = None
        self.value = None
        self.isclicked = False
        self.isquestion = False
        self.isflag = False


    def click(self):
        """Обработка нажатия на кнопку"""
        if (not self.isflag) and (not self.isquestion):
            self.isclicked = True

    @property
    def isbomb(self):
        return self._isbomb

    @isbomb.setter
    def isbomb(self, value):
        """Выставление бомбы"""
        self._isbomb = value
        self.value = "x"


class Field:
    """Класс игрового поля"""

    @staticmethod
    def reloadbutton_click():
        """Обработка нажатия на button перезапуска игры"""
        return Field(10,10)

    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.first_click = True

        self.matrix = None
        self.buttons_matrix = None

        self.generation()
        self.buttonsmatrix_filler()
        self.synchronizer()

    def filler(self, coords=()):
        """Заполнение матрицы данными"""
        x_first, y_first = coords
        matrix = self.matrix

        #Логика расстановки бомб на игровом поле
        bomb_counter = 0

        while bomb_counter < (self.n+self.m):
            x_coord, y_coord = random.randint(0, self.n-1), random.randint(0, self.m-1)
            #Если выбранная клетка не бомба, то она станет бомбой
            if (not matrix[x_coord][y_coord].isbomb) and (x_coord != x_first) and (y_coord != y_first):
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

    def matrixbutton_leftclick(self, coords, event):
        """Обработка нажатия на button"""
        # Если первое нажатие
        if self.first_click:
            self.filler(coords)
            self.first_click = False
        x, y = coords
        self.matrix[x][y].click()

        # Если значение ячейки 0, то раскрываем соседние ячейки до тех пор, пока не до дойдем до ячейки с числом
        if self.matrix[x][y].value == 0:
            self.recursion_clicker(x, y)
        elif self.matrix[x][y].isclicked and self.matrix[x][y].value == "x":
            self.bombs_opening()
            # TODO конец игры

        self.synchronizer()

    def matrixbutton_rightclick(self, coords, event):
        """Обработка выставляения флага/вопроса на button"""
        x, y = coords
        if self.matrix[x][y].isflag:
            self.matrix[x][y].isflag=False
            self.matrix[x][y].isquestion=True
        elif self.matrix[x][y].isquestion:
            self.matrix[x][y].isquestion=False
        else:
            self.matrix[x][y].isflag=True
        self.synchronizer()

    def recursion_clicker(self, x, y, first_flag=True):
        """Рекурсивное раскрытитие соседних ячеек"""
        #Проверка на выход из диапазона
        if x > self.n-1 or x < 0 or y > self.m-1 or y < 0:
            return

        #Если уже кликнули на эту ячейку и это не 1 итерация - выходим
        if not first_flag and self.matrix[x][y].isclicked:
            return
       
        #Раскрываем ячейку
        self.matrix[x][y].click()

        #Если значение этой ячейки 0, то запускаем рекурсия
        if self.matrix[x][y].value == 0:
            for a in range(3):
                for b in range(3):
                    self.recursion_clicker(x-1+a, y-1+b, False)

        else:
            return

    def bombs_opening(self):
        """Раскрытие всех бомб на поле"""
        for x in range(self.n):
            for y in range(self.m):
                if self.matrix[x][y].isbomb:
                    self.matrix[x][y].click()

    def generation(self):
        """Генерация основной матрицы"""
        matrix = []
        for i in range(self.n):
            buf_matrix = []
            for j in range(self.m):
                buf_matrix.append(Cell(i, j))
            matrix.append(buf_matrix)
        self.matrix = matrix

    def buttonsmatrix_filler(self):
        """Генерация матрицы buttonов и элементов интерфейса"""

        buttons_matrix = []
        for c in range(self.n):
            row = []
            for r in range(self.m):
                #Генерация buttonов
                action_left = partial(self.matrixbutton_leftclick, (c,r))
                action_right = partial(self.matrixbutton_rightclick, (c,r))
                button = tk.Button(root, text=str(self.matrix[c][r].value)) 
                #Обработка нажатий мышью
                button.bind("<Button-1>", action_left)
                button.bind("<Button-2>", action_right)
                button.bind("<Button-3>", action_right)
                button.grid(row=c+1, column=r+1)
                row.append(button)
            buttons_matrix.append(row)

            label1 = tk.Label(text="Ваш счёт:")
            label2 = tk.Label(text="Ваш счёт:")
            reload_button = tk.Button(root, text="Перезапуск", command=Field.reloadbutton_click)

            #Привязка прочих элементов к сетке
            label1.grid(row=1, column=0)
            label2.grid(row=2, column=0)

            reload_button.grid(row=self.n, column=0)
        self.buttons_matrix = buttons_matrix
    
    def synchronizer(self):
        """Синхронизация значений в self.matrix с buttons_matrix"""
        number2color_dict = {
            "0" : "white",
            "1" : "royal blue",
            "2" : "forest green",
            "3" : "red2",
            "4" : "medium blue",
            "5" : "red4",
            "6" : "turquoise4",
            "7" : "dark orchid",
            "8" : "dark slate blue",
            "x" : "black",
        }
        for c in range(self.n):
            for r in range(self.m):
                #Если нет нажатия на button - значение неизвестно
                if not self.matrix[c][r].isclicked:           
                    self.buttons_matrix[c][r].config(text="    ")
                    #Если мы поставили флаг или вопрос
                    if self.matrix[c][r].isflag:
                        self.buttons_matrix[c][r].config(text=" F ")
                    elif self.matrix[c][r].isquestion:
                        self.buttons_matrix[c][r].config(text=" ? ")
                #Если нажали на кнопку
                else:
                    value = self.matrix[c][r].value
                    self.buttons_matrix[c][r].config(text=" {} ".format(str(value).replace("0", "  ")), disabledforeground=number2color_dict[str(value)], state=tk.DISABLED, bg="#b8b8b8", relief="flat")

    def __str__(self):
        """Вывод матрицы на экран"""
        matrix = self.matrix
        for i in range(self.n):
            for j in range(self.m):
                print(matrix[i][j].value, end=' ')
            print('')
        return ""
    
def main():
    
    root.title("Сапёр")
    #Экземпляр игрового поля
    Field.reloadbutton_click()
    root.mainloop()

if __name__ == "__main__":
    main()