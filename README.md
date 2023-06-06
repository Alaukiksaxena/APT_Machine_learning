# CompositionSpace

CompositionSpace is a python library for analysis of APT data.

## Installation

### Installation using pip

Compositionspace can be installed using:

```
pip install compositionspace
```

### Installation using [Conda](https://anaconda.org/)

It is **strongly** recommended to install and use `calphy` within a conda environment. To see how you can install conda see [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/).

Once a conda distribution is available, the following steps will help set up an environment to use `compositionspace`. First step is to clone the repository.

```
git clone https://github.com/eisenforschung/CompositionSpace.git
```

After cloning, an environment can be created from the included file-

```
cd CompositionSpace
conda env create -f environment.yml
```

Activate the environment,

```
conda activate compspace
```

then, install `compositionspace` using,

```
python setup.py install
```
The environment is now set up to run calphy.

## Examples

For an example of the complete workflow using `compositionspace`, see `example/full_workflow.ipynb`.

The provided dataset is a small one for testing purposes, which is also accessible here:

Ceguerra, AV (2021) Supplementary material: APT test cases.
Available at http://dx.doi.org/10.25833/3ge0-y420

## Documentation

Documentation is available [here](https://compositionspace.readthedocs.io/en/latest/).