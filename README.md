# Gridworks Marketmaker

## QuickStart

1. Clone this repo

2. Using python 3.10.\* or greater, create virtual env inside this repo

   ```
   python -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

3. Install [docker](https://docs.docker.com/get-docker/)

4. Start docker containers

- **X86 CPU**:

  ```
  docker compose -f docker-x86.yml up -d
  ```

- **arm CPU**:

  ```
  docker compose -f docker-arm.yml up -d
  ```

5. Start the API for the MarketMaker

```
uvicorn gwmm.rest_api:app --host localhost --port 7997 --workers 5
```

    - http://localhost:7997/ shows market maker information
    - http://localhost:7997/get-time/ shows the current time of the simulation

6. Run the rabbit-half of the MarketMaker:

```
python demo.py
```

NOTE: This requires a TimeCoordinator and at least one AtomicTNode in order
for time to move forward.

## Requirements

- TODO

## Installation

You can install _Gridworks Marketmaker_ via [pip] from [PyPI]:

```console
$ pip install gwmm
```

## Usage

Please see the [Command-line Reference] for details.

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
