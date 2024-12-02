Welcome to the MillenniumDB Python Driver documentation!
=========================================================

.. note::

   This project is under active development.

Installation
------------

First install it using pip:

.. code-block:: console

   $ pip install millenniumdb_driver

Usage
-----

Creating a Driver instance:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First you must create a ``Driver`` instance:

.. code-block:: console

   url = 'URL for the MillenniumDB server'
   driver = millenniumdb_driver.driver(url)

When you are done with the driver, you should close it before exiting the application.

.. code-block:: console

   driver.close()

Acquiring a Session:
~~~~~~~~~~~~~~~~~~~~~

For sending queries to the MillenniumDB server, you must acquire a session instance:

.. code-block:: console

   session = driver.session()

Then you can send queries through your session.

.. code-block:: console

   query = 'MATCH (?from)-[:?type]->(?to) RETURN * LIMIT 10'
   result = session.run(query)

Consuming results:
~~~~~~~~~~~~~~~~~~~~~

The alternatives for consuming results must never be mixed because it would generate undefined behavior on your client and/or server. It is important to mention that the session must be closed when your operations are done.

.. code-block:: console

   result.variables() -> Tuple[str]

Returns the list of variables in the result.

.. code-block:: console
   
      result.records() -> List[Record]

Returns the list of records in the result.

.. code-block:: console
   
      result.values() -> List[object]

Returns the list of values in the result.

.. code-block:: console
      
         result.data() -> List[Dict[str, object]]

Returns the list of records in the result as dictionaries.

.. code-block:: console
   
            result.to_df() -> DataFrame

Returns the result as a pandas DataFrame.

.. code-block:: console
   
                  result.summary() -> object

Returns the summary of the result.

.. code-block:: console
      
      for record in result:
      
Iterates over each record in result.


Catalog Module
===============================
.. automodule:: millenniumdb_driver.catalog
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__,                     __repr__,                     __iter__

Chunk Decoder Module
===============================
.. automodule:: millenniumdb_driver.chunk_decoder
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__,                     __repr__,                     __iter__

Driver Module
===============================
.. automodule:: millenniumdb_driver.driver
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__,                     __repr__,                     __iter__

Graph Objects Module
===============================
.. automodule:: millenniumdb_driver.graph_objects
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__,                     __repr__,                     __iter__

Iobuffer Module
===============================
.. automodule:: millenniumdb_driver.iobuffer
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__,                     __repr__,                     __iter__

Message Decoder Module
===============================
.. automodule:: millenniumdb_driver.message_decoder
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__,                     __repr__,                     __iter__

Message Receiver Module
===============================
.. automodule:: millenniumdb_driver.message_receiver
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__,                     __repr__,                     __iter__

Millenniumdb Error Module
===============================
.. automodule:: millenniumdb_driver.millenniumdb_error
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__,                     __repr__,                     __iter__

Protocol Module
===============================
.. automodule:: millenniumdb_driver.protocol
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__,                     __repr__,                     __iter__

Record Module
===============================
.. automodule:: millenniumdb_driver.record
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__,                     __repr__,                     __iter__

Request Builder Module
===============================
.. automodule:: millenniumdb_driver.request_builder
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__,                     __repr__,                     __iter__

Response Handler Module
===============================
.. automodule:: millenniumdb_driver.response_handler
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__,                     __repr__,                     __iter__

Result Module
===============================
.. automodule:: millenniumdb_driver.result
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__,                     __repr__,                     __iter__

Session Module
===============================
.. automodule:: millenniumdb_driver.session
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__,                     __repr__,                     __iter__

Socket Connection Module
===============================
.. automodule:: millenniumdb_driver.socket_connection
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__,                     __repr__,                     __iter__
