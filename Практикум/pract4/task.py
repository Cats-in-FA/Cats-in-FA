import random

class Cell:
    """Класс клетки на поле"""
    
    def __init__(self, x, y, isbomb=False, value=0) -> None:
        self.x = x
        self.y = y
        self.isbomb = isbomb
        self.value = value

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

    #TODO
    def filler(self):
        """Заполнялка матрицы данными с бомбами"""
        i = 0
        matrix = self.matrix
        while i <= (self.n + self.m): #Рандомная пропорция на количество бомб на поле
            a = random.randint(0, self.n-1)
            b = random.randint(0, self.m-1)
            if not matrix[a][b].isbomb:
                matrix[a][b].isbomb = True
                i += 1 #счетчик без for, не бей меня :D
        for i in range(self.n): #Проставляем числа
            for j in range(self.m):
                if not matrix[i][j].isbomb: #Считаем бомбы
                    count = 0
                    for a in range(3):
                        for b in range(3):
                            if (0<=(i-1+a)<self.n) and (0<=(j-1+b)<self.m) and (matrix[i-1+a][j-1+b].isbomb): count+=1 #Если клетка внутри поля и это бомба, то считаем
                    matrix[i][j].value = count
        self.matrix = matrix
        
    def __str__(self):
        """Вывод матрицы на экран"""
        matrix = self.matrix
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j].isbomb:
                    print("*", end=' ')
                else:
                    print(matrix[i][j].value, end=' ')
            print('')
        return ""

def main():
    Field1 = Field(10,10)
    print(Field1)

if __name__ == "__main__":
    main()