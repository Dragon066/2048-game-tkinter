import tkinter
import numpy as np
import time
from copy import deepcopy


class Node():
    colors = ['lightgrey', '#4ed9bf', '#42c1d6', '#4268d6', '#a842d6',
             '#d6429a', '#d64242', '#d68b42', '#d2d642',
             '#80d642', '#42d662', '#ebff23']
    
    def __init__(self, canvas, x, y, value=0, width=100, color='white'):
        self.c = canvas
        self.x = x
        self.y = y
        self.value = value
        self.width = width
        self.obj = None
        self.text = None
        self.color = color
            
    def draw_cell(self):
        if self.obj:
            self.c.delete(self.obj)
        if self.value == 0:
            self.color = Node.colors[0]
        else:
            self.color = Node.colors[int(np.log2(self.value)) % len(Node.colors) + (1 if int(np.log2(self.value)) >= len(Node.colors) else 0)]
        self.obj = create_rounded(self.c, self.width * self.x + 5, self.width * self.y + 5, (self.x + 1) * self.width - 5, (self.y + 1) * self.width - 5, radius=18, fill=self.color)
        
    def draw_text(self):
        if self.text:
            self.c.delete(self.text)
        if self.value != 0:
            self.text = self.c.create_text(self.x * self.width + 0.5 * self.width, self.y * self.width + 0.5 * self.width, text=self.value, font=("Helvetica 15 bold"))
    
    def animate_draw(self, c=255):
        self.c.itemconfig(self.obj, outline="#%02x%02x%02x" % (c, 0, 0), width=20/(np.log2(256 - c) + 1))
        
        if c > 50:
            window.after(1, lambda: self.animate_draw(c - 1))
        else:
            self.c.itemconfig(self.obj, outline='black', width=1)
            
    def animate(self, c=255, obj=None):
        if not(obj):
            obj = create_rounded(self.c, self.width * self.x + 5, self.width * self.y + 5, (self.x + 1) * self.width - 5, (self.y + 1) * self.width - 5, radius=18, fill=None)
        
        self.c.itemconfig(obj, outline="#%02x%02x%02x" % (0, c, 0), width=20/(np.log2(256 - c) + 1))
        
        if c > 0:
            window.after(1, lambda: self.animate(c - 1, obj))
        else:
            self.c.delete(obj)
            
            
class Field():
    def __init__(self, c, width=120):
        self.c = c
        self.field = Field.gen_field(c, width)
        self.width = width
        self.field_visual = Field.gen_field_visual(c, width)
        
    @classmethod
    def gen_field_visual(cls, c, width):
        field = []
        for i in range(4):
            field.append([])
            for j in range(4):
                field[i].append(c.create_rectangle(width * i + 2, width * j + 2, (i + 1) * width - 2, (j + 1) * width - 2, fill='grey'))
                c.pack()
        return field
        
    @classmethod
    def gen_field(cls, c, width):
        lst = []
        for i in range(4):
            lst.append([])
            for j in range(4):
                lst[i].append(Node(c, i, j, width=width))
                c.pack()
        return np.array(lst)
        
    def gen(self):
        num = np.random.choice([2, 4], p=[0.8, 0.2])
        mx = sum([1 for i in self.field for j in i if j.value == 0])
        pos = np.random.randint(1, mx + 1)
        c = 0
        for i in range(4):
            for j in range(4):
                if self.field[i, j].value == 0:
                    c += 1
                if c == pos:
                    self.field[i, j].value = num
                    self.draw(i, j)
                    return self.field[i, j]
                    
    def draw(self, x, y):
        cell = self.field[x, y]
        cell.draw_cell()
        cell.draw_text()
            
    def draw_all(self):
        for i in self.field:
            for j in i:
                j.draw_cell()
                j.draw_text()
                        
    def summ(self):
        summ = 0
        for i in self.field:
            for j in i:
                summ += j.value if j.value else 0
        return summ
    
    def shake_field(self, x=1, y=0, k=1):
        for i in np.array(self.field_visual).flatten():
            self.c.move(i, x, y)
            
        window.update()
        
        if k % 3 == 0:
            x, y = -x, -y
            
        if k <= 11:
            window.after(2, self.shake_field(x, y, k + 1))
    
    def move(self, direction):
        last = self.field.flatten()
        for i in range(16):
            last[i] = last[i].value
        
        if direction == 'left':
            for _ in range(10):
                for i in range(3, 0, -1):
                    for j in range(4):
                        if self.field[i - 1, j].value == 0:
                            self.field[i - 1, j].value = self.field[i, j].value
                            self.field[i, j].value = 0
                        if self.field[i, j].value == self.field[i - 1, j].value != 0:
                            self.field[i - 1, j].value *= 2
                            self.field[i, j].value = 0
                            self.field[i - 1, j].animate()
                        
        if direction == 'right':
            for _ in range(10):
                for i in range(3):
                    for j in range(4):
                        if self.field[i + 1, j].value == 0:
                            self.field[i + 1, j].value = self.field[i, j].value
                            self.field[i, j].value = 0
                        if self.field[i, j].value == self.field[i + 1, j].value != 0:
                            self.field[i + 1, j].value *= 2
                            self.field[i, j].value = 0
                            self.field[i + 1, j].animate()
                            
        if direction == 'up':
            for _ in range(10):
                for i in range(4):
                    for j in range(3, 0, -1):
                        if self.field[i, j - 1].value == 0:
                            self.field[i, j - 1].value = self.field[i, j].value
                            self.field[i, j].value = 0
                        if self.field[i, j].value == self.field[i, j - 1].value != 0:
                            self.field[i, j - 1].value *= 2
                            self.field[i, j].value = 0
                            self.field[i, j - 1].animate()
                            
        if direction == 'down':
            for _ in range(10):
                for i in range(4):
                    for j in range(3):
                        if self.field[i, j + 1].value == 0:
                            self.field[i, j + 1].value = self.field[i, j].value
                            self.field[i, j].value = 0
                        if self.field[i, j].value == self.field[i, j + 1].value != 0:
                            self.field[i, j + 1].value *= 2
                            self.field[i, j].value = 0
                            self.field[i, j + 1].animate()
                            
        self.draw_all()
        
        current = self.field.flatten()
        for i in range(16):
            current[i] = current[i].value
            
        if not (current != last).any():
            self.shake_field()
        
        return (current != last).any()
    
    def check_lose(self):
        current = self.field.flatten()
        for i in range(16):
            current[i] = current[i].value
        if len(current[current == 0]):
            return False
        current = current.reshape(4, 4)
        for i in range(4):
            for j in range(3):
                if current[i, j] == current[i, j + 1]:
                    return False
                
        current = np.transpose(current)
        for i in range(4):
            for j in range(3):
                if current[i, j] == current[i, j + 1]:
                    return False

        return True
    
    def check_win(self):
        current = self.field.flatten()
        for i in range(16):
            current[i] = current[i].value
        return 2048 in current
    
    def destroy(self):
        for i in self.field:
            for j in i:
                self.c.delete(j.obj)
                self.c.delete(j.text)
        for i in self.field_visual:
            for j in i:
                self.c.delete(j)
    
    
