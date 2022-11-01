# vsweep
An elegant way to perform sweeps.

## Installation

`pip3 install git+ssh://git@github.com/VianneyRousset/vsweep.git`

## Usage

```python
from vsweep import LinearSweep, LogSweep, AdaptiveSweep

# perform a linear sweep between 0 and 10 in 20 steps
sweep = AdaptiveSweep()

for step in sweep:
    step.y = measure(step.x)

result = sweep.result
plt.plot(result.x, result.y)
```
