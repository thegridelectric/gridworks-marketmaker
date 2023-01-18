GridWorks MarketMaker
=======================


This is the ` GridWorks <https://gridworks.readthedocs.io/>`_ Python SDK for building 
`MarketMaker Actors <https://gridworks.readthedocs.io/en/latest/market-maker.html>`_. They run markets for the electric
grid (energy and other) in GridWorks. They are geared to serve millions of coordinated and intelligent 
`Transactive Devices <https://gridworks.readthedocs.io/en/latest/transactive-device.html>`_, represented in their
markets by `AtomicTNodes <https://gridworks.readthedocs.io/en/latest/atomic-t-node.html>`_. The veracity of the
ex-poste energy and power data provided by AtomicTNodes to the MarketMaker is backed up via a series of GridWorks Certificates 
globally visible on the Algorand blockchain.  These include the foundational 
`TaDeeds <https://gridworks.readthedocs.io/en/latest/ta-deed.html>`_ that establish ownership of the underlying
transactive device, and Scada Certificate establishing the credentials of the code running locally on or attached to
the transcactive device, and the  [ta-trading-rights](https://gridworks.readthedocs.io/en/latest/ta-trading-rights.html) that
give the AtomicTNode authority to represent the Transactive Device in markets. 

To explore the rest of GridWorks, visit the `GridWorks docs <https://gridworks.readthedocs.io/en/latest/>`_.



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

.. toctree::
    :hidden:
    :maxdepth: 2
    :caption: Participate

    Contributing <contributing>
    Code of Conduct <codeofconduct>
    License <license>
