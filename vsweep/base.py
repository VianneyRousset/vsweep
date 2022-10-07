"""
Abstract definition of a `Sweep` and definition of a `SweepStep` and a
`SweepResult`.

Iteration over a `Sweep` object yield `SweepSteps` with a `x` value. The value
measured at each step must be recorded in `SweepStep.y`. Sweep result is given
by `Sweep.result` as a `SweepResult` object containing both axis `SweepResult.x`
and `SwepResult.y`.
"""

from abc import ABC, abstractmethod, abstractproperty
from time import time


class Sweep(ABC):

    """
    An iterable giving each step and recording result.
    """

    def __init__(self):
        self.start_time = None

    def start_timer(self):
        self.start_time = time()

    def get_elapsed_time(self):

        if self.start_time is None:
            return 0.0

        return time() - self.start_time

    @abstractproperty
    def result(self):
        """Returns the result of the sweep in a SweepResult object."""
        raise NotImplementedError()

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError()

    @abstractmethod
    def __next__(self):
        raise NotImplementedError()


class SweepStep:

    """
    Step of a sweep.

    Members
    -------

    x: float
        The x value of the step

    y: float
        The measured value of the step

    n: int
        The nth step of the sweep.

    total: int
        The total planned number of steps of the sweep.

    elapsed_time: float
        Elapsed time since the first step.
    """

    def __init__(self, x, y=None, step_number=None, total=None, elapsed_time=None):
        self.x = x
        self.y = y
        self.n = step_number
        self.total = total
        self.elapsed_time = elapsed_time

    def __repr__(self):
        def tabulated(info):
            w = max(len(k) for k, v in info.items())
            fmt = "{:>" + str(w) + "} : {:e}"
            return "\n".join(fmt.format(k, v) for k, v in info.items())

        # format nicely the step number
        step = None
        if step is not None:
            if self.total is not None:
                step = f"{self.n} / {self.total}"
            else:
                step = f"{self.n} / ?"

        info = {
            "x": self.x,
            "y": self.y,
            "step": step,
            "elapsed time": self.elapsed_time,
        }

        # filter None info
        info = {k: v for k, v in info.items() if v is not None}

        return f"--- Sweep step ---\n" + tabulated(info)


class SweepResult:

    """
    Sweep result.

    Members
    -------

    x: array
        X axis values

    y: array
        Y axis values
    """

    def __init__(self, x, y):

        try:
            self.x = list(x)
            self.y = list(y)

        except TypeError:
            self.x = [x]
            self.y = [y]

    def __add__(self, other):
        other = SweepResult(*other)
        return SweepResult(self.x + other.x, self.y + other.y)

    def __iter__(self):
        return iter([self.x, self.y])
