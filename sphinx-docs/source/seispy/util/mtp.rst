:mod:`seispy.util.mtp` -- Multi-Threaded Processing
===================================================
.. module:: seispy.util.mtp

This module offers a single public class :class:`MultiThreadProcess` to
facilitate multi-threaded processing. Private classes are documented here for
development purposes as well.

Contents
--------

+---------------------------+-----------------------+
|`Public Classes`_          |`Private Classes`_     |
+===========================+=======================+
|:class:`MultiThreadProcess`|:class:`_InputProcess` |
+---------------------------+-----------------------+
|                           |:class:`_OutputProcess`|
+---------------------------+-----------------------+
|                           |:class:`_MainPool`     |
+---------------------------+-----------------------+


Simple Example
--------------
A simple example to print the square of a sequence of integers.

.. code-block:: python

   >>> from seispy.util.mtp import MultiThreadProcess
   >>> from time import sleep
   >>> def input_thread():
   ...     for x in range(100):
   ...         yield x
   ...
   >>> def process_thread(x):
   ...     sleep(0.5)
   ...     return x ** 2
   ...
   >>> def output_thread(x):
   ...     print x
   ...
   >>> mtp = MultiThreadProcess(input_thread,
   ...                          process_thread,
   ...                          output_thread)
   >>> mtp.start()
   0
   1
   9
   4
   16
   25
   49
   36
   64 81
   100
   121

Intermediate Example
--------------------
   >>> from seispy.util.mtp import MultiThreadProcess
   >>> from time import sleep
   >>> def input_thread(start=0, stop=100, step=1):
   ...     for x in range(start, stop, step):
   ...         yield x
   ...
   >>> def process_thread(x, y, exponent=1, sleep_length=0.5):
   ...     sleep(sleep_length)
   ...     return (x + y) ** exponent
   ...
   >>> def output_thread(x):
   ...     print x
   ...
   >>> config_params = {'n_threads': 4}
   >>> extra_args = {'input_init_kwargs': {'start': -100,
   ...                                     'stop': 100,
   ...                                     'step': 5},
   ...               'main_init_args': (15,),
   ...               'main_init_kwargs': {'exponent': 2}
   ...              }
   >>> mtp = MultiThreadProcess(input_thread,
   ...                          process_thread,
   ...                          output_thread)
   ...                          config_params=config_params,
   ...                          extra_args=extra_args)
   >>> mtp.start()

Advanced Example
----------------
.. todo::
   This will be an example of multi-threaded database processing.

Public Classes
--------------

.. autoclass:: MultiThreadProcess

Private Classes
---------------

.. autoclass:: _InputProcess

.. autoclass:: _OutputProcess

.. autoclass:: _MainPool
