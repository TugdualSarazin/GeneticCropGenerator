import itertools
import random
import numpy
from deap import algorithms, base, creator, tools

from GeneticCropGenerator.Crop import Crop
from GeneticCropGenerator.Plant import *


class Gen:
    def __init__(self, crop: Crop, n_plants=10, n_population=300, n_gen=100,
                 n_hof=1, verbose=True):
        # Gen params
        self.crop = crop
        self.N_PLANTS = n_plants
        self.N_POPULATION = n_population
        self.N_GEN = n_gen
        self.VERBOSE = verbose
        self.N_HOF = n_hof

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox()

        # Attribute generator
        self.toolbox.register("attr_x", Gen.randx, self)
        self.toolbox.register("attr_y", Gen.randy, self)
        self.toolbox.register("attr_id_plant", Gen.rand_id_plant, self)

        # Structure initializers
        self.toolbox.register("individual", tools.initCycle, creator.Individual,
                              (self.toolbox.attr_x, self.toolbox.attr_y, self.toolbox.attr_id_plant), n=self.N_PLANTS)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        self.toolbox.register("evaluate", Gen.evalOneMax, self)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def randx(self):
        return random.uniform(self.crop.minx, self.crop.maxx)

    def randy(self):
        return random.uniform(self.crop.miny, self.crop.maxy)

    def rand_id_plant(self):
        plant_types = self.crop.expected_production.keys()
        n_plant_types = len(plant_types) - 1
        return random.randint(0, n_plant_types)

    def eval_ground_intersect(self, plants: [Plant]):
        score = 0
        cnt = 0
        for p1, p2 in itertools.combinations(plants, 2):
            cnt += 1
            if not p1.ground_intersect(p2):
                score += 1
        if cnt > 0:
            return score / cnt
        else:
            return 1

    def eval_symbiosis_interset(self, plants: [Plant]):
        score = 0
        cnt = 0
        for p1, p2 in itertools.combinations(plants, 2):
            cnt += 1
            if p1.symbiosis_intersect(p2):
                score += 1
        if cnt > 0:
            return score / cnt
        else:
            return 1

    def eval_crop_within(self, plants: [Plant]):
        score = 0
        nb_plant = len(plants)
        for plant in plants:
            if plant.ground_shape.within(self.crop.crop_shape):
                score += 1
        if nb_plant > 0:
            return score / nb_plant
        else:
            return 1

    def eval_animal_intersect(self, plants: [Plant]):
        score = 0
        nb_plant = len(plants)
        if self.crop.animal_shape is not None:
            for plant in plants:
                if plant.is_help_animal and plant.ground_shape.intersects(self.crop.animal_shape):
                    score += 1
        if nb_plant > 0:
            return score / nb_plant
        else:
            return 1

    @staticmethod
    def process_prod(plants):
        prod = {}
        for plant in plants:
            prod[type(plant)] = prod.get(type(plant), 0) + plant.kg_production
        return prod

    def eval_production(self, plants):
        # Process current production
        prod = Gen.process_prod(plants)

        # Diff with desire production
        score = 0
        for des_name, des_val in self.crop.expected_production.items():
            prod_val = prod.get(des_name, 0)
            score += (des_val - abs(des_val - prod_val)) / des_val

        # Divide by nb desire production to have a result between [0, 1]
        nb_production = len(self.crop.expected_production)
        if nb_production > 0:
            return score / nb_production
        else:
            return 1.

    @staticmethod
    def adjust_weight(weight_score: [(float, float)]):
        sum_score = 0
        sum_weight = 0
        for weight, score in weight_score:
            sum_weight += weight
            sum_score += score * weight

        return sum_score, 1 / sum_weight

    def plants_from_arr(self, indiv: [float]):
        plant_types = list(self.crop.expected_production.keys())
        plants = []
        for i in range(0, len(indiv), 3):
            x = indiv[i]
            y = indiv[i + 1]
            id_plant = indiv[i + 2]
            plant = plant_types[id_plant](x, y)
            plants.append(plant)
        return plants

    def evalOneMax(self, indiv):
        #plant_types = list(self.crop.expected_production.keys())
        #plants = Plant.plants_from_arr(indiv, plant_types)
        plants = self.plants_from_arr(indiv)
        self.plants_from_arr(indiv)
        return Gen.adjust_weight([
            (10, self.eval_crop_within(plants)),
            (10, self.eval_ground_intersect(plants)),
            (4, self.eval_production(plants)),
            (1, self.eval_symbiosis_interset(plants)),
            (1, self.eval_animal_intersect(plants))
        ])

    def run(self):
        pop = self.toolbox.population(n=self.N_POPULATION)
        hof = tools.HallOfFame(self.N_HOF)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)

        pop, log = algorithms.eaSimple(pop, self.toolbox, cxpb=0.5, mutpb=0.2, ngen=self.N_GEN, stats=stats,
                                       halloffame=hof, verbose=self.VERBOSE)
        # pop, log = algorithms.eaSimple(pop, self.toolbox, cxpb=0.2, mutpb=0.1, ngen=self.N_GEN, stats=stats, halloffame=hof, verbose=self.VERBOSE)
        # pop, log = algorithms.eaMuCommaLambda(pop, self.toolbox, mu=10, lambda_=100, cxpb=0.5, mutpb=0.2, ngen=self.N_GEN, stats=stats, halloffame=hof, verbose=self.VERBOSE)
        # pop, log = algorithms.eaMuCommaLambda(pop, self.toolbox, mu=2, lambda_=1, cxpb=0.5, mutpb=0.2, ngen=self.N_GEN, stats=stats, halloffame=hof, verbose=self.VERBOSE)
        # pop, log = algorithms.eaGenerateUpdate(self.toolbox, ngen=self.N_GEN, stats=stats, halloffame=hof, verbose=self.VERBOSE)

        # return pop, log, hof
        return hof
        # return Gen.create_plants(hof[0])
