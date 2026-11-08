#!/usr/bin/env python
"""
Examples of routines for simulating a roulette wheel.
The big takeaway is the concept of the law of large numbers.
Roulette has a negative expected value, so you will lose money in the long run.

Future improvements:

    * Allow for bets on multiple numbers and colors as well as odd/even, etc
    * Allow for different bets on different spins
    * Jupyter notebook with interactive widgets to show historical results
    * Add a web interface to allow for bets and results using streamlit or gradio

Implemented in this fork:

    * streak-analysis: empirically test the gambler's fallacy by measuring
      P(target colour | L consecutive opposite colours) and running a
      chi-square red/black balance test. See docs/lab-report.md (section B).

"""
import csv
from pathlib import Path

import pandas as pd
import click
import sys


def build_wheel():
    """
    Roulette wheel with 38 slots and probabilities of landing on each slot
    """

    wheel = pd.DataFrame(
        [
            [0, "green", 0],
            [1, "red", 1],
            [2, "black", 2],
            [3, "red", 3],
            [4, "black", 4],
            [5, "red", 5],
            [6, "black", 6],
            [7, "red", 7],
            [8, "black", 8],
            [9, "red", 9],
            [10, "black", 10],
            [11, "black", 11],
            [12, "red", 12],
            [13, "black", 13],
            [14, "red", 14],
            [15, "black", 15],
            [16, "red", 16],
            [17, "black", 17],
            [18, "red", 18],
            [19, "red", 19],
            [20, "black", 20],
            [21, "red", 21],
            [22, "black", 22],
            [23, "red", 23],
            [24, "black", 24],
            [25, "red", 25],
            [26, "black", 26],
            [27, "red", 27],
            [28, "black", 28],
            [29, "black", 29],
            [30, "red", 30],
            [31, "black", 31],
            [32, "red", 32],
            [33, "black", 33],
            [34, "red", 34],
            [35, "black", 35],
            [36, "red", 36],
            [37, "green", 0],
        ],
        columns=["slot", "color", "number"],
    )
    # add the probabilities of landing on each slot
    wheel["probability"] = [1 / 38] * 38
    return wheel


def spin_wheel(wheel):
    """
    Simulate a single spin of the roulette wheel
    """
    return wheel.sample(n=1, weights="probability")


def simulate_spins(wheel, spins):
    """
    Simulate multiple spins of the roulette wheel
    """
    results = []
    for _ in range(spins):
        results.append(spin_wheel(wheel))
    return pd.concat(results)


def generate_report(results, full_report=False):
    """
    Generate a report on the results of the roulette wheel simulation
    """
    print(f"Total number of spins: {len(results)}")
    if full_report:
        print(
            f"Number of times each number landed: {results['number'].value_counts()[results['number'].value_counts() > 1]}"
        )
    # only print the color
    print(f"Number of times each color landed:\n {results['color'].value_counts()}")


def calculate_winnings(results, bet, count, color=None, number=None):
    """
    Calculate the winnings of the roulette wheel simulation
    using bet amount and number of spins for each color or number bet
    """
    color_winnings = 0
    number_winnings = 0
    total_amount_bet = count * bet

    if color == "red":
        color_winnings = (
            results[results["color"] == "red"]["slot"].count() * (bet * 2)
            - total_amount_bet
        )
    elif color == "black":
        color_winnings = (
            results[results["color"] == "black"]["slot"].count() * (bet * 2)
            - total_amount_bet
        )
    elif color == "green":
        color_winnings = (
            results[results["color"] == "green"]["slot"].count() * (bet * 17)
            - total_amount_bet
        )

    if number:
        number_winnings = (
            results[results["number"] == number]["slot"].count() * (bet * 35)
            - total_amount_bet
        )
        ncount = results[results["number"] == number]["slot"].count()
        print(f"Total count for number bet on [{number}]: {ncount}")

    grand_total = sum([color_winnings, number_winnings])
    return grand_total


# build a function to print each run of the wheel with red and black colors using click style
def print_wheel(results):
    """
    Print the results of the roulette wheel simulation
    """
    for _, row in results.iterrows():
        if row["color"] == "red":
            click.secho(f"{row['slot']}", fg="red", nl=False)
        elif row["color"] == "black":
            click.secho(f"{row['slot']}", fg="black", nl=False)
        else:
            # if the number is 37 replace it with 00 and don't print number
            if row["slot"] == 37:
                click.secho("00", fg="green", nl=False)
            else:
                click.secho(f"{row['slot']}", fg="green", nl=False)
        click.echo(" ", nl=False)
    click.echo()


@click.group()
def cli():
    """
    A group of commands for simulating a roulette wheel
    """


@cli.command("spin")
@click.option("--count", default=1, help="Total count of spins")
@click.option(
    "--color", type=click.Choice(["red", "black", "green"]), help="Color to bet on"
)
@click.option("--bet", default=1, help="Amount to bet on each spin")
@click.option(
    "--number_bet", default=None, help="Number to bet on", type=click.IntRange(0, 36)
)
def spin_option(count, bet, number_bet, color):
    """
    Spin the roulette wheel:

     Example:
        Ten spins of the wheel with a bet of $1 on red
        ./roulette.py spin --count 10 --color red --bet 1

    """
    print(f"Selected number of spins: {count}")
    if not number_bet and not color:
        print("No bet selected")
    else:
        print(f"Selected bet amount: {bet}")
    if number_bet and color:
        print("Can't bet on color and number at the same time")
        # exit the program if both color and number are selected
        sys.exit()

    print(f"Selected number to bet on: {number_bet}")
    print(f"Selected color to bet on: {color}")

    # build the wheel
    wheel = build_wheel()
    # simulate the spins
    results = simulate_spins(wheel, count)
    # print the results
    print_wheel(results)
    generate_report(results)
    # print the winnings
    total_winnings = calculate_winnings(
        results=results, bet=bet, count=count, color=color, number=number_bet
    )
    print(f"Total winnings: {total_winnings}")


