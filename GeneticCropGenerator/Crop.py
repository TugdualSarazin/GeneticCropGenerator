from shapely.geometry import Polygon

from GeneticCropGenerator.Plant import Potato, Tomato, Olive, Oignon, Garlic, Marigold


class Crop:
    crop_shape = None
    minx: float
    maxx: float
    miny: float
    maxy: float
    animal_shape = None

    def __init__(self, crop_shape: Polygon, expected_production, animal_shape: Polygon = None):
        self.crop_shape = crop_shape
        self.animal_shape = animal_shape
        self.expected_production = expected_production
        self.minx, self.miny, self.maxx, self.maxy = self.crop_shape.bounds

    def __str__(self):
        return f'Crop(crop_shape={self.crop_shape}, expected_production={self.expected_production}, animal_shape={self.animal_shape})'

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def from_args(args):
        crop_shape = Polygon(args.crop_point)

        expected_prod = {}
        if args.potato and args.potato > 0:
            expected_prod[Potato] = args.potato

        if args.tomato and args.tomato > 0:
            expected_prod[Tomato] = args.tomato

        if args.marigold and args.marigold > 0:
            expected_prod[Marigold] = args.marigold

        if args.oignon and args.oignon > 0:
            expected_prod[Oignon] = args.oignon

        if args.olive and args.olive > 0:
            expected_prod[Olive] = args.olive
            
        if args.garlic and args.garlic > 0:
            expected_prod[Garlic] = args.garlic
        #     Potato: args.potato,
        #     Tomato: args.tomato,
        #     Marigold: args.marigold,
        #     Oignon: args.oignon,
        #     Olive: args.olive,
        #     Garlic: args.garlic,
        return Crop(crop_shape, expected_prod)

    @staticmethod
    def square_polygon(min, max):
        return Polygon([(min, min), (min, max), (max, max), (max, min)])
