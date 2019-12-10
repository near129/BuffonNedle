import random
import tkinter as tk
import numpy as np
import tkinter.ttk as ttk


class BufffonCal:
    def __init__(self, length, interval, width_x=800, width_y=600):
        self.length = length
        self.interval = interval
        self.width_x = width_x
        self.width_y = width_y
        # self.drops_x1 = []
        self.drops_y1 = []
        # self.drops_x2 = []
        self.drops_y2 = []
        self.drops = []
        self.counts = 0
        self.lines = []
        self.degree = 0
        self.number = 0

    def base_lines(self):
        self.lines = [i * self.interval for i in range(self.width_y // self.interval + 1)]
        return self.lines

    def drop(self, number):
        self.number = number
        self.degree = 0
        for i in range(self.number):
            self.drop_x1 = self.width_x * random.random()
            self.drop_y1 = self.width_y * random.random()
            theta = np.pi * random.random()
            self.drop_x2 = self.drop_x1 + self.length * np.cos(theta)
            self.drop_y2 = self.drop_y1 + self.length * np.sin(theta)
            # self.drops_x1.append(self.drop_x1)
            self.drops_y1.append(self.drop_y1)
            # self.drops_x2.append(self.drop_x2)
            self.drops_y2.append(self.drop_y2)
            self.degree += 1
            self.drops.append([self.drop_x1, self.drop_y1, self.drop_x2, self.drop_y2])
            print('\rrandom: {}%'.format(100 * self.degree / self.number), end='')
        print('')
        return self.drops

    def count(self):
        self.counts = 0
        self.degree = 0
        for y1, y2 in zip(self.drops_y1, self.drops_y2):
            for line_y in self.base_lines():
                if y1 <= line_y <= y2:
                    self.counts += 1
                    break
            self.degree += 1
            print('\rcount: {}%'.format(100 * self.degree / self.number), end='')
        


        return self.counts

    def pi_cal(self):
        if self.counts > 0:
            self.pi = (2*self.length*self.number) / (self.counts*self.interval)
        else:
            self.pi = float('inf')
        return self.pi


class BuffonAPP(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(padx=10, pady=10)
        self.reset()
        t = self.winfo_toplevel()
        t.resizable(False, False)

    def reset(self):
        self.state = 'OFF'
        self.interval = 100
        self.length = 50
        self.instance = BufffonCal(self.length, self.interval)
        self.number = 0
        self.count = 0
        self.pi = 0
        self.create_widgets()

    def create_widgets(self):
        self.frame1 = ttk.Frame(self)
        self.create_canvas(self.frame1)
        self.frame1.grid(row=0, column=0, rowspan=2, padx=10)

        self.frame2 = ttk.Frame(self)
        self.create_inputforms(self.frame2)
        self.frame2.grid(row=0, column=1)

        self.frame3 = ttk.Frame(self)
        self.create_outputforms(self.frame3)
        self.frame3.grid(row=1, column=1)

    def create_inputforms(self, frame):
        self.explain_n = ttk.Label(frame, text='drop number')
        self.explain_i = ttk.Label(frame, text='line distance')
        self.explain_l = ttk.Label(frame, text='needle length')
        self.form_n = ttk.Entry(frame, justify='right')
        self.form_n.insert(tk.END, self.number)
        self.form_i = ttk.Entry(frame, justify='right')
        self.form_i.insert(tk.END, self.interval)
        self.form_l = ttk.Entry(frame, justify='right')
        self.form_l.insert(tk.END, self.length)
        self.runbutton = ttk.Button(frame, text='Execute', command=self.calculate)
        # self.runbutton.bind('<Key-Return>', self.calculate())
        self.resetbutton = ttk.Button(frame, text='Reset', command=self.reset)

        self.explain_n.grid(row=0, column=0, columnspan=2, padx=5, pady=10)
        self.explain_i.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        self.explain_l.grid(row=4, column=0, columnspan=2, padx=5, pady=10)
        self.form_n.grid(row=1, column=0, columnspan=2, padx=5)
        self.form_i.grid(row=3, column=0, columnspan=2, padx=5)
        self.form_l.grid(row=5, column=0, columnspan=2, padx=5)
        self.runbutton.grid(row=6, column=0, padx=0, pady=10)
        self.resetbutton.grid(row=6, column=1, padx=0, pady=10)

    def create_outputforms(self, frame):
        self.result = ttk.Label(frame, text='---Result---')
        self.count_drops_text = ttk.Label(frame, text='cross: \ndrop: \npi:')
        self.count_drops = ttk.Label(frame, text='{0:10d}\n{1:10d}\n{2:10f}'.format(self.count, self.number, self.pi))

        self.result.grid(row=0, column=0, columnspan=2)
        self.count_drops_text.grid(row=1, column=0, stick='w')
        self.count_drops.grid(row=1, column=1, sticky='e')

    def create_canvas(self, frame):
        self.canvas = tk.Canvas(frame, width=self.instance.width_x, height=self.instance.width_y, background='white')
        for y in self.instance.base_lines():
            self.canvas.create_line(0, y, self.instance.width_x, y)
        if self.state == 'ON':
            for i in self.drops:
                self.canvas.create_line(i[0], i[1], i[2], i[3])
        self.canvas.pack()

    def calculate(self):
        self.state = 'ON'
        self.number = int(self.form_n.get())
        self.length = int(self.form_l.get())
        self.interval = int(self.form_i.get())
        self.instance = BufffonCal(self.length, self.interval)
        self.drops = self.instance.drop(self.number)
        self.count = self.instance.count()
        self.pi = self.instance.pi_cal()
        self.create_widgets()


def test():
    number = int(input('n: '))
    buffon = BufffonCal(1, 2, 1000, 1000)
    buffon.drop(number)
    counts = buffon.count()
    print('pi={}'.format(buffon.pi_cal()))
    print('線と交わった針の数:{} \n投げた回数        :{}'.format(counts, buffon.number))


def main():
    root = tk.Tk()
    root.title('Buffon\'s Needle')
    app = BuffonAPP()
    app.mainloop()


if __name__ == '__main__':
    main()
    # test()


