from multiprocessing import Pool, Process, Queue
from Queue import Empty

class MultiThreadedProcessor:
    """
    This is a class to facilitate multithreaded processing.
    """
    def __init__(self, *args, **kwargs):
        """
        Positional Arguments:
        inputter - <function>
        main processor - <function>
        outputter - <function>

        Keyword Arguments:
        inp_args - <tuple>/<list>
        inp_kwargs - <dict>
        main_args - <tuple>/<list>
        main_kwargs - <dict>
        out_args - <tuple>/<list>
        out_kwargs - <dict>
        nthreads - <int>
        input_q_max_size - <int>
        output_q_max_size - <int>
        """

        for f in args[:3]:
            if not isfunction(f):
                raise MultiThreadedProcessorError()
        self.inp = args[0]
        self.main = args[1]
        self.out = args[2]
        self._terminate = False
        self.input_q_max_size = 10
        self.output_q_max_size = 10
        for var in ['input_q_max_size', 'output_q_max_size']:
            if var in kwargs:
                if not isinstance(kwargs[var], int):
                    raise MultiThreadedProcessorError("Keyword argument "\
                            "'%s' must be of type <int>, got %s."\
                            % (var, type(kwargs[var])))
                else:
                    exec("self.%s = kwargs['%s']" % (var, var))
        self.nthreads = 2
        if 'nthreads' in kwargs:
            self.nthreads = kwargs['nthreads']
        self._config_inp_proc(args, kwargs)
        self._config_out_proc(args, kwargs)
        self._config_main_pool(args, kwargs)

    def _config_inp_proc(self, *args, **kwargs):
        self._inp_q = Queue(self.input_q_max_size)
        if 'inp_args' in kwargs:
            inp_args = kwargs['inp_args']
        else:
            inp_args = None
        if 'inp_kwargs' in kwargs:
            inp_kwargs = kwargs['inp_kwargs']
        else:
            inp_kwargs = None
        if inp_args == None and inp_kwargs == None:
            self._inp_proc = Process(target=self.inp, args=(self._inp_q,))
        elif inp_args == None:
            self._inp_proc = Process(target=self.inp, args=(self._inp_q,
                                                            inp_kwargs))
        elif inp_kwargs == None:
            self._inp_proc = Process(target=self.inp, args=(self._inp_q,
                                                            inp_kwargs))
        else:
            self._inp_proc = Process(target=self.inp, args=(self._inp_q,
                                                            inp_args,
                                                            inp_kwargs))

    def _config_main_pool(self, *args, **kwargs):
        if 'main_args' in kwargs:
            self.main_args = kwargs['main_args']
        else:
            self.main_args = None
        if 'main_kwargs' in kwargs:
            self.main_kwargs = kwargs['main_kwargs']
        else:
            self.main_kwargs = {}
        self.main_kwargs['input_queue'] = self._inp_q
        self.main_pool = Pool(processes=self.nthreads)

    def _config_out_proc(self, *args, **kwargs):
        self._out_q = Queue(self.output_q_max_size)
        if 'out_args' in kwargs:
            out_args = kwargs['out_args']
        else:
            out_args = None
        if 'out_kwargs' in kwargs:
            out_kwargs = kwargs['out_kwargs']
        else:
            out_kwargs = None
        if out_args == None and out_kwargs == None:
            self._out_proc = Process(target=self.out, args=(self._out_q,))
        elif out_args == None:
            self._out_proc = Process(target=self.out, args=(self._out_q,
                                                            out_kwargs))
        elif out_kwargs == None:
            self._out_proc = Process(target=self.out, args=(self._out_q,
                                                            out_kwargs))
        else:
            self._out_proc = Process(target=self.out, args=(self._out_q,
                                                            out_args,
                                                            out_kwargs))

    def start(self):
        self._inp_proc.start()
        self._out_proc.start()
        kill_out_proc = False
        while True:
            if self._terminate:
                return 1
            args = []
            for i in range(self.nthreads):
                try:
                    obj = self._inp_q.get_nowait()
                    if isinstance(obj, PoisonPill):
                        kill_out_proc = True
                        break
                    else:
                        args += [obj]
                except Empty:
                    break
            res = self.main_pool.map(self.main, args)
            for obj in res:
                self._out_q.put(obj)
            if kill_out_proc:
                self.kill_out_proc()
                return

    def terminate(self):
        self._terminate = True
        self._inp_proc.terminate()
        self._out_proc.terminate()

    def kill_out_proc(self):
        self._out_q.put(PoisonPill())

class MultiThreadedProcessorError(Exception):
    def __init__(self):
        pass

class PoisonPill:
    def __init__(self):
        pass

def isfunction(f):
    return hasattr(f, '__call__')
