"""
Definition of VectorSweep, LinearSweep and LogSweep.
"""

from .base import Sweep, SweepStep, SweepResult
import numpy as np
from itertools import chain, repeat


class VectorSweep(Sweep):

    '''
    Sweep with Fixed x values.
    '''

    def __init__(self, vector, roundtrip=False, npasses=1, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.vector = vector
        self.roundtrip = roundtrip
        self.npasses = npasses

        self._result = None
        self._step = None
        self._iterator = None

    @property
    def result(self):
        return self._result

    def __iter__(self):

        # reset result
        self._result = SweepResult([], [])
        self._step = None

        # prepare passes
        vector = self.vector

        if self.roundtrip:
            values = list(vector)
            vector = chain(values[::1], values[::-1])

        # repeat the vector for each pass
        self._iterator = enumerate(chain(*repeat(vector, self.npasses)))

        # start timer
        super().start_timer()

        return self

    def __next__(self):

        # save data of the previous step
        if self._step is not None:
            self._result = self._result + [self._step.x, self._step.y]

        n, x = next(self._iterator)
        self._step = SweepStep(
            x = x,
            step_number = n, total = len(self),
            elapsed_time = self.get_elapsed_time(),
        )

        # may change x and y
        return self._step

    def __len__(self):

        total = len(self.vector) * self.npasses

        if self.roundtrip:
            total = total * 2

        return total

    def __repr__(self):

        vmin = min(self.vector)
        vmax = max(self.vector)
        nsteps = len(self.vector)

        opts = [f'{nsteps} steps']

        if self.roundtrip:
            opts = opts + ['roundtrip']

        if self.npasses > 1:
            opts = opts + [f'{self.npasses} passes']

        opts = ', '.join(opts)

        return f'<{self.__class__.__name__} [{vmin:.2g}, {vmax:.2g}] ({opts})>'


class LinearSweep(VectorSweep):

    '''Evenly distributed steps in a linear space.'''

    def __init__(self, start, stop, nsteps=None, step_size=None, *args, **kwargs):

        # save previous step result
        if step_size is not None:
            nsteps = int(round(abs((stop - start) / step_size))) + 1

        vector = np.linspace(start, stop, nsteps)

        super().__init__(vector, *args, **kwargs)


class LogSweep(VectorSweep):

    '''Evenly distributed steps in a logarithmic space.'''

    def __init__(self, start, stop, nsteps, *args, **kwargs):

        vector = np.logspace(np.log10(start), np.log10(stop), nsteps)

        super().__init__(vector, *args, **kwargs)
