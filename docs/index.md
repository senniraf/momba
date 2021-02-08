Welcome to Momba's documentation!
=================================

[![PyPi Package](https://img.shields.io/pypi/v/momba.svg?label=latest%20version)](https://pypi.python.org/pypi/momba)
[![Basic Checks](https://img.shields.io/github/workflow/status/koehlma/momba/Basic%20Checks?label=basic%20checks)](https://github.com/koehlma/momba/actions)
[![Tests](https://img.shields.io/github/workflow/status/koehlma/momba/Run%20Tests?label=tests)](https://github.com/koehlma/momba/actions)
[![Docs](https://img.shields.io/static/v1?label=docs&message=master&color=blue)](https://koehlma.github.io/momba/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Gitter](https://badges.gitter.im/koehlma/momba.svg)](https://gitter.im/koehlma/momba?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

*Momba* is a Python framework for dealing with quantitative models centered around the [JANI-model](http://www.jani-spec.org/) interchange format.
Momba strives to deliver an integrated and intuitive experience to aid the process of model construction, validation, and analysis.
It provides convenience functions for the modular construction of models effectively turning Python into a syntax-aware macro language for quantitative models.
Momba's built-in simulation engine allows gaining confidence in a model, for instance, by rapidly prototyping a tool for interactive model exploration and visualization, or by connecting it to a testing framework.
Finally, thanks to the JANI-model interchange format, several state-of-the-art model checkers and other tools are readily available for model analysis.


## Features

* first-class **import and export** of **JANI models**
* **syntax-aware macros** for the modular construction of models with Python code
* **built-in simulation engine** for PTAs, MDPs and other model types
* interfaces to state-of-the-art model checkers, e.g., [The Modest Toolset](http://www.modestchecker.net/) and [Storm](https://www.stormchecker.org/)
* pythonic and **statically typed** APIs to thinker with formal models


## Getting Started

Momba is available from the [Python Package Index](https://pypi.org/):
```sh
pip install momba[all]
```
Installing Momba with the `all` feature flag will install all optional dependencies unleashing the full power and all features of Momba.
Check out the [examples](examples) or read the [user guide](guide) to learn more.


## Contents

```{toctree}
:maxdepth: 2

guide/index
examples/index
reference/index
contributing/index
```