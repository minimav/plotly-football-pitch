import random

import numpy as np
import pytest

from plotly_football_pitch import (
    add_heatmap,
    make_pitch_figure,
    PitchDimensions,
)
from plotly_football_pitch.pitch_background import (
    AttackVsDefenceBackground,
    ChequeredBackground,
    HorizontalStripesBackground,
    SingleColourBackground,
    VerticalStripesBackground,
)


def test_number_of_pitch_markings():
    """Basic pitch should have expected number of pitch markings.

    These are the 9 linear markings found on the figure's `data` attribute:
      * pitch outline
      * halfway-line
      * 2x 6-yard box
      * 2x 18-yard box
      * 2x penalty spots
      * centre spot

    These 3 non-linear markings are added to the layout's shapes
    attribute:
      * centre circle
      * 2x penalty box arcs
    """
    dimensions = PitchDimensions()
    fig = make_pitch_figure(dimensions)

    # linear markings
    assert len(fig.data) == 9

    # curved markings
    assert len(fig.layout.shapes) == 3


@pytest.mark.parametrize(
    "pitch_width_metres, pitch_length_metres",
    [(10, 10), (105, 68), (68, 105), (100, 100), (2, 30)],
)
def test_different_pitch_dimensions(pitch_width_metres, pitch_length_metres):
    """No errors are raised when custom dimensions are used."""
    dimensions = PitchDimensions(
        pitch_width_metres,
        pitch_length_metres,
    )
    fig = make_pitch_figure(dimensions)
    assert fig


@pytest.mark.parametrize(
    "width_grid, length_grid", [(10, 10), (5, 12), (4, 6), (15, 12)]
)
def test_adding_heat_maps(width_grid, length_grid):
    """Heatmaps of different grid sizes can be added successfully."""
    dimensions = PitchDimensions()
    fig = make_pitch_figure(dimensions)
    num_data_on_plot = len(fig.data)

    random.seed(1234)
    data = np.array(
        [[random.random() for _ in range(length_grid)] for _ in range(width_grid)]
    )
    fig = add_heatmap(fig, data)

    assert len(fig.data) == num_data_on_plot + 1


@pytest.mark.parametrize(
    "pitch_background_cls, kwargs",
    [
        (
            AttackVsDefenceBackground,
            {"attack_colour": "#425AFE", "defence_colour": "blue"},
        ),
        (
            ChequeredBackground,
            {
                "colours": ["blue", "#FFAAFF"],
                "num_horizontal_stripes": 4,
                "num_vertical_stripes": 3,
            },
        ),
        (
            HorizontalStripesBackground,
            {"colours": ["#425AFE", "#F22F34"], "num_stripes": 12},
        ),
        (SingleColourBackground, {"colour": "green"}),
        (
            VerticalStripesBackground,
            {"colours": ["black", "grey", "orange"], "num_stripes": 10},
        ),
    ],
)
def test_adding_pitch_backgrounds(pitch_background_cls, kwargs):
    """Different backgrounds can be added successfully."""
    dimensions = PitchDimensions()
    pitch_background = pitch_background_cls(**kwargs)
    make_pitch_figure(dimensions, pitch_background=pitch_background)
