# Conveyor Belt Model and Robust Real-Time Diagnosis Experiments

This directory contains the conveyor belt model and experiments conducted for our robust real-time diagnosis paper (under submission). It is structured as follows:

- [`parameters`](parameters): Contains `.toml` files defining different sets of parameters (latency, jitter, fault actions, fault injection, …) for diagnosis and the generation of observations for the experiments. These parameter files can be used with the `robust-diagnosis` command.
- [`scenarios`](scenarios): Contains `.toml` files describing model configurations (length of the belt and positions of the sensors). These are mainly for easy testing. Most experiments generate their own variants of the conveyor belt model.
- [`models`](models): Contains Momba IR models generated from scenarios.
- [`conveyor_belt`](conveyor_belt): Contains Python code for generating models for different model configurations as well as code for running the experiments and analyzing their results.

## Experiments

There are three experiments corresponding to the three sections in the empirical evaluation section of the paper:

- `scalability`: Investigate the scalability of the approach.
- `history_bound`: Investigate the impact of the history bound.
- `latency_jitter`: Investigate the impact of latency guarantees.

To run all experiments, this directory contains a script `run-all-experiments.sh`. Note that for this script to run, you first have setup everything:

1. Install [Poetry](https://python-poetry.org/). We use Poetry to manage the Python dependencies.
2. Run `poetry install` in this directory in order to setup a virtual environment with all the necessary dependencies.
3. Install [Rust and Cargo](https://rustup.rs/).
4. Build the `robust-diagnosis` binary by executing `cargo build --release` in the directory `engine/crates/robust-diagnosis` (relative to the root of this repository).

Now, you can run all experiments with `run-all-experiments.sh`. This will create an `output` directory per experiment. The output directory will contain the simulation runs and generated system models as well as some other information depending on the experiment.

To run different analyses on the generated output run

```
poetry run python -m conveyor_belt.experiments.scalability analyze
```

where `scalability` can be replaced with `history_bound` or `latency_jitter` to run analyses for the other experiments. Note that the analyses scripts require you to specify the output directory (previously generated by running the experiments). They also have additional options for which an explanation is provided via the `--help` switch.

The plots in the paper have been curated from the outputs of the analysis scripts: The script for `scalability` will output the values shown in the respective plot, the script for `history_bound` will output TikZ code for the box plots, and `latency_jitter` will also output TikZ code for the box plots.
