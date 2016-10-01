#import native python functionality
from multiprocessing import cpu_count,\
                            Pipe,\
                            Process,\
                            Queue
from Queue import Empty
from time import sleep

#import 3rd party package functionality
from obspy.core import UTCDateTime

#######################
#                     #
#  CLASS DEFINITIONS  #
#                     #
#######################

class MultiThreadProcess(object):
    """
    A class to facilitate multi-threaded processing.

    +--------------+---------------+
    |Public Methods|Private Methods|
    +==============+===============+
    |:meth:`start` |               |
    +--------------+---------------+

    :argument generator inputter: a generator that will yield objects
                                  to process
    :argument function main_processor: a function to process objects on
                                       the input queue and put process
                                       result objects on the output
                                       queue
    :argument function outputter: a function to output the process
                                  result objects
    :keyword dict extra_args: a :class:`dict` to provide initialization
                              arguments and keyword arguments to
                              ``inputter``, ``main_processor`` and
                              ``outputter``
    :keyword dict config_params: a :class:`dict` to provide
                                 configuration parameters
    :raise TypeError: if arguments are of invalid type
    :raise ValueError: if arguments are of invalid type


    +------------------------------------------------------------------+
    |extra_args                                                        |
    +------------------+-----------------------------------------------+
    |Keyword           |Description                                    |
    +==================+===============================================+
    |input_init_args   |a :class:`list` of arguments to be passed      |
    |                  |straight to ``inputter`` generator.            |
    +------------------+-----------------------------------------------+
    |input_init_kwargs |a :class:`dict` of keyword arguments to be     |
    |                  |passed straight to ``inputtter`` generator.    |
    +------------------+-----------------------------------------------+
    |main_init_args    |a :class:`list` of positional arguments to be  |
    |                  |passed straight to ``main_processor`` function,|
    |                  |immediately following object to be processed.  |
    +------------------+-----------------------------------------------+
    |main_init_kwargs  |a :class:`dict` of keyword arguments to be     |
    |                  |passed straight to ``main_processor`` function.|
    +------------------+-----------------------------------------------+
    |output_init_args  |a :class:`list` of positional arguments to be  |
    |                  |passed straight to ``outputter`` function,     |
    |                  |immediately following processed object.        |
    +------------------+-----------------------------------------------+
    |output_init_kwargs|A :class:`dict` of keyword arguments to be     |
    |                  |passed straight to ``outputter`` function.     |
    +------------------+-----------------------------------------------+

    .. automethod:: start

    .. versionadded:: 0.0alpha
    """
    def __init__(self,
                 inputter,
                 main_processor,
                 outputter,
                 extra_args=None,
                 config_params=None):
        # type check the input args, kwargs
        for arg in (inputter, main_processor, outputter):
            if not isfunction(arg):
                raise TypeError
        if extra_args:
            if not isinstance(extra_args, dict):
                raise TypeError
            for key in ('input_init_args',
                        'main_init_args',
                        'output_init_args'):
                if key in extra_args:
                    if not isinstance(extra_args[key], tuple)\
                            and not isinstance(extra_args[key], list):
                        raise TypeError
                else:
                    extra_args[key] = ()
            for key in ('input_init_kwargs',
                        'main_init_kwargs',
                        'output_init_kwargs'):
                if key in extra_args:
                    if not isinstance(extra_args[key], dict):
                        raise TypeError
                else:
                    extra_args[key] = {}
        else:
            extra_args = {}
            for key in ('input_init_args',
                        'main_init_args',
                        'output_init_args'):
                extra_args[key] = ()
            for key in ('input_init_kwargs',
                        'main_init_kwargs',
                        'output_init_kwargs'):
                extra_args[key] = {}
        if config_params:
            if not isinstance(config_params, dict):
                raise TypeError
            if 'n_threads' not in config_params:
                config_params['n_threads'] = cpu_count() / 2
            if 'input_q_max_size' not in config_params:
                config_params['input_q_max_size'] = 100
            if 'output_q_max_size' not in config_params:
                config_params['output_q_max_size'] = 100
        else:
            config_params = {'n_threads': cpu_count(),
                             'input_q_max_size': 100,
                             'output_q_max_size': 100}
        self.extra_args = extra_args
        #initialize the object attributes
        self.config_params = config_params
        #configure IO and processing threads
        self.input_q = Queue(self.config_params['input_q_max_size'])
        self.output_q = Queue(self.config_params['output_q_max_size'])
        self.input_process = _InputProcess(inputter,
                                          self.input_q,
                                          *extra_args['input_init_args'],
                                          **extra_args['input_init_kwargs'])
        self.output_process = _OutputProcess(outputter,
                                            self.output_q,
                                            *extra_args['output_init_args'],
                                            **extra_args['output_init_kwargs'])
        self.main_pool = _MainPool(main_processor, self)

    def start(self):
        """
        Start multi-threaded processing. This method will block until
        processing is complete and all threads have been terminated.
        """
        self.input_process.start()
        self.main_pool.start()
        self.output_process.start()
        self.input_process.join()
        self.main_pool.signal_kill()
        while self.main_pool.is_alive():
            sleep(1)
        self.output_process.signal_kill()
        while self.output_process.is_alive():
            sleep(1)

