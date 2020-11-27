import pytest

from GeneticCropGenerator.Gen import Gen, Crop
from GeneticCropGenerator.Plant import Plant
from shapely.geometry import Polygon


class Plant1(Plant):
    name = "Plant1"
    kg_production = 1


class Plant2(Plant):
    name = "Plant2"
    kg_production = 2


class Plant3(Plant):
    name = "Plant3"
    kg_production = 3


class PlantGroundSize1(Plant):
    name = "PlantGroundSize1"
    ground_radius = 1


crop = Crop(
    crop_shape=Crop.square_polygon(0, 25)
)

gen = Gen(crop=crop, n_plants=120, n_population=200, n_gen=50,
          verbose=True)


def test_process_prod():
    plants = [Plant1(0, 0), Plant2(0, 0), Plant2(0, 0)]
    assert gen.process_prod(plants) == {Plant1: 1, Plant2: 4}


def test_eval_production():
    plant1 = Plant1(0, 0)
    plant2 = Plant2(0, 0)

    # Mono plant
    crop.expected_production = {Plant1: 2}
    gen.crop = crop
    assert gen.eval_production([plant1, plant1]) == 1.
    assert gen.eval_production([plant1]) == 0.5
    assert gen.eval_production([plant1, plant1, plant1]) == 0.5

    # Multi plants
    crop.expected_production = {Plant1: 1, Plant2: 4}
    gen.crop = crop
    assert gen.eval_production([plant1, plant2, plant2]) == 1.
    assert gen.eval_production([plant1, plant2]) == 0.75
    assert gen.eval_production([plant1, plant2, plant2, plant2]) == 0.75
    assert gen.eval_production([plant1]) == 0.5

    # Empty desire production
    crop.expected_production = {}
    gen.crop = crop
    assert gen.eval_production([plant1, plant2, plant2]) == 1.


def test_eval_ground_intersect():
    assert gen.eval_ground_intersect([PlantGroundSize1(0, 0), PlantGroundSize1(2, 2)]) == 1.
    assert gen.eval_ground_intersect([PlantGroundSize1(2, 2), PlantGroundSize1(0, 0)]) == 1.
    assert gen.eval_ground_intersect([PlantGroundSize1(0, 0), PlantGroundSize1(0, 0)]) == 0.
    multiPlants = gen.eval_ground_intersect([PlantGroundSize1(0, 0), PlantGroundSize1(1, 1), PlantGroundSize1(20, 20)])
    assert 0.6 < multiPlants < 0.7
    assert gen.eval_ground_intersect([PlantGroundSize1(1, 1)]) == 1.


def test_eval_symbiosis_interset():
    class EffectedPlant(Plant):
        symbiosis_radius = 1

    class NotEffectedPlant(Plant):
        symbiosis_radius = 1

    class PlantEffect10(Plant):
        symbiosis_radius = 10
        symbiosis_list = {EffectedPlant}

    assert gen.eval_symbiosis_interset([PlantEffect10(1, 1), EffectedPlant(2, 2)]) == 1
    assert gen.eval_symbiosis_interset(
        [PlantEffect10(1, 1), EffectedPlant(2, 2), EffectedPlant(2, 2), EffectedPlant(2, 2)]) == 0.5
    assert gen.eval_symbiosis_interset([PlantEffect10(1, 1), NotEffectedPlant(2, 2)]) == 0.


def test_eval_crop_within():
    gen.crop = Crop(crop_shape = Crop.square_polygon(0, 10))

    # 100% out
    assert gen.eval_crop_within([PlantGroundSize1(20, 20)]) == 0
    # 100% in
    assert gen.eval_crop_within([PlantGroundSize1(5, 5)]) == 1
    # 50% in / 50% out
    assert gen.eval_crop_within([PlantGroundSize1(0, 5)]) == 0
    # 1 in and 1 out
    assert gen.eval_crop_within([PlantGroundSize1(5, 5), PlantGroundSize1(20, 20)]) == 0.5


def test_eval_animal_intersect():
    class HelpSize1(Plant):
        ground_radius = 1
        is_help_animal = True

    class NotHelpSize1(Plant):
        ground_radius = 1
        is_help_animal = False

    # Init crop with animal area
    crop = Crop.square_polygon(0, 10)
    crop.animal_shape = Polygon([(2, 2), (8, 2), (8, 8), (2, 8)])
    gen.crop = crop

    # 100% out AND help
    assert gen.eval_animal_intersect([HelpSize1(0, 0)]) == 0
    # 100% in AND help
    assert gen.eval_animal_intersect([HelpSize1(5, 5)]) == 1
    # 100% in AND not help
    assert gen.eval_animal_intersect([NotHelpSize1(5, 5)]) == 0
    # 50% in / 50% out AND help
    assert gen.eval_animal_intersect([HelpSize1(2, 4)]) == 1
    # 1 in AND help + 1 out AND help
    assert gen.eval_animal_intersect([HelpSize1(5, 5), HelpSize1(0, 0)]) == 0.5


@pytest.mark.skip(reason="division disabled for deap")
def test_adjust_weight():
    assert gen.adjust_weight([]) == 1.
    assert gen.adjust_weight([(2, 1)]) == 1.
    assert gen.adjust_weight([(1, 1), (1, 0)]) == 0.5
    assert gen.adjust_weight([(1, 1), (3, 0)]) == 0.25
