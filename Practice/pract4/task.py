import tkinter as tk
from functools import partial
import random
root = tk.Tk()

#TODO проверка на окончание игры (победа, проигрыш)
#TODO открытие всех бомб после окончания игры
#TODO фильтрация на первый ход (БОМБА)
#TODO выставление игроком флагов и вопросов
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
    def reloadbutton_click(obj=None):
        """Обработка нажатия на button перезапуска игры"""
        
        game_counter = 1
        #Если уже играли, то берем номер игры из объекта предыдущей игры
        if obj is not None and isinstance(obj, Field):
            game_counter = obj.game_number
            game_counter += 1

        return Field(10,10, game_counter)

    def __init__(self, n, m, game_number):
        self.n = n
        self.m = m
        self.game_number = game_number
        print("ИГРА НОМЕР")
        print(game_number)

        self.matrix = None
        self.buttons_matrix = None

        self.generation()
        self.filler()
        self.buttonsmatrix_filler()
        self.synchronizer()

    def filler(self):
        """Заполнение матрицы данными"""
        
        matrix = self.matrix

        #Логика расстановки бомб на игровом поле
        bomb_counter = 0

        while bomb_counter < (self.n+self.m):
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

    def matrixbutton_leftclick(self, coords, event):
        """Обработка нажатия на button"""
        x, y = coords
        self.matrix[x][y].click()

        # Если значение ячейки 0, то раскрываем соседние ячейки до тех пор, пока не до дойдем до ячейки с числом
        if self.matrix[x][y].value == 0:
            self.recursion_clicker(x, y)

        self.synchronizer()

    # TODO
    def matrixbutton_rightclick(self, coords, event):
        """Обработка выставляения флага/вопроса на button"""
        x, y = coords
        print("НАЖАЛИ НА ПРАВУЮ")


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
            label3 = tk.Label(text="Игра №{}".format(self.game_number))
            reload_button = tk.Button(root, text="Перезапуск", command=Field.reloadbutton_click)

            #Привязка прочих элементов к сетке
            label1.grid(row=1, column=0)
            label2.grid(row=2, column=0)

            reload_button.grid(row=self.n-1, column=0)
            label3.grid(row=self.n, column=0)
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
            "6" : "turquoise4", #аква
            "7" : "dark orchid", #фиолетовый
            "8" : "dark slate blue",
            "x" : "black",
        }
        for c in range(self.n):
            for r in range(self.m):
                #Если нет нажатия на button - значение неизвестно
                if not self.matrix[c][r].isclicked:           
                    self.buttons_matrix[c][r].config(text="    ")
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
    obj = Field.reloadbutton_click()
    root.mainloop()
    

if __name__ == "__main__":
    main()