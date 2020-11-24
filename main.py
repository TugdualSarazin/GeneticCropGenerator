from GeneticCropGenerator.PlotArea import PlotArea
from GeneticCropGenerator.Gen import Crop, Gen
from GeneticCropGenerator.Plant import *
from shapely.geometry import Polygon


def print_prod(plants, desire_prod):
    gen_plants = Gen.process_prod(plants)
    for tplant in gen_plants:
        desprod_val = desire_prod.get(tplant, 0)
        print(f"{tplant.name}: {gen_plants[tplant]}/{desprod_val}")
    # print("Desire production: ", desire_prod)
    # print("Production:        ", Gen.process_prod(plants))


#mplts = geopandas.read_file("./data/plot_selected.shp")
#crop = Crop(crop_shape=mplts['geometry'][0])
crop = Crop(
    crop_shape=Polygon([(0, 0), (2, 40), (20, 36), (38, 20), (34, 2)]),
    animal_shape=Polygon([(8, -3), (4, 10), (8, 43), (12, 43), (20, 25), (23, -3)])
)

desire_prod = {
    Potato: 25,
    Tomato: 25,
    # Marigold: 10,
    Olive: 7,
    Oignon: 15,
    Garlic: 15,
}

gen = Gen(crop=crop, desire_production=desire_prod, n_plants=10, n_population=100, n_gen=2, n_hof=1, verbose=True)
#gen = Gen(crop=crop, desire_production=desire_prod, n_plants=100, n_population=30, n_gen=10, verbose=True)
#gen = Gen(crop=crop, desire_production=desire_prod, n_plants=600, n_population=50, n_gen=20, verbose=True)
#gen = Gen(crop=crop, desire_production=desire_prod, n_plants=100, n_population=200, n_gen=20, verbose=True)


hof = gen.run()

for i in range(len(hof)):
    plants = Plant.plants_from_arr(hof[i])
    PlotArea(plants, crop, grid=False).show()
