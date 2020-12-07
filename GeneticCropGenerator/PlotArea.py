import matplotlib.pyplot as plt

from GeneticCropGenerator.Crop import Crop
from GeneticCropGenerator.Plant import Plant


class PlotArea:
    MARGIN = 5
    #BACKGROUND_COLOR = '#6a794c'
    GRID = False
    BACKGROUND_COLOR = 'w'
    ax = None
    crop = None
    minx = None
    maxx = None
    miny = None
    maxy = None

    def __init__(self):
        self.ax = plt.gca(aspect='equal')
        self.ax.cla()
        self.ax.set_facecolor(PlotArea.BACKGROUND_COLOR)
        self.ax.grid(PlotArea.GRID)

    def plot_plants(self, plants):
        for plant in plants:
            xs, ys = plant.ground_shape.exterior.xy
            self.ax.fill(xs, ys, alpha=0.4, color=plant.color)

    def plot_crop_boundary(self, crop: Crop):
        self.ax.plot(*crop.crop_shape.exterior.xy, color='black')
        if crop.animal_shape is not None:
            self.ax.fill(*crop.animal_shape.exterior.xy, color='tab:green', alpha=0.1)

    def set_lim(self, crop):
        # Mins
        if self.minx is None or crop.minx < self.minx:
            self.minx = crop.minx
        if self.miny is None or crop.miny < self.miny:
            self.miny = crop.miny

        # Maxs
        if self.maxx is None or crop.maxx > self.maxx:
            self.maxx = crop.maxx
        if self.maxy is None or crop.maxy > self.maxy:
            self.maxy = crop.maxy
        self.ax.set_xlim((self.minx - self.MARGIN, self.maxx + self.MARGIN))
        self.ax.set_ylim((self.miny - self.MARGIN, self.maxy + self.MARGIN))

    def plot_crop(self, crop:Crop, plants: [Plant]):
        self.set_lim(crop)
        self.plot_crop_boundary(crop)
        self.plot_plants(plants)

    def show(self):
        plt.show()

    def savefig(self, path):
        plt.axis('off')
        plt.savefig(path+'.svg')
        plt.savefig(path+'.png', dpi=600, facecolor=self.BACKGROUND_COLOR)
