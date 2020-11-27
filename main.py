import geopandas

from GeneticCropGenerator.PlotArea import PlotArea
from GeneticCropGenerator.Gen import Crop, Gen
from GeneticCropGenerator.Plant import *


def print_prod(plants, desire_prod):
    gen_plants = Gen.process_prod(plants)
    for tplant in gen_plants:
        desprod_val = desire_prod.get(tplant, 0)
        print(f"{tplant.name}: {gen_plants[tplant]}/{desprod_val}")
    # print("Desire production: ", desire_prod)
    # print("Production:        ", Gen.process_prod(plants))


mplts = geopandas.read_file("./data/san_vincenc_site_division.shp")

expected_prods = [
    {Tomato: 85, Marigold: 15},
    {Olive: 40, Garlic: 60},
    {Olive: 30, Oignon: 70},
    {Olive: 10, Potato: 80, Oignon: 10},
]

crops = []
id_exp = 0
for mplt in mplts['geometry']:
    if mplt is not None:
        crops.append(Crop(
            crop_shape=mplt,
            expected_production={Olive: 3, Garlic: 5}
        ))

    if id_exp == len(expected_prods) - 1:
        id_exp = 0
    else:
        id_exp += 1

expected_prod = {
    Potato: 25,
    Tomato: 25,
    # Marigold: 10,
    Olive: 7,
    Oignon: 15,
    Garlic: 15,
}




crop1 = Crop(
    crop_shape=Crop.square_polygon(0, 10),
    expected_production={Tomato: 1, Marigold: 2}
    # crop_shape=Polygon([(0, 0), (2, 40), (20, 36), (38, 20), (34, 2)]),
    # animal_shape=Polygon([(8, -3), (4, 10), (8, 43), (12, 43), (20, 25), (23, -3)])
)

crop2 = Crop(
    crop_shape=Crop.square_polygon(10, 20),
    expected_production={Olive: 3, Garlic: 5}
    # crop_shape=Polygon([(0, 0), (2, 40), (20, 36), (38, 20), (34, 2)]),
    # animal_shape=Polygon([(8, -3), (4, 10), (8, 43), (12, 43), (20, 25), (23, -3)])
)

#gen = Gen(crop=None, n_plants=10, n_population=10, n_gen=2, n_hof=1, verbose=True)
gen = Gen(crop=None, n_plants=100, n_population=300, n_gen=5, n_hof=1, verbose=True)


plot = PlotArea()

#for crp in [crop1, crop2]:
for crp in crops:
    gen.crop = crp
    hof = gen.run()
    plants = gen.plants_from_arr(hof[0])

    plot.plot_crop(crp, plants)

# plot.show()
plot.savefig("img/san_vincenc_gen_crop")
