# Laboratory 3 — Probability Simulations

**Author:** Antonio Bernal Navarro
**Repository:** fork of `nogibjj/Coursera-MLOps-C2-lab3-probability-simulations`, modernised to Python 3.12.

## A. Startup and Venture-Capital Portfolio Simulations

### A.1 Commands executed

| Command | Key result |
|---|---|
| `./startup_game.py sanity` | 50/50 and 2/98 ≈ 2.3% |
| `./startup_game.py simulate --simulations 4 --probability 0.023` | **Total: $0** (P(0 successes) = 0.977⁴ ≈ 91%) |
| `./startup_game.py simulate_multiple --people 20 --simulations 4 --probability 0.5` | 95% generate a return, mean $1.75M |
| `./startup_game.py vcportfolio --simulations 20 --probability 0.023` | **ROI −100%** ($77.74M → $0) |
| `./startup_game.py vcportfolio --simulations 50 --probability 0.1` | **ROI +5127%** ($252.85M → $13,216.72M) |

### A.2 Reflection A1 — employee versus investor

The simulation exposes a structural asymmetry. At p = 0.023, a professional who passes through four startups faces P(0 successes) = 0.977⁴ ≈ 91%, with a modal outcome of $0. Their equity is a lottery with a ceiling (1% of a $100M company = $1M per success). The investor, facing the same rate, observes −100% across twenty investments (an *a priori* probability of approximately 63%); however, upon raising p to 0.1 and the portfolio to fifty companies, the return rises to +5127%, with one or two outliers carrying the entire fund (*power law*). The employee sells time in exchange for stability; the investor purchases unlimited optionality. The two profiles are not comparable.

### A.3 Reflection A2 — why simulate first

Simulations (1) reveal the shape of the distribution rather than merely its mean; (2) render assumptions explicit and falsifiable (success rate, equity, valuation, portfolio size); (3) are inexpensive, rapid and reproducible; (4) the `sanity` check functions as a unit test of the model (it detected three genuine bugs).

### A.4 Bugs corrected in `startup_game.py`

| # | Bug | Fix |
|---|---|---|
| 1 | `TypeError` in `sanity` (list × 100 concatenates) | `generate_true_false` now accepts a scalar or `[p_true, p_false]` |
| 2 | Double sampling in `calculate_value_multiple` | A single call to `calculate_value` per individual |
| 3 | ROI computed against payout | `(payout − invested) / invested` |

**Documented quirk:** `simulate_investor` generates `simulations` scenarios but consumes only `scenarios[0]`. The aggregate is correct; the per-batch printout is misleading.

## B. Roulette

### B.1 Base command

```bash
./roulette.py spin --count 10 --color red --bet 1
```

**Observed outcome:** `30 10 31 13 30 4 4 9 0 29` → 6 black, 3 red, 1 green. **Total winnings: −4**.

### B.2 Reflection B1 — is it prudent to bet heavily on red after ten blacks?

No. The wheel implemented in this repository is the American variant (38 slots: 0 and 00 green, 18 red, 18 black). P(red) = 18/38 ≈ 47.37% on each spin. Ten consecutive blacks carry a probability of (18/38)^10 ≈ 0.062% — rare but possible; their occurrence does not increase the future probability of red. This is the gambler's fallacy. Increasing the stake in expectation of "compensation" constitutes a martingale strategy that amplifies variance.

> Note: on a European wheel (37 slots) the probability would be 18/37 ≈ 48.65% and (18/37)^10 ≈ 0.16%. The qualitative conclusion is identical.

### B.3 Original enhancement: `streak-analysis`

**Motivation.** The original simulator merely generates spins; it does not explain the pattern that the user believes to perceive. `streak-analysis` converts the intuition into a falsifiable hypothesis.

**Result with `--spins 10000 --color red --seed 42`:**

```
L (streak of black)   Trials   Red hits   P(red|L)   Theoretical
1                      4758       2225      0.4676       0.4737
2                      2289       1056      0.4613       0.4737
3                      1114        543      0.4874       0.4737
4                       516        247      0.4787       0.4737
5                       238        129      0.5420       0.4737
6                        96         57      0.5938       0.4737
7                        33         24      0.7273       0.4737
8                         9          6      0.6667       0.4737

Chi-square red/black balance: 0.0341  (critical @ alpha=0.05, df=1: 3.841)
PASS: cannot reject fairness between red and black (p > 0.05)
```

**Interpretation.** P(red|L) is flat around 0.4737. The noise increases with L because `Trials` decreases exponentially. No value survives a Bonferroni correction (α = 0.05/8 = 0.00625). The data are compatible with a fair wheel; the gambler's fallacy is refuted.

**Reflection B2 — contribution of the enhancement.** It converts an erroneous intuition into a falsifiable hypothesis. It reuses `build_wheel()`, adds `--seed` (pandas `random_state`) and `--export`. It demonstrates that observed streaks follow the expected geometric distribution and that noise in short streaks does not constitute bias.

**Tests.** `tests/test_roulette.py` (8 tests): wheel shape, colour counts 18/18/2, spin contracts, seed reproducibility, CLI smoke test, CSV export, flatness at 50k spins.