"""
Definition of AdaptiveSweep
"""

from .base import Sweep, SweepStep, SweepResult
import numpy as np
import adaptive
from itertools import chain, repeat


class AdaptiveSweep(Sweep):

    '''Dynamicly evaluated parameter step values base on the adaptive lib.'''

    def __init__(self, start, stop, npoints, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.start = start
        self.stop = stop
        self.npoints = npoints
        self._learner = None
        self._step = None

    @property
    def result(self):
        # sort data along x
        data = np.array(sorted(self._learner.data.items(), key=lambda v: v[0]))

        return SweepResult(*data.T)

    def __iter__(self):

        def nope(x):
            pass

        self._learner = adaptive.Learner1D(nope, (self.start, self.stop))

        # reset result
        self._result = SweepResult([], [])
        self._step = None

        return self

    def __next__(self):

        # save previous step result
        if self._step is not None:
            self._learner.tell(self._step.x, self._step.y)

        if self._learner.npoints >= self.npoints:
            raise StopIteration()

        self._step = SweepStep(
            x=self._learner.ask(1)[0][0],
            step_number=self._learner.npoints,
            total=self.npoints,
        )

        # may change x and y
        return self._step

    def __len__(self):
        return self.npoints
