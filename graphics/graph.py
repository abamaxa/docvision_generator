import random

import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from PIL import Image

class Graph :
    def __init__(self, width, height, label_text) :
        self.labels = label_text.split(' ')
        random.shuffle(self.labels)
        self.num_points = random.randint(min(3, len(self.labels)),max(7,len(self.labels)))
        dpi = 100
        self.fig = Figure((width // dpi, height // dpi), dpi = dpi)
        self.canvas = FigureCanvas(self.fig)
                    
    def generate_bar(self) :
        ax = self.fig.add_subplot(111)
        ax.bar(self.__get_x_data(), self.__get_y_data(), color = self.__get_color()) 
        
    def generate_line(self) :
        ax = self.fig.add_subplot(111)
        ax.plot(self.__get_x_data(), self.__get_y_data(), color = self.__get_color())    
        
    def generate_pie(self) :
        ax = self.fig.add_subplot(111)    
        ax.pie(self.__get_y_data(), labels=self.__get_x_data())
        ax.axis('equal')

    def debug_save(self, filename) :
        # figure.savefig("software.svg", bbox_inches="tight", transparent=True)
        self.canvas.print_png(filename)
        
    def get_image(self) :
        self.canvas.draw()
        fig = self.canvas.figure
        size = (int(fig.get_figwidth() * fig.get_dpi()),
                int(fig.get_figheight() * fig.get_dpi()))
        
        return Image.frombytes("RGBA", size, self.canvas.buffer_rgba())
    
    def __get_x_data(self) :
        return self.labels[:self.num_points]
    
    def __get_y_data(self) :
        return [random.randint(1,10) for _ in range(self.num_points)]
    
    def __get_color(self) :
        return random.choice(['red','green','blue'])
    
    
