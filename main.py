import tkinter
from tkinter import *
import numpy
newton_cache = {}
def prog1():
    import turtle

    t = turtle.Turtle()
    s = turtle.Screen()
    s.bgcolor("black")
    t.pencolor("white")
    t.speed(0)
    c = 0
    while True:
        for i in range(4):
            t.forward(80)
            t.right(90)
        t.right(5)
        c += 1
        if c >= 360 / 5:
            break
    t.hideturtle()

    turtle.done()
def prog2():

    newton_cache = {}  # pamięć podręczna dla wyników funkcji newton

    def Newton(n, k):
        '''Funkcja oblicza wartość symbolu Newtona'''
        global newton_cache
        if (n, k) not in newton_cache:
            # licznik = n*(n-1)*...*(n-k+1)
            licznik = 1
            for i in range(n - k + 1, n + 1):
                licznik *= i

            # mianownik = k!
            mianownik = 1
            for i in range(1, k + 1):
                mianownik *= i

            newton_cache[(n, k)] = licznik / mianownik

        return newton_cache[(n, k)]

    def B(n, i, t):
        '''
        Funkcja oblicza wartość wielomianu bazowego Brensteina dla
        zadanego parametru t.
        '''
        return Newton(n, i) * (t ** i) * (1.0 - t) ** (n - i)

    def Bezier2D(punkty_kontrolne, k):
        '''
        Funkcja przybliża dwuwymiarową krzywą Beziera za pomocą łamanej
        złożonej z k segmentów. Zwraca listę wierzchołków łamanej.

        punkty_kontrolne - lista punktów kontrolnych: [(x0,y0), ..., (xn,yn)]
        k                - ilość segmentów
        '''

        n = len(punkty_kontrolne) - 1  # stopień krzywej Beziera

        # funkcja obliczająca współrzędne (x,y) punktu krzywej dla zadanego t
        def p(t):
            '''
            x = \sum_{i=0}^n x_i B^n_i(t)
            y = \sum_{i=0}^n y_i B^n_i(t)
            '''
            x = 0.0
            y = 0.0
            for i in range(n + 1):
                x += punkty_kontrolne[i][0] * B(n, i, t)
                y += punkty_kontrolne[i][1] * B(n, i, t)
            return (x, y)

        dt = 1.0 / k  # krok parametru t
        return [p(i * dt) for i in range(k + 1)]

    # program główny
    if __name__ == '__main__':
        from PIL import Image, ImageDraw

        # parametry programu

        rozdzielczosc = 600  # rozdzielczość obrazów
        k = 200  # liczba segmentów łamanej przybliżającej krzywą
        l = 1  # liczba obrazów generowanych przy jednym
        # uruchomieniu programu

        image = Image.new("RGB", (rozdzielczosc, rozdzielczosc))
        draw = ImageDraw.Draw(image)
        from random import randint as R

        # 3. Rysowanie krzywej:
        # 3a. wyczyszczenie obrazu (kolorem białym)

        # DEKLAROWANIE DLUGOSCI I ILOSCI PUNKTOW KONTRORLNYCH PRZY UZYCIU RANDOMOWYCH PUNKTOW
        n = 3  # liczba punktów kontrolnych (stopień krzywej+1)
        Lp = 3  # liczba krzywych ktora powstanie
        # losowanie liczb do tablicy (test wielu krzywych)
        draw.rectangle([0, 0, rozdzielczosc, rozdzielczosc], fill="#fff")
        import numpy as np
        a = np.random.randint(1, rozdzielczosc, size=(Lp, n * 2))

        for i in range(l):
            print("Tworzenie krzywej %d z %d" % (i + 1, l))
            # 1. Wylosowanie n punktów kontrolnych
            #    (oczywiście można je wpisać ręcznie, do czego zachęcamy)
            for z in range(len(a)):

                punkty_kontrolne = [(a[z][0], a[z][1]), (a[z][2], a[z][3]), (a[z][4], a[z][5])]
                # 2. Wyznaczenie łamanej p przyliżającą krzywą Beziera
                p = Bezier2D(punkty_kontrolne, k)

                # 3b. rysowanie łamanej kontrolnej (w kolorze jasnoszarym)
                draw.line(punkty_kontrolne, fill="#ccc")

                # 3c. zaznaczenie niebieskimi kółkami punktów kontrolnych
                r = 2  # promień
                for (x, y) in punkty_kontrolne:
                    draw.ellipse([x - r, y - r, x + r, y + r], fill="#00f")

                # 3d. rysowanie krzywej Beziera (w kolorze czerownym)
                draw.line(p, fill="#f00")

            # 4. Zapisanie obrazu do pliku
            image.save("Krzywa.png", "PNG")
            img= Image.open("Krzywa.png")
            img.show()
