## TTP-DFS

DFS pruning algorithm for finding all valid TTP schedules.

## Usage

### Generate Schedules

Generates all normalized (-N) schedules for `n=4` and saves them to the folder `Schedules_All`:

```sh
python3 run.py -N -s=All 4
```

### Calculate Differences

Calculates the differences between the normalized schedules and saves them to the folder `Differences`:

```sh
python3 calc.py ./Schedules/Schedules_All/All-4.csv 4
```

### Generate Plot

Generates the plot from the paper and saves it to the folder 'Plots':

```sh
python3 plot.py
```