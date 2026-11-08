# Probability Simulations Lab — Startup Careers & Roulette

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Tests](https://img.shields.io/badge/tests-pytest-green.svg)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A fork of [`nogibjj/Coursera-MLOps-C2-lab3-probability-simulations`](https://github.com/nogibjj/Coursera-MLOps-C2-lab3-probability-simulations),
**modernised to Python 3.12** and extended with an original enhancement to the
roulette simulator that empirically demonstrates the gambler's fallacy.

The purpose of this laboratory is to employ Monte Carlo simulations in order
to model two real‑world scenarios: the **professional career within startups**
as contrasted with the **portfolio of a venture‑capital investor**, and the
behaviour of a **European roulette wheel**.

---

## Table of contents

- [Repository context](#repository-context)
- [Original laboratory objectives](#original-laboratory-objectives)
- [Modernisation to Python 3.12 (first commit)](#modernisation-to-python-312-first-commit)
- [How to run](#how-to-run)
- [A. Startup and VC‑portfolio simulations](#a-startup-and-vc-portfolio-simulations)
  - [Principal results](#principal-results)
  - [Reflection A1 — employee versus investor](#reflection-a1--employee-versus-investor)
  - [Reflection A2 — why simulate first](#reflection-a2--why-simulate-first)
  - [Bugs corrected in `startup_game.py`](#bugs-corrected-in-startup_gamepy)
- [B. Roulette](#b-roulette)
  - [Base command executed](#base-command-executed)
  - [Reflection B1 — the gambler's fallacy](#reflection-b1--the-gamblers-fallacy)
  - [Original enhancement: `streak-analysis`](#original-enhancement-streak-analysis)
  - [Reflection B2 — contribution of the enhancement](#reflection-b2--contribution-of-the-enhancement)
- [Repository structure (schema)](#repository-structure-schema)
- [Tests](#tests)
- [Work history](#work-history)
- [References](#references)
- [Author](#author)

---

## Repository context

| Field | Value |
|---|---|
| Base repository | [`nogibjj/Coursera-MLOps-C2-lab3-probability-simulations`](https://github.com/nogibjj/Coursera-MLOps-C2-lab3-probability-simulations) |
| Fork | [`AntonioBernalNavarro/Coursera-MLOps-C2-lab3-probability-simulations`](https://github.com/AntonioBernalNavarro/Coursera-MLOps-C2-lab3-probability-simulations) |
| Working branch | `feature/lab3-portfolio` |
| Runtime | Python 3.12 (devcontainer + Codespaces) |
| Status | Section A complete; Section B in progress |

---

## Original laboratory objectives

The original laboratory defines two blocks of tasks that this fork executes
and documents:

**A. Simulate career earnings versus an investor's portfolio**

1. Execute `startup_game.py` and explore each command (`sanity`, `simulate`,
   `simulate_multiple`, `vcportfolio`).
2. Construct an original VC portfolio using `vcportfolio` and a startup career
   using `simulate_multiple`.
   - *Reflection:* What has been learnt regarding the payoff of a regular
     employee as opposed to that of an investor?
   - *Reflection:* Why are simulations important as first modelling steps?

**B. Determine whether roulette wheels exhibit patterns that a simulation can detect**

1. Execute `roulette.py spin --count 10 --color red --bet 1`.
   - *Reflection:* Is it prudent to place a large bet on red after observing
     ten consecutive black numbers?
   - *Reflection:* Which behaviour could be added to the roulette simulator in
     order to improve it? Implement it and construct a portfolio project that
     demonstrates the enhancement.

> This section is retained as a reference to the original scope. The results
> and the answers to the reflection questions are developed below.

---

## Modernisation to Python 3.12 (first commit)

The first commit of the fork (`Modernize devcontainer and dependencies for
Python 3.12 compatibility`) resolves the cascade of incompatibilities that
prevented the construction of the development container from a Python 3.12
base image. The original repository dates from 2022 and carried dependencies
that do not compile on 3.12: reliance on `pkg_resources`, `distutils`,
`numpy.distutils` and `imp`, together with wheels that do not exist for
several versions of torch and tensorflow.

### Modified files

#### `requirements.txt`

| Package | Before | After | Rationale |
|---|---|---|---|
| pandas | 1.5.0 | **2.2.2** | Removes the `pkg_resources` dependency |
| numpy | 1.23.3 | **1.26.4** | Removes the `distutils` dependency |
| scikit-learn | 1.1.2 | **1.5.0** | Removes the `numpy.distutils` dependency |
| databricks-cli | 0.17.3 | **0.18.0** | Removes the `imp` dependency |
| torch | 1.12.1 | **2.5.1** | Python 3.12 support |
| torchvision | 0.13.1 | **0.20.1** | Python 3.12 support |
| tensorflow | 2.10.0 | **2.16.2** | First release with 3.12 wheels |
| mlflow | 1.29.0 | **2.22.0** | Resolves the `pandas<2` constraint |
| databricks-sql-connector | 2.1.0 | **4.4.0** | Resolves the `pandas<2` constraint |
| protobuf | 3.16.0 | **4.25.3** | Resolves the conflict with onnx/streamlit |
| onnx | 1.12.0 | **1.16.0** | protobuf compatibility |
| streamlit | 1.13.0 | **1.24.0** | protobuf compatibility |
| tokenizers | 0.12.1 | **0.19.1** | Pre‑built wheels |
| transformers | 4.22.2 | **4.41.2** | tokenizers compatibility |

#### `.devcontainer/Dockerfile`

- Added `libjpeg-dev`, `zlib1g-dev` and `libpng-dev` (required to compile
  Pillow when no pre‑built wheel is available).
- Removed the Yarn APT source, which caused `apt-get update` to fail with exit
  code 100.
- Introduced retry logic and ensured that `ca-certificates` are installed
  before refreshing the package lists.

#### `.devcontainer/devcontainer.json`

- Replaced the **Oryx** build command (which no longer supports Python 3.12)
  with an explicit and deterministic sequence: creation of a virtual
  environment followed by `pip install -r requirements.txt`. Oryx was the root
  cause of the failure in `postCreateCommand`.

#### `.vscode/`

- Added workspace‑specific settings: Python interpreter and linting
  configuration. These are optional but improve the developer experience.

### Outcome

The development container starts successfully, dependencies are installed
without source compilation, and the laboratory notebooks execute without
dependency‑resolution errors.

---

## How to run

```bash
# 1) Environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2) Dependencies
pip install -r requirements.txt

# 3) Verify installation
./startup_game.py --help
./roulette.py --help
make test
```

---

## A. Startup and VC‑portfolio simulations

### Principal results

All executions are documented, together with their full analysis, in
[`docs/lab-report.md`](docs/lab-report.md).

| Command | Purpose | Key result |
|---|---|---|
| `./startup_game.py sanity` | Verify the law of large numbers (p=0.5 and p=0.023) | 50/50 and 2/98 ≈ 2.3% ✔ |
| `./startup_game.py simulate --simulations 4 --probability 0.023` | Realistic individual career | **Total: $0** (P(0 successes) = 0.977⁴ ≈ 91%) |
| `./startup_game.py simulate_multiple --people 20 --simulations 4 --probability 0.5` | Mechanism control with high p | 95% generate a return, mean $1.75M |
| `./startup_game.py vcportfolio --simulations 20 --probability 0.023` | VC portfolio, realistic rate | **ROI −100%** ($77.74M invested → $0) |
| `./startup_game.py vcportfolio --simulations 50 --probability 0.1` | VC portfolio, favourable rate | **ROI +5127%** ($252.85M → $13,216.72M) |

### Reflection A1 — employee versus investor

The simulation exposes a **structural asymmetry** rather than a difference in
fortune:

1. **The regular employee inhabits the left tail.** With the realistic
   success rate (p=0.023, the "1 in 43" documented within the code itself), a
   professional who passes through four startups over roughly sixteen years
   faces `P(0 successes) = 0.977⁴ ≈ 91%`. The **modal** outcome of the
   execution was precisely this: `Total: $0`. The employee's remuneration is a
   salary of low variance, but with equity modelled as a low‑probability
   lottery exhibiting a **capped upside** (1% of a $100M company = $1M per
   success, with no possibility of capturing the tail).

2. **The investor inhabits the right tail.** The same success rate, applied to
   a portfolio of twenty companies, produced an ROI of `−100%` (zero
   successes, with an *a priori* probability of approximately 63%). However,
   upon raising p to 0.1 across a portfolio of fifty investments, the return
   jumped to **+5127%**: $252.85M invested yielded $13,216.72M. No median
   investment justifies this figure — **one or two outliers carry the entire
   fund**. This is the signature of the *power law*: the mean is irrelevant,
   the median is misleading, and only the tail pays.

3. **Conclusion.** The employee sells time in exchange for stability and
   accepts a ceiling in return for a floor; the investor accepts total loss on
   the majority of positions in order to purchase unlimited optionality. The
   two profiles are not comparable: employee equity should be valued as a
   **lottery with a ceiling**, not as deferred salary, since in 91% of
   scenarios it is worth exactly $0.

> **Methodological note:** the case `p=0.5`, in which 95% of individuals
> generate a return, is included solely as a *smoke test* of the mechanism. It
> is **not** representative of the real world: at p=0.5, any portfolio wins.

### Reflection A2 — why simulate first

1. **Simulations reveal the shape of the distribution, not merely its mean.**
   The portfolio's ROI shifted from −100% to +5127% by moving p from 0.023 to
   0.1 over the same mechanism. A spreadsheet based on point estimates would
   have reported a single figure and concealed the fact that 63% of realistic
   scenarios end in ruin. Simulation forces the analyst to examine the entire
   distribution.

2. **Simulations render assumptions explicit and falsifiable.** Before writing
   any production code, simulation compels the analyst to declare: success
   rate (0.023), equity per employee (1%), valuation ($100M), portfolio size
   (20–50) and investment range ($10k–$10M). These figures may be contested —
   and that is precisely their value: they transform an intuition ("startups
   are risky") into a **quantified hypothesis** that can be validated or
   refuted against real data.

3. **Simulations are inexpensive, rapid and reproducible.** The entire
   laboratory executed in seconds. Before instrumenting a pipeline or
   procuring data, a fifty‑line Monte Carlo simulation identifies which
   variable dominates the outcome (in this case, `p` and the valuation tail)
   and which variables constitute noise.

4. **The `sanity` check functions as the *unit test* of the model.** The
   `sanity` command itself detected two genuine bugs in the original code (see
   below). Modelling without *sanity checks* is analogous to deploying without
   tests: the failure is discovered in production.

### Bugs corrected in `startup_game.py`

The `sanity` check and the execution of `vcportfolio` revealed three bugs in
the original code (not introduced by the modernisation), corrected on the
`feature/lab3-portfolio` branch:

| # | Bug | Symptom | Root cause | Fix |
|---|---|---|---|---|
| 1 | `TypeError` in `sanity` | `unsupported format string passed to list.__format__` at `startup_game.py:16` | `generate_true_false` expects a scalar, whereas `sanity_test` invokes it with `[p, 1-p]`. In Python, `[0.5, 0.5] * 100` concatenates rather than scales. | The function now accepts either a scalar or a `[p_true, p_false]` pair, validates that the probabilities sum to 1, and selects `p_true`. This corrects both callers simultaneously. |
| 2 | Double sampling in `calculate_value_multiple` | The count of winners and the total employed distinct random draws | `calculate_value` was invoked twice per individual: once for the `if > 0` test and once for the accumulation into the total | A single invocation per individual; the resulting `value` is reused |
| 3 | Incorrect ROI in `simulate_investor` | `percentage_return_on_investment` was computed against the *payout* | Division by payout rather than by invested capital | `(payout − invested) / invested` (relative to capital) |

**Design quirk documented (not corrected):** `simulate_investor` generates
`simulations` scenarios per iteration but consumes only `scenarios[0]`. The
per‑company distribution remains Bernoulli(p), so the aggregate result is
statistically correct; only the per‑batch *printout* is misleading
(`SUCCESS: 1` need not imply a payout if the success does not occupy position
0). This is documented in order not to alter the original behaviour of the
laboratory.

---

## B. Roulette

### Base command executed

```bash
./roulette.py spin --count 10 --color red --bet 1
```

The execution and its balance are recorded in `docs/lab-report.md`.

### Reflection B1 — the gambler's fallacy

It is not prudent. On a fair European roulette wheel, `P(red) = 18/37 ≈ 48.65%`
on **each** spin, independently of all previous outcomes. Ten consecutive
black numbers carry a probability of `(19/37)^10 ≈ 0.16%` — a rare but
possible event whose occurrence **does not increase** the future probability
of red. This is the **gambler's fallacy**: conflating the *a priori*
probability of a streak with the *conditional* probability of the next spin.
Increasing the stake in expectation of "compensation" constitutes a martingale
strategy that amplifies variance and may exhaust the bankroll before recovery.

### Original enhancement: `streak-analysis`

**Status:** in progress on the `feature/lab3-portfolio` branch.

The original simulator merely *generates* spins; it does not *explain* the
pattern that the user believes to perceive. The enhancement introduces a
command that simulates N spins, detects streaks of the opposite colour, and
empirically tests the gambler's fallacy:

- `P(colour | streak of opposite colour of length L)` for `L = 1..8` → expected
  to be **flat** and equal to `18/37`.
- χ² test of uniformity over the complete sequence.
- Export of a CSV file and a plot to `docs/img/` for integration into
  notebooks.
- Pure function `spin_once(rng)` extracted so that it can be unit‑tested.

### Reflection B2 — contribution of the enhancement

The enhancement converts an erroneous intuition into a **falsifiable
hypothesis** and refutes it with reproducible evidence. From an engineering
perspective, it separates the sampling logic (`spin_once`) so that it can be
tested, adds `--seed` for reproducibility, and provides `--export` for
integration with the analysis. From a pedagogical perspective, it demonstrates
that observed streaks follow the expected geometric distribution and that the
future probability does not depend on the history.

---

## Repository structure (schema)

```text
.
├── .devcontainer/
│   ├── Dockerfile                    # Added libjpeg/zlib/libpng; Yarn APT removed
│   └── devcontainer.json             # Oryx replaced by explicit virtualenv + pip
├── .vscode/
│   └── settings.json                 # Interpreter, linting
├── docs/
│   ├── img/                          # Generated plots
│   └── lab-report.md                 # Report with results and reflections
├── mylib/                            # Auxiliary library from the original repository
├── notebooks/
│   └── exploration.ipynb             # Analysis with pandas/matplotlib
├── tests/
│   ├── test_main.py                  # Original tests
│   └── test_roulette.py              # Enhancement tests (pending)
├── .gitignore
├── LICENSE
├── Makefile                          # Targets: install, test, lint
├── README.md                         # This file
├── main.py
├── requirements.txt                  # Updated for Python 3.12
├── roulette.py                       # Roulette simulator (with enhancement)
└── startup_game.py                   # Startup and VC portfolio simulator
```

**Git workflow:**

```text
main ──●──●──●──●  (fork history)
        │
        └──●──●──●  feature/lab3-portfolio  (modernisation + fixes + report + enhancement)
```

---

## Tests

```bash
make test
# or directly
pytest tests/ -v
```

---

## Work history

| Commit | Type | Description |
|---|---|---|
| `Modernize devcontainer...` | `feat` | Modernisation to Python 3.12: requirements, Dockerfile, devcontainer, .vscode |
| `docs(lab3): document sanity...` | `docs` | Documented the `TypeError` incident and its fix |
| `fix(startup_game): root-cause...` | `fix` | Three root‑cause bugs corrected (sanity, double sampling, ROI) |
| `docs(lab3): add startup/VC...` | `docs` | Report with results and reflections A1/A2 |
| `docs: rewrite README...` | `docs` | README rewritten as a portfolio entry point |

---

## References

- Original repository: [`nogibjj/Coursera-MLOps-C2-lab3-probability-simulations`](https://github.com/nogibjj/Coursera-MLOps-C2-lab3-probability-simulations)
- Course: *Machine Learning Engineering for Production (MLOps)* — Coursera

---

## Author

**Antonio Bernal Navarro**
- GitHub: [@AntonioBernalNavarro](https://github.com/AntonioBernalNavarro)
- LinkedIn: _(add your URL)_