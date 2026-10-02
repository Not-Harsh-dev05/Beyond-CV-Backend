"""Pure competence-minus-baseline delta calculation."""


def calculate_delta(competence: float, baseline: float) -> float:
    """Return competence score minus pedigree baseline score."""
    return round(float(competence) - float(baseline), 2)