def create_rounded(c, x0, y0, x1, y1, radius, fill='white'):
    return c.create_polygon(
        x0, y0+radius,
        x0, y1-radius,
        x0+radius, y1,
        x1-radius, y1,
        x1, y1-radius,
        x1, y0+radius,
        x1-radius, y0,
        x0+radius, y0,
        outline='black', fill=fill, smooth=True
    )


window = tkinter.Tk()
window.title('Православный 2048')
window.geometry('481x600')

c = tkinter.Canvas(window, width=481, height=600)
c.pack()

c.create_rectangle(2, 482, 478, 597, fill='#a1a1a1')

score = c.create_text(445, 505, text=0, font=("Helvetica 40 bold"))
result = c.create_text(220, 540, font=("Helvetica 15 bold"), fill='gold', justify="center")
restarting = False

def update_score(field):
    summ = field.summ()
    c.itemconfig(score, text=summ)
    c.moveto(score, 440 - 29 * (len(str(summ)) - 1), 505)
    
    
def restart():
    global restarting
    restarting = True

b_restart = tkinter.Button(c, text='Начать\nсызнова ↺', width=15, height=6, command=restart, bg='#c2c227')
b_restart.place(x=10, y=490)
    
    
motion_flag = False
motion = [(0, 0), (0, 0)]
    
    
def track(event):
    global motion, motion_flag
    motion_flag = True
    motion[0] = (event.x, event.y)
    
def untrack(event):
    global motion, motion_flag
    motion[1] = (event.x, event.y)
    motion_flag = False
    
def arrows(event, direction):
    global motion
    motion = direction


c.bind('<ButtonPress-1>', track)
c.bind('<ButtonRelease-1>', untrack)

c.bind_all('<Up>', lambda e: arrows(e, [(0, 0), (0, -150)]))
c.bind_all('<Down>', lambda e: arrows(e, [(0, 0), (0, 150)]))
c.bind_all('<Right>', lambda e: arrows(e, [(0, 0), (150, 0)]))
c.bind_all('<Left>', lambda e: arrows(e, [(0, 0), (-150, 0)]))


def catch_motion():
    if not motion_flag:
        dx = motion[0][0] - motion[1][0]
        dy = motion[0][1] - motion[1][1]
        if abs(dx) < 100 and abs(dy) < 100:
            return None
        else:
            return dx, dy
        
        
def perform_move(field):
    global motion
    dx, dy = catch_motion()
    motion = [(0, 0), (0, 0)]
    direction = None
    
    if dx < -100 and abs(dy) < 100:
        direction = 'right'
    elif dx > 100 and abs(dy) < 100:
        direction = 'left'
    elif dy < -100 and abs(dx) < 100:
        direction = 'down'
    elif dy > 100 and abs(dx) < 100:
        direction = 'up'
    
    if not direction:
        return
    
    res = field.move(direction)
    
    if res:
        gen = field.gen()
        gen.animate_draw()
        
    if field.check_win():
        c.itemconfig(result, text='Православная\n☭ победа ☭', fill='gold')
        
    if field.check_lose():
        c.itemconfig(result, text='Гнусное\n👎 поражение 👎', fill='red')
    
    
def update(field):
    global restarting
    if restarting:
        field.destroy()
        field = Field(c)
        field.gen()
        field.gen()
        field.draw_all()
        restarting = False
        update_score(field)
        c.itemconfig(result, text='')
    
    if catch_motion():
        field.draw_all()
        perform_move(field)
        update_score(field)
        
    window.after(10, lambda: update(field))


def main():
    field = Field(c)
    field.gen()
    field.gen()
    field.draw_all()
    update_score(field)
    update(field)
    
    
main()

window.mainloop()
