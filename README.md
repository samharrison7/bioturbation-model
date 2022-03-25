# Bioturbation Model

[![fair-software.eu](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B-yellow)](https://fair-software.eu) [![PyPI version](https://badge.fury.io/py/bioturbation.svg)](https://badge.fury.io/py/bioturbation)

A simple model of earthworm bioturbation, using a layered soil profile. The model predicts the mixing of mass pools (e.g. of contaminants) over time as a function of earthworm density.

## Quickstart

The model can be installed using `pip`:

```bash
$ pip install bioturbation
```

Alternatively, you can download the source code and use the provided Conda environment file to install the relevant dependencies:

```bash
$ git clone https://github.com/samharrison7/bioturbation-model.git
$ cd bioturbation-model
$ conda env create -f environment.yml
```

## Usage

Check out the [examples](./examples/) directory for examples of how to use the model.

## Conceptualisation

See the [conceptualisation](./examples/conceptualisation.ipynb) notebook for a mathematical description of how the model works.

## Limitations

No guarantee is given as the to scientific validity of this model for your data. The onus is on the user to verify this validity. Indeed, there are a number of limitations to the model as it stands which might limit its applicability:
* Transport is only between *adjacent* soil layers, therefore neglecting preferential flow pathways, e.g. representing deep burrowing earthworms transporting tracers directly from upper to lower layers.
* No change in soil properties due to bioturbation is modelled. That is, there is an implicit assumption that the amount of soil mixed between layers is negligible. This assumption might not always be valid.

We welcome requests for collaboration if you are interested in exploring the validity of the model for your own research. Please [get in touch](mailto:sharrison@ceh.ac.uk).