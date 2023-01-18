GridWorks MarketMaker
=======================


This is the  Python SDK for building
`MarketMakers <https://gridworks.readthedocs.io/en/latest/market-maker.html>`_ for GridWorks. GridWorks uses distributed 
actors to balance the electric grid, and MarketMakers are the actors brokering this grid balancing via the markets
they run for energy and balancing services.

This SDK is available as the `gridworks-marketmaker <https://pypi.org/project/gridworks-marketmaker/>`_ pypi package. Documentation
specific to using this SDK is available `here <https://gridworks-marketmaker.readthedocs.io/>`_. If this is your first time
with GridWorks code, please start with the `main GridWorks docs <https://gridworks.readthedocs.io/>`_.

MarketMakers support grid balancing by running markets. They are geared to serve millions of coordinated and intelligent
`Transactive Devices <https://gridworks.readthedocs.io/en/latest/transactive-device.html>`_, represented in their
markets by `AtomicTNodes <https://gridworks.readthedocs.io/en/latest/atomic-t-node.html>`_. The veracity of the
ex-poste energy and power data provided by AtomicTNodes to the MarketMaker is backed up via a series of GridWorks Certificates
globally visible on the Algorand blockchain.  These include the foundational
`TaDeeds <https://gridworks.readthedocs.io/en/latest/ta-deed.html>`_ that establish ownership of the underlying
Transactive Device, and the  `TaTradingRights <https://gridworks.readthedocs.io/en/latest/ta-trading-rights.html>`_ that
give the AtomicTNode authority to represent the Transactive Device in its MarketMaker's markets.


Installation
^^^^^^^^^^^^

.. note::
    gridworks-marketmaker requires python 3.10 or higher.


.. code-block:: console

    (venv)$ pip install gridworks-marketmaker


.. toctree::
    :hidden:
    :maxdepth: 2
    :caption: Code Support

    Hello MarketMaker <hello-marketmaker>
    Lexicon <https://gridworks.readthedocs.io/en/latest/lexicon.html>


.. toctree::
    :hidden:
    :maxdepth: 2
    :caption: API docs

    Type APIs <apis/types>

.. toctree::
    :hidden:
    :maxdepth: 2
    :caption: SDK docs

    DataClasses <data-classes>
    Enums <enums>
    Types <sdk-types>
    MarketMakerApi <market-maker-api>
    MarketMakerBase <market-maker-base>

.. toctree::
    :hidden:
    :maxdepth: 2
    :caption: Participate

    Contributing <contributing>
    Code of Conduct <code-of-conduct>
    License <license>
