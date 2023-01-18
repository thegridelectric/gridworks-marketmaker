# Gridworks Marketmaker

This is the Python SDK for building 
[MarketMakers](https://gridworks.readthedocs.io/en/latest/market-maker.html) for GridWorks.   GridWorks uses distributed actors to balance the electric grid, and MarketMakers are the actors brokering this grid balancing via the markets they run for energy and balancing services.

This SDK is available as the [gridworks-marketmaker](https://pypi.org/project/gridworks-marketmaker/) pypi package. Documentation
specific to using this SDK is available [here](https://gridworks-marketmaker.readthedocs.io/). If this is your first time
with GridWorks code, please start with the [main GridWorks doc](https://gridworks.readthedocs.io/).



MarketMakers support grid balancing by running markets. They are geared to serve millions of coordinated and intelligent
[Transactive Devices](https://gridworks.readthedocs.io/en/latest/transactive-device.html), represented in their
markets by  [AtomicTNodes](https://gridworks.readthedocs.io/en/latest/atomic-t-node.html). The veracity of the
ex-poste energy and power data provided by AtomicTNodes to the MarketMaker is backed up via a series of GridWorks Certificates
globally visible on the Algorand blockchain.  These include the foundational
[TaDeeds](https://gridworks.readthedocs.io/en/latest/ta-deed.html) that establish ownership of the underlying
Transactive Device, and the [TaTradingrights](https://gridworks.readthedocs.io/en/latest/ta-trading-rights.html) that
give the AtomicTNode authority to represent the Transactive Device in its MarketMaker's markets.


## Millinocket MarketMaker directions

These are directions for running this code as the MarketMaker in the [Millinocket tutorial](https://gridworks.readthedocs.io/en/latest/millinocket-tutorial.html).  These directions assume you have **already started docker sandbox and the GridWorks dev rabbit broker**, as described in the [Demo prep](https://gridworks.readthedocs.io/en/latest/millinocket-tutorial.html#demo-prep).

1. Clone this repo

2. Using python 3.10.\* or greater, create virtual env inside this repo

   ```
   python -m venv venv
   source venv/bin/activate
   pip install -e .
   ```
3.Run the FastAPI half of the MarketMaker:

```
uvicorn gwmm.rest_api:app --host localhost --port 7997 --workers 5
```

    - http://localhost:7997/ shows market maker information
    - http://localhost:7997/get-time/ shows the current time of the simulation

4. Run the rabbit half of the MarketMaker:

```
python demo.py
```

NOTE: This requires a TimeCoordinator and at least one AtomicTNode in order
for time to move forward. 


## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Gridworks Marketmaker_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

[![PyPI](https://img.shields.io/pypi/v/gridworks-marketmaker.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/gridworks-marketmaker.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/gridworks-marketmaker)][python version]
[![License](https://img.shields.io/pypi/l/gridworks-marketmaker)][license]

[![Read the documentation at https://gridworks-marketmaker.readthedocs.io/](https://img.shields.io/readthedocs/gridworks-marketmaker/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/thegridelectric/gridworks-marketmaker/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/thegridelectric/gridworks-marketmaker/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/gridworks-marketmaker/
[status]: https://pypi.org/project/gridworks-marketmaker/
[python version]: https://pypi.org/project/gridworks-marketmaker
[read the docs]: https://gridworks-marketmaker.readthedocs.io/
[tests]: https://github.com/thegridelectric/gridworks-marketmaker/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/thegridelectric/gridworks-marketmaker
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/thegridelectric/gridworks-marketmaker/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/thegridelectric/gridworks-marketmaker/blob/main/LICENSE
[contributor guide]: https://github.com/thegridelectric/gridworks-marketmaker/blob/main/CONTRIBUTING.md
[command-line reference]: https://gridworks-marketmaker.readthedocs.io/en/latest/usage.html
