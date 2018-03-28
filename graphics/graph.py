import random

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

class Graph :
    def __init__(self, width, height, style, label_text) :
        self.width = width
        self.height = height
        self.style = style
        self.labels = label_text.split(' ')
        random.shuffle(self.labels)
        self.num_points = random.randint(min(3, len(self.labels)),max(7,len(self.labels)))
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
                    
    def generate_bar_graph(self) :
        ax = self.fig.add_subplot(111)
        ax.bar(self.__get_x_data(), self.__get_y_data(), color = self.__get_color()) 
        
    def generate_line_graph(self) :
        ax = self.fig.add_subplot(111)
        ax.plot(self.__get_x_data(), self.__get_y_data(), color = self.__get_color())    
        
    def generate_pie(self) :
        ax = self.fig.add_subplot(111)    
        ax.pie(self.__get_y_data(), labels=self.__get_x_data())
        ax.axis('equal')

    def debug_save(self, filename) :
        # figure.savefig("software.svg", bbox_inches="tight", transparent=True)
        self.canvas.print_png(filename)
        
    def __get_x_data(self) :
        return self.labels[:self.num_points]
    
    def __get_y_data(self) :
        return [random.randint(1,10) for _ in range(self.num_points)]
    
    def __get_color(self) :
        return random.choice(['red','green','blue'])
    
    
