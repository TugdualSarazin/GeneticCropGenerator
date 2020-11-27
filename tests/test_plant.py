from GeneticCropGenerator.Plant import Plant, Potato, Tomato, Olive


class PlantSize10(Plant):
    ground_radius = 10


class PlantSize1(Plant):
    ground_radius = 1


class SymbiodedPlant(Plant):
    symbiosis_radius = 1


class NotSymbiodedPlant(Plant):
    symbiosis_radius = 1


class PlantSymbiosis10(Plant):
    symbiosis_radius = 1
    symbiosis_list = {SymbiodedPlant}


def test_ground_intersect():
    plant10 = PlantSize10(0, 0)

    assert plant10.ground_intersect(PlantSize1(0, 0))
    assert plant10.ground_intersect(PlantSize1(10.9, 0))
    assert not plant10.ground_intersect(PlantSize1(11, 0))


def test_symbiosis_intersect():
    plant = PlantSymbiosis10(0, 0)

    # Test symbiosis distance
    assert plant.symbiosis_intersect(SymbiodedPlant(0, 0))
    assert plant.symbiosis_intersect(SymbiodedPlant(1.9, 0))
    assert not plant.symbiosis_intersect(SymbiodedPlant(2, 0))

    # Test symbiosis 2 ways
    assert SymbiodedPlant(0, 0).symbiosis_intersect(plant)

    # Test no symbiosis
    assert not plant.symbiosis_intersect(NotSymbiodedPlant(0, 0))


def test_plants_from_arr():
    plants_arr = [1.1, 1.2, 0, 2.1, 2.2, 1]
    plants = Plant.plants_from_arr(plants_arr, [Potato, Tomato, Olive])

    assert len(plants) == 2
    plt0 = plants[0]
    assert type(plt0) == Potato
    assert plt0.x == 1.1
    assert plt0.y == 1.2
    plt1 = plants[1]
    assert type(plt1) == Tomato
    assert plt1.x == 2.1
    assert plt1.y == 2.2
