import matplotlib.pyplot as plt

from GeneticCropGenerator.Crop import Crop
from GeneticCropGenerator.Plant import Plant


class PlotArea:
    ax = None
    crop = None
    plants: [Plant] = []
    MARGIN = 2

    def __init__(self, plants: [], crop=Crop.square(0, 20), grid=True):
        self.plants = plants
        self.crop = crop

        self.ax = plt.gca(aspect='equal')
        self.ax.cla()
        self.ax.set_xlim((self.crop.minx - self.MARGIN, self.crop.maxx + self.MARGIN))
        self.ax.set_ylim((self.crop.miny - self.MARGIN, self.crop.maxy + self.MARGIN))
        self.ax.grid(grid)

    def plot_plants(self):
        for plant in self.plants:
            xs, ys = plant.ground_shape.exterior.xy
            self.ax.fill(xs, ys, alpha=0.4, color=plant.color)

    def plot_crop(self):
        self.ax.plot(*self.crop.crop_shape.exterior.xy, color='black')
        if self.crop.animal_shape is not None:
            self.ax.fill(*self.crop.animal_shape.exterior.xy, color='tab:green', alpha=0.1)

    def show(self):
        self.plot_crop()
        self.plot_plants()
        plt.show()

    def savefig(self, path):
        self.plot_crop()
        self.plot_plants()
        plt.axis('off')
        plt.savefig(path+'.svg')
        plt.savefig(path+'.png')
