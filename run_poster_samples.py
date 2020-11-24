import random

from GeneticCropGenerator.PlotArea import PlotArea
from GeneticCropGenerator.Gen import Crop, Gen
from GeneticCropGenerator.Plant import *
from shapely.geometry import Polygon


def print_prod(plants, desire_prod):
    gen_plants = Gen.process_prod(plants)
    for tplant in gen_plants:
        desprod_val = desire_prod.get(tplant, 0)
        print(f"{tplant.name}: {gen_plants[tplant]}/{desprod_val}")


crop = Crop(
    crop_shape=Polygon([(0, 0), (2, 40), (20, 36), (38, 20), (34, 2)]),
    animal_shape=Polygon([(8, -3), (4, 10), (8, 43), (12, 43), (20, 25), (23, -3)])
)

crop_big = Crop(
    crop_shape=Polygon([(0, 0), (20, 400), (200, 360), (380, 200), (340, 20)]),
    animal_shape=Polygon([(80, -3), (40, 100), (80, 430), (120, 430), (200, 250), (230, -3)])
)

desire_prod = {
    Potato: 25,
    Tomato: 25,
    Olive: 7,
    Oignon: 15,
    Garlic: 15,
}

desire_prod_big = {
    Potato: 100,
    Tomato: 100,
    Olive: 20,
    Oignon: 40,
    Garlic: 40,
}

# gen = Gen(crop=crop_big, desire_production=desire_prod_big, n_plants=300, n_population=10, n_gen=20, verbose=True)
gen = Gen(crop=crop_big, desire_production=desire_prod_big, n_plants=300, n_population=3000, n_gen=25, n_hof=20, verbose=True)

random.seed(62)

hof = gen.run()

for i in range(len(hof)):
    plants = Gen.create_plants(hof[i])
    print_prod(plants, desire_prod)
    path = './img_crops/sample_{:0d}'.format(i)
    print(path)
    # PlotArea(plants, crop, grid=False).show()
    PlotArea(plants, crop, grid=False).savefig(path)
