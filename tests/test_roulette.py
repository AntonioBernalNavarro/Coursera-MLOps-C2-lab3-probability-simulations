"""Tests for the streak-analysis enhancement in roulette.py."""
import re

import pandas as pd
from click.testing import CliRunner

from roulette import build_wheel, cli, simulate_spins, spin_wheel


def test_build_wheel_shape():
    wheel = build_wheel()
    assert len(wheel) == 38
    assert {"slot", "color", "number", "probability"} <= set(wheel.columns)
    assert abs(wheel["probability"].sum() - 1.0) < 1e-9


def test_build_wheel_colour_counts():
    """American wheel: 18 red, 18 black, 2 green (0 and 00)."""
    counts = build_wheel()["color"].value_counts().to_dict()
    assert counts == {"red": 18, "black": 18, "green": 2}


def test_spin_wheel_returns_one_row():
    result = spin_wheel(build_wheel())
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1


def test_simulate_spins_count():
    assert len(simulate_spins(build_wheel(), 50)) == 50


def test_streak_analysis_cli_runs():
    result = CliRunner().invoke(
        cli, ["streak-analysis", "--spins", "2000", "--seed", "42"]
    )
    assert result.exit_code == 0, result.output
    assert "gambler's" in result.output
    assert "0.4737" in result.output  # 18/38


def test_streak_analysis_reproducible_with_seed():
    runner = CliRunner()
    r1 = runner.invoke(cli, ["streak-analysis", "--spins", "500", "--seed", "123"])
    r2 = runner.invoke(cli, ["streak-analysis", "--spins", "500", "--seed", "123"])
    assert r1.output == r2.output


def test_streak_analysis_exports_csv(tmp_path):
    out = tmp_path / "streak.csv"
    result = CliRunner().invoke(
        cli,
        ["streak-analysis", "--spins", "1000", "--seed", "1", "--export", str(out)],
    )
    assert result.exit_code == 0, result.output
    assert out.exists()
    lines = out.read_text().strip().splitlines()
    assert lines[0] == "streak_length,trials,hits,p_empirical,p_theoretical"
    assert len(lines) == 9  # header + 8 streak lengths


def test_streak_analysis_p_is_flat_in_l():
    """P(red | L blacks) must stay near 18/38 for small L, with enough spins."""
    result = CliRunner().invoke(
        cli, ["streak-analysis", "--spins", "50000", "--seed", "7"]
    )
    assert result.exit_code == 0
    m = re.search(r"^1\s+\d+\s+\d+\s+([\d.]+)", result.output, re.MULTILINE)
    assert m is not None
    p_1 = float(m.group(1))
    assert 0.43 < p_1 < 0.52  # 18/38 ≈ 0.474, generous CI at 50k spins