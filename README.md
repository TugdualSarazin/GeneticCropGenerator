# GeneticCropGenerator

## Anaconda env

### Create anaconda env
````shell script
conda env create -f environment.yml
````

### Update anaconda env
````shell script
conda env update --prefix ./env --file environment.yml  --prune
````

### Update environment file
````shell script
conda env export > environment.yml
````