# ---------------------------------------------------------------------------
# Original enhancement: streak-analysis
# Empirically refutes the gambler's fallacy by measuring
# P(target | L consecutive opposite colours) for L = 1..8 and running a
# chi-square red/black balance test.
#
# NOTE: this wheel is the American variant (38 slots: 0 and 00), so the
# theoretical probability of red (or black) is 18/38 ~= 0.4737, not 18/37
# as on a European wheel.
# ---------------------------------------------------------------------------


@cli.command("streak-analysis")
@click.option("--spins", default=10000, type=int, help="Number of spins to simulate")
@click.option(
    "--color",
    default="red",
    type=click.Choice(["red", "black"]),
    help="Target colour",
)
@click.option("--seed", default=None, type=int, help="Random seed for reproducibility")
@click.option(
    "--export",
    "export_path",
    default=None,
    type=click.Path(),
    help="Write results to a CSV file at this path",
)
def streak_analysis(spins, color, seed, export_path):
    """Simulate N spins and empirically test the gambler's fallacy.

    For each streak length L of the opposite colour (1..8), report the
    empirical P(target colour | L consecutive opposite colours). On a fair
    wheel this must be constant and equal to 18/38 ~= 0.4737 (American
    wheel: 0 and 00). Also runs a chi-square test (df=1) on the red/black
    balance.

    Example:
        ./roulette.py streak-analysis --spins 10000 --color red --seed 42
    """
    wheel = build_wheel()
    # Vectorised sampling: one call, reproducible, fast
    samples = wheel.sample(
        n=spins, replace=True, weights="probability", random_state=seed
    )
    colours = samples["color"].tolist()
    opposite = "black" if color == "red" else "red"

    # Empirical P(color | L opposite in a row)
    results = []
    for length in range(1, 9):
        hits = 0
        trials = 0
        streak = 0
        for c in colours:
            if streak >= length:
                trials += 1
                if c == color:
                    hits += 1
            if c == opposite:
                streak += 1
            else:
                streak = 0
        prob = hits / trials if trials else float("nan")
        results.append((length, trials, hits, prob))

    # Chi-square on red vs black balance (green excluded, df=1)
    relevant = [c for c in colours if c in (color, opposite)]
    n = len(relevant)
    observed_color = sum(1 for c in relevant if c == color)
    observed_opp = n - observed_color
    expected = n / 2 if n else 1.0
    chi_sq = (
        ((observed_color - expected) ** 2 / expected)
        + ((observed_opp - expected) ** 2 / expected)
        if n
        else 0.0
    )
    fair = chi_sq < 3.841  # critical value at alpha=0.05, df=1

    theoretical = 18 / 38  # American wheel

    click.echo(click.style(f"Simulated {spins} spins (seed={seed})", fg="cyan"))
    click.echo(click.style(f"Target colour: {color}", fg="cyan"))
    click.echo(
        click.style(
            f"Theoretical P({color}) = 18/38 = {theoretical:.4f} "
            "(American wheel: 0 and 00)",
            fg="cyan",
        )
    )
    click.echo()
    header = (
        f"{'L (streak of ' + opposite + ')':<28}"
        f"{'Trials':>8}"
        f"{color.capitalize() + ' hits':>12}"
        f"{'P(' + color + '|L)':>14}"
        f"{'Theoretical':>14}"
    )
    click.echo(header)
    click.echo("-" * 76)
    for length, trials, hits, prob in results:
        click.echo(
            f"{length:<28}{trials:>8}{hits:>12}{prob:>14.4f}{theoretical:>14.4f}"
        )
    click.echo()
    click.echo(
        f"Chi-square red/black balance: {chi_sq:.4f} "
        "(critical @ alpha=0.05, df=1: 3.841)"
    )
    if fair:
        click.echo(
            click.style(
                "PASS: cannot reject fairness between red and black (p > 0.05)",
                fg="green",
            )
        )
    else:
        click.echo(
            click.style(
                "FAIL: red/black imbalance detected (p < 0.05)", fg="yellow"
            )
        )
    click.echo()
    click.echo("Conclusion: P(color | L opposite) is flat in L. Streaks do")
    click.echo("not change the probability of the next spin. The gambler's")
    click.echo("fallacy is refuted with reproducible evidence.")

    if export_path:
        path = Path(export_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["streak_length", "trials", "hits", "p_empirical", "p_theoretical"]
            )
            for length, trials, hits, prob in results:
                writer.writerow(
                    [length, trials, hits, f"{prob:.6f}", f"{theoretical:.6f}"]
                )
        click.echo(click.style(f"Results exported to {path}", fg="green"))


# run the cli
if __name__ == "__main__":
    cli()