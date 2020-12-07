import argparse

from GeneticCropGenerator.Crop import Crop
from GeneticCropGenerator.Gen import Gen

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-cp', '--crop_point', type=float, nargs=2, action='append',
                    help='<Required> Point (x and y) of the crop e.g: -cp 1.0 2.0', required=True)
parser.add_argument('--potato', type=int, help='Number of potato', required=False)
parser.add_argument('--tomato', type=int, help='Number of tomato', required=False)
parser.add_argument('--marigold', type=int, help='Number of marigold', required=False)
parser.add_argument('--oignon', type=int, help='Number of Oignon', required=False)
parser.add_argument('--olive', type=int, help='Number of Olive', required=False)
parser.add_argument('--garlic', type=int, help='Number of Garlic', required=False)
parser.add_argument('--plants', type=int, help='Number of plants', default=2, required=False)
parser.add_argument('--population', type=int, help='Number of population', default=2, required=False)
parser.add_argument('--iter', type=int, help='Number of iteration', default=2, required=False)


def main():
    args = parser.parse_args()
    crop = Crop.from_args(args)
    # print(crop.expected_production)

    gen = Gen(crop=crop,
              n_plants=args.plants,
              n_population=args.population,
              n_gen=args.iter,
              n_hof=1,
              verbose=False)
    gen_plants = gen.run()[0]
    for plant in gen_plants:
        print(plant.csv())


if __name__ == "__main__":
    main()