class _InputProcess(object):
    """
    A wrapper class for the input thread.

    +--------------+-----------------------+
    |Public Methods|Private Methods        |
    +==============+=======================+
    |:meth:`join`  |:meth:`_target_wrapper`|
    +--------------+                       +
    |:meth:`start` |                       |
    +--------------+-----------------------+

    :argument generator target: a generator that yields objects to be
                                processed
    :argument Queue.Queue input_q: a :class:`Queue.Queue` object
                                   to place objects to be processed on
    :argument tuple \*args: a deferenced :class:`tuple` containing
                            positional arguments to be passed directly
                            through to ``target`` input generator
    :argument dict \*\*kwargs: a double dereferenced :class:`dict`
                               containing keyword arguments to be
                               passed directly through to ``target``
                               input generator

    .. automethod:: join

    .. automethod:: start

    .. automethod:: _target_wrapper

    .. versionadded:: 0.0alpha
    """
    def __init__(self, target, input_q, *args, **kwargs):
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.input_q = input_q
        self.process = Process(target=self._target_wrapper)

    def start(self):
        """
        Start input process.
        """
        self.process.start()

    def _target_wrapper(self):
        """
        A wrapper to place objects from ``target`` generator on
        ``input_q``.
        """
        for obj in self.target(*self.args, **self.kwargs):
            self.input_q.put(obj)

    def join(self):
        """
        Force calling function to block until input process is complete.
        """
        self.process.join()

class _OutputProcess(object):
    """
    A wrapper class for the output thread.

    +---------------------+-----------------------+
    |Public Methods       |Private Methods        |
    +=====================+=======================+
    |:meth:`is_alive`     |:meth:`_target_wrapper`|
    +---------------------+                       +
    |:meth:`signal_kill`  |                       |
    +---------------------+                       +
    |:meth:`start`        |                       |
    +---------------------+-----------------------+

    :argument function target: target function to output processed
                               objects
    :argument Queue.Queue input_q: a :class:`Queue.Queue` object
                                   containing processed objects
    :argument tuple \*args: a dereferenced tuple of positional
                            arguments to be passed straight through to
                            ``target`` output function
    :argument dict \*\*kwargs: a double-dereferenced :class:`dict` of
                               keyword arguments to be passed straight
                               through to ``target`` output function

    .. automethod:: is_alive

    .. automethod:: signal_kill

    .. automethod:: start

    .. automethod:: _target_wrapper

    .. versionadded:: 0.0alpha
    """
    def __init__(self, target, output_q, *args, **kwargs):
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.output_q = output_q
        self.process = Process(target=self._target_wrapper)
        self.pconn, self.cconn = Pipe()

    def is_alive(self):
        """
        Return True if output process is still alive, else return False.
        """
        return self.process.is_alive()

    def signal_kill(self):
        """
        Send kill signal to output process. Output process will
        terminate only when the output queue is empty.
        """
        self.pconn.send('KILL')

    def start(self):
        """
        Start output process.
        """
        self.process.start()

    def _target_wrapper(self):
        """
        A wrapper to take processed objects off the output queue and
        pass them to the output function.
        """
        while True:
            try:
                obj = self.output_q.get(timeout=1)
            except Empty:
                if self.cconn.poll() and self.cconn.recv() == 'KILL':
                    return
                continue
            self.target(obj, *self.args, **self.kwargs)

