from shapely.geometry import Point


class Plant():
    id: int = None
    x: float
    y: float
    name: str = None
    color: str = 'black'
    ground_radius: float = 1
    symbiosis_radius: float = 1
    symbiosis_list: {type} = {}
    kg_production: int = 0
    is_help_animal = False

    ground_shape = None
    symbiosis_shape = None

    def __init__(self, x, y):
        self.x = x
        self.y = y
        point = Point(x, y)
        self.ground_shape = point.buffer(self.ground_radius)
        self.symbiosis_shape = point.buffer(self.symbiosis_radius)

    def plot_ground(self, ax):
        xs, ys = self.ground_shape.exterior.xy
        ax.fill(xs, ys, alpha=0.3, color=self.color)

    def ground_intersect(self, p):
        return self.ground_shape.intersects(p.ground_shape)

    def symbiosis_intersect(self, p):
        if (type(p) in self.symbiosis_list or type(self) in p.symbiosis_list) \
                and self.symbiosis_shape.intersects(p.symbiosis_shape):
            return True
        else:
            return False

    def __str__(self) -> str:
        return f"{self.name}(x={self.x}, y={self.y})"

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def plant_types():
        return [Potato, Tomato, Marigold, Olive, Oignon, Garlic]

    @staticmethod
    def plants_from_arr(indivs: [float]):
        plants = []
        for i in range(0, len(indivs), 3):
            x = indivs[i]
            y = indivs[i + 1]
            id_plant = indivs[i + 2]
            plant = Plant.plant_types()[id_plant](x, y)
            plants.append(plant)
        return plants

class Potato(Plant):
    name = 'Potato'
    color = 'tab:brown'
    ground_radius = 1
    kg_production = 1


class Tomato(Plant):
    name = 'Tomato'
    color = 'tab:red'
    ground_radius = 1
    # kg_production = 3
    kg_production = 1


class Marigold(Plant):
    name = 'Mexican marigold'
    color = 'gold'
    ground_radius = 0.5
    symbiosis_radius = 5
    symbiosis_list = {Tomato}
    kg_production = 1


class Olive(Plant):
    name = 'Olive'
    color = 'tab:olive'
    ground_radius = 4
    # kg_production = 30
    kg_production = 1
    is_help_animal = True


class Oignon(Plant):
    name = 'Oignon'
    color = 'tab:pink'
    ground_radius = 1
    # kg_production = 2
    kg_production = 1


class Garlic(Plant):
    name = 'Garlic'
    color = 'tab:purple'
    ground_radius = 1
    kg_production = 1