def prog3():
    import random, time
    class Snake(Tk):
        def __init__(self, *arge, **kwargs):
            Tk.__init__(self, *arge, **kwargs)
            self.initialSetup()

        def initialSetup(self):
            self.base = Canvas(self, width=500, height=500)
            self.base.pack(padx=10, pady=10)
            self.snake = self.base.create_rectangle(1, 1, 21, 21, fill="DodgerBlue2")
            self.score = 0
            self.scoreDisplay = Label(self, text="Score:{}".format(self.score), font=('arial', 20, 'bold'))
            self.scoreDisplay.pack(anchor='n')
            self.length = 3
            self.target = None
            self.gameStatus = 1
            self.x = 20
            self.y = 0
            self.bodycoords = [(0, 0)]
            self.bind('<Any-KeyPress>', self.linkKeys)
            return

        def check_snake_coords(self):
            self.base.move(self.snake, self.x, self.y)
            i, j, ii, jj = self.base.coords(self.snake)
            if i <= 0 or j <= 0 or ii >= 500 or jj >= 500:
                self.x = 0
                self.y = 0
                # gameover
                self.base.create_text(220, 220, text="GAME OVER", font=('arial', 40, 'bold'), fill='red')
                self.gameStatus = 0
            return

        def move_snake(self):
            i, j, ii, jj = self.base.coords(self.snake)
            ii = (ii - ((ii - i) / 2))
            jj = (jj - ((jj - j) / 2))
            self.bodycoords.append((ii, jj))
            self.base.delete('snakebody')
            if len(self.bodycoords) >= self.length:
                self.bodycoords = self.bodycoords[-self.length:]
            self.base.create_line(tuple(self.bodycoords), tag='snakebody', width=20, fill="DodgerBlue2")
            return

        def food(self):
            if self.target == None:
                a = random.randint(20, 480)
                b = random.randint(20, 480)
                self.target = self.base.create_oval(a, b, a + 20, b + 20, fill='red', tag='food')
                # print(self.base.coords(self.target))
            if self.target:
                # print(self.base.coords(self.target))
                i, j, ii, jj = self.base.coords(self.target)
                # time.sleep(0.1)
                if len(self.base.find_overlapping(i, j, ii, jj)) != 1:
                    self.base.delete("food")
                    self.target = None
                    self.updateScore()
                    self.length += 1
                return

        def updateScore(self):
            self.score += 1
            self.scoreDisplay['text'] = "Score : {}".format(self.score)
            return

        def linkKeys(self, event=None):
            pressedkey = event.keysym
            if pressedkey == 'Left':
                self.x = -20
                self.y = 0
            elif pressedkey == 'Up':
                self.x = 0
                self.y = -20
            elif pressedkey == 'Right':
                self.x = 20
                self.y = 0
            elif pressedkey == 'Down':
                self.x = 0
                self.y = 20
            else:
                pass
            return

        def manage(self):
            if (self.gameStatus == 0):
                return
            self.check_snake_coords()
            self.move_snake()
            self.food()

            return

    snakeobj = Snake(className="Snake")
    while True:
        snakeobj.update()
        snakeobj.update_idletasks()
        snakeobj.manage()
        time.sleep(0.4)
window = tkinter.Tk()
window.title("Projekt")
window.geometry('500x500')
guzik1 =Button(text="Rysunek",
                   bd=10,
                   bg="grey",
                   fg="red",
                   command=prog1,
                   activeforeground="Orange",
                   activebackground="blue",
                   font="Andalus",
                   height=2,
                   highlightcolor="purple",
                   justify="right",
                   padx=10,
                   pady=10,
                   relief="groove")
guzik1.pack(side=LEFT,expand=YES)
guzik2 =Button(text="krzywe",
                   bd=10,
                   bg="grey",
                   fg="red",
                   command=prog2,
                   activeforeground="Orange",
                   activebackground="blue",
                   font="Andalus",
                   height=2,
                   highlightcolor="purple",
                   justify="right",
                   padx=10,
                   pady=10,
                   relief="groove")
guzik2.pack(side=LEFT,expand=YES)
guzik3 =Button(text="Snake",
                   bd=10,
                   bg="grey",
                   fg="red",
                   command=prog3,
                   activeforeground="Orange",
                   activebackground="blue",
                   font="Andalus",
                   height=2,
                   highlightcolor="purple",
                   justify="right",
                   padx=10,
                   pady=10,
                   relief="groove")
guzik3.pack(side=LEFT,expand=YES)
# guzik4 =
window.mainloop()


