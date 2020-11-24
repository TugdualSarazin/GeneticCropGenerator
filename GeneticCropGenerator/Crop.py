from shapely.geometry import Polygon


class Crop:
    crop_shape = None
    minx: float
    maxx: float
    miny: float
    maxy: float
    animal_shape = None

    def __init__(self, crop_shape: Polygon, animal_shape: Polygon = None):
        self.crop_shape = crop_shape
        self.animal_shape = animal_shape
        self.minx, self.miny, self.maxx, self.maxy = self.crop_shape.bounds

    @staticmethod
    def square(min, max):
        return Crop(
            crop_shape=Polygon([(min, min), (min, max), (max, max), (max, min)]),
            animal_shape=None
        )
