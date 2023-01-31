import random

import numpy as np
import pytest

from plotly_football_pitch import (
    add_heatmap,
    make_pitch_figure,
    PitchDimensions,
)


def test_number_of_pitch_markings():
    """Basic pitch should have expected number of pitch markings.

    These are the 9 linear markings found on the figure's `data` attribute:
      * pitch outline
      * halfway-line
      * 2x 6-yard box
      * 2x 18-yard box
      * 2x penalty spots

    These 4 non-linear markings/points are added to the layout's shapes
    attribute:
      * centre circle
      * centre spot
      * 2x penalty box arcs
    """
    dimensions = PitchDimensions()
    fig = make_pitch_figure(dimensions)

    # linear markings
    assert len(fig.data) == 9

    # curved markings
    assert len(fig.layout.shapes) == 4


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
    """Heatmaps of different grid sizes can be added successfully"""
    dimensions = PitchDimensions()
    fig = make_pitch_figure(dimensions)
    num_data_on_plot = len(fig.data)

    random.seed(1234)
    data = np.array(
        [[random.random() for _ in range(length_grid)] for _ in range(width_grid)]
    )
    fig = add_heatmap(fig, data)

    assert len(fig.data) == num_data_on_plot + 1
