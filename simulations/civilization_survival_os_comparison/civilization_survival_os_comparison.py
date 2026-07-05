"""
Civilization Survival OS Comparison Simulation

This is an illustrative, non-predictive simulation for comparing two
civilizational operating principles:

1. Current Linear Civilization OS
2. Edo-like Circular Civilization OS

The model does not claim to reproduce historical reality or forecast the future.
It is a structural comparison model for Civilization OS research.

Author: Master / inchacomusho / InchaComisho
Co-created with: G (ChatGPT)
License: CC BY 4.0
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    """Keep an index within 0-100."""
    return max(low, min(high, value))


@dataclass(frozen=True)
class Scenario:
    name: str
    extraction: float
    waste: float
    reuse: float
    organic_return: float
    water_recharge: float
    cooling_recovery: float
    cohesion: float
    dependency_growth: float
    heat_stress: float


SCENARIOS: List[Scenario] = [
    Scenario(
        name="Current Linear Civilization OS",
        extraction=1.55,
        waste=1.25,
        reuse=0.18,
        organic_return=0.22,
        water_recharge=0.20,
        cooling_recovery=0.10,
        cohesion=0.32,
        dependency_growth=0.35,
        heat_stress=0.38,
    ),
    Scenario(
        name="Edo-like Circular Civilization OS",
        extraction=0.70,
        waste=0.45,
        reuse=0.78,
        organic_return=0.82,
        water_recharge=0.62,
        cooling_recovery=0.48,
        cohesion=0.72,
        dependency_growth=0.08,
        heat_stress=0.18,
    ),
]


def survival_score(state: Dict[str, float]) -> float:
    """
    Composite civilization survival score.

    Higher values mean the civilization retains ecological base,
    food security, natural cooling capacity, and social resilience.
    Waste pressure and external dependency reduce the score.
    """
    score = (
        0.17 * state["resource_base"]
        + 0.17 * state["soil_health"]
        + 0.16 * state["water_cycle"]
        + 0.16 * state["natural_cooling"]
        + 0.17 * state["food_security"]
        + 0.17 * state["social_resilience"]
        - 0.10 * state["waste_pressure"]
        - 0.07 * state["external_dependency"]
    )
    return clamp(score)


def simulate(scenario: Scenario, years: int = 250) -> List[Dict[str, float]]:
    """Run one scenario for the given number of years."""

    state = {
        "resource_base": 78.0,
        "soil_health": 74.0,
        "water_cycle": 74.0,
        "natural_cooling": 72.0,
        "food_security": 76.0,
        "social_resilience": 70.0,
        "waste_pressure": 20.0,
        "external_dependency": 25.0,
    }

    rows: List[Dict[str, float]] = []

    for year in range(years + 1):
        rows.append(
            {
                "scenario": scenario.name,
                "year": float(year),
                **state,
                "survival_score": survival_score(state),
            }
        )

        effective_extraction = scenario.extraction * (1.0 - scenario.reuse * 0.55)
        natural_assimilation = (
            (state["soil_health"] + state["water_cycle"]) / 200.0
        ) * (scenario.organic_return * 0.95 + scenario.reuse * 0.45)

        state["waste_pressure"] = clamp(
            state["waste_pressure"]
            + scenario.waste * (1.0 - scenario.reuse) * 0.68
            + scenario.extraction * 0.08
            - natural_assimilation * 0.75
        )

        state["external_dependency"] = clamp(
            state["external_dependency"]
            + scenario.dependency_growth
            + scenario.extraction * 0.04
            - scenario.reuse * 0.16
            - scenario.cohesion * 0.07
        )

        state["resource_base"] = clamp(
            state["resource_base"]
            - effective_extraction * 0.32
            - (state["waste_pressure"] / 100.0) * 0.055
            + scenario.organic_return * 0.14
            + scenario.reuse * 0.07
        )

        state["soil_health"] = clamp(
            state["soil_health"]
            + scenario.organic_return * 0.55
            + scenario.reuse * 0.18
            + (state["water_cycle"] - 50.0) * 0.006
            - state["waste_pressure"] * 0.019
            - scenario.extraction * 0.14
        )

        state["water_cycle"] = clamp(
            state["water_cycle"]
            + scenario.water_recharge * 0.45
            + (state["soil_health"] - 50.0) * 0.005
            - state["waste_pressure"] * 0.014
            - scenario.heat_stress * 0.14
        )

        state["natural_cooling"] = clamp(
            state["natural_cooling"]
            + scenario.cooling_recovery * 0.47
            + (state["water_cycle"] - 50.0) * 0.005
            + (state["soil_health"] - 50.0) * 0.003
            - scenario.heat_stress * 0.24
            - state["waste_pressure"] * 0.009
        )

        state["food_security"] = clamp(
            state["food_security"]
            + (state["soil_health"] - 50.0) * 0.009
            + (state["water_cycle"] - 50.0) * 0.008
            + (state["resource_base"] - 50.0) * 0.005
            - state["waste_pressure"] * 0.011
            - scenario.heat_stress * 0.16
            - state["external_dependency"] * 0.004
        )

        state["social_resilience"] = clamp(
            state["social_resilience"]
            + scenario.cohesion * 0.27
            + scenario.reuse * 0.10
            + (state["food_security"] - 50.0) * 0.005
            - state["external_dependency"] * 0.009
            - state["waste_pressure"] * 0.005
            - scenario.heat_stress * 0.06
        )

    return rows


def write_summary_csv(output_path: Path, interval: int = 25) -> None:
    """Write a compact CSV summary at fixed year intervals."""
    fields = [
        "scenario",
        "year",
        "resource_base",
        "soil_health",
        "water_cycle",
        "natural_cooling",
        "food_security",
        "social_resilience",
        "waste_pressure",
        "external_dependency",
        "survival_score",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()

        for scenario in SCENARIOS:
            rows = simulate(scenario)
            for row in rows[::interval]:
                rounded = {
                    key: (round(value, 2) if isinstance(value, float) else value)
                    for key, value in row.items()
                }
                rounded["year"] = int(rounded["year"])
                writer.writerow(rounded)


def main() -> None:
    output_path = Path(__file__).with_name("results_summary.csv")
    write_summary_csv(output_path)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