class _MainPool(object):
    """
    A pool of processing threads.

    +-------------------+-----------------------+
    |Public Methods     |Private Methods        |
    +===================+=======================+
    |:meth:`is_alive`   |:meth:`_target_wrapper`|
    +-------------------+-----------------------+
    |:meth:`signal_kill`|                       |
    +-------------------+                       +
    |:meth:`start`      |                       |
    +-------------------+-----------------------+

    :argument function target: target main processing function
    :argument MultiThreadProcess parent: parent
                                         :class:`MultiThreadProcess`

    .. automethod:: is_alive

    .. automethod:: signal_kill

    .. automethod:: start

    .. automethod:: _target_wrapper

    .. versionadded:: 0.0alpha
    """
    def __init__(self, target, parent):
        self.target = target
        self.parent = parent
        self.process_threads = ()
        self.conns = ()
        for thread_id in range(self.parent.config_params['n_threads']):
            pconn, cconn = Pipe()
            self.conns += ({'pconn': pconn, 'cconn': cconn},)
            self.process_threads += (Process(target=self._target_wrapper,
                                             args=(thread_id,)),)

    def is_alive(self):
        """
        Return True if main processing pool is still alive, else return
        False.
        """
        for process in self.process_threads:
            if process.is_alive():
                return True
        return False

    def signal_kill(self):
        """
        Send kill signal to main processing pool. Main processing pool
        will not terminate until input queue is empty.
        """
        for thread_id in range(len(self.conns)):
            self.conns[thread_id]['pconn'].send('KILL')

    def start(self):
        """
        Start input process.
        """
        for i in range(self.parent.config_params['n_threads']):
            self.process_threads[i].start()

    def _target_wrapper(self, thread_id):
        """
        A wrapper to take objects off the input queue, pass them to
        the main processing function and place the resulting processed
        object on the output queue.
        """
        while True:
            try:
                obj = self.parent.input_q.get(timeout=0.1)
            except Empty:
                if self.conns[thread_id]['cconn'].poll() and\
                        self.conns[thread_id]['cconn'].recv() == 'KILL':
                    return
                continue
            self.parent.output_q.put(self.target(obj,
                                                 *self.parent.extra_args['main_init_args'],
                                                 **self.parent.extra_args['main_init_kwargs']))
##########################
#                        #
#  FUNCTION DEFINITIONS  #
#                        #
##########################

isfunction = lambda func: hasattr(func, '__call__')

def validate_time(time):
    if not isinstance(time, UTCDateTime) and\
            not isinstance(time, float) and\
            not isinstance(time, int) and\
            not isinstance(time, str):
        raise TypeError("invalid type: %s" % type(time))
    if not isinstance(time, UTCDateTime):
        if isinstance(time, str):
            time = float(time)
        if isinstance(time, int) and 1000000 <= time <= 9999999:
            time = UTCDateTime(year=time / 1000, julday=time % 1000)
        elif isinstance(time, float) and time == -1.0:
            time = UTCDateTime(year=3000, julday=365, hour=23, minute=59, second=59)
        else:
            time = UTCDateTime(time)
    return time
