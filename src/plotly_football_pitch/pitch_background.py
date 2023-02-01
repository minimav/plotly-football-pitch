"""Helpers for adding background colours to a pitch plot."""
from typing import List, Protocol
import itertools

import plotly.graph_objects as go

from plotly_football_pitch.pitch_dimensions import PitchDimensions


class PitchBackground(Protocol):
    def add_background(
        self,
        fig: go.Figure,
        dimensions: PitchDimensions,
    ) -> go.Figure:
        """Add background to a pitch.

        Args:
            fig (plotly.graph_objects.Figure): Figure with pitch markings
                already drawn.
            dimensions (PitchDimensions): Dimensions of the pitch.

        Returns:
            plotly.graph_objects.Figure
        """


class SingleColourBackground(PitchBackground):
    """Add a single colour background to a fooball pitch."""

    def __init__(self, colour: str):
        """Add a single colour background to a fooball pitch.

        Args:
            colour (str): Colour for the background.
        """
        self.colour = colour

    def add_background(self, fig: go.Figure, dimensions: PitchDimensions) -> go.Figure:
        """Add a single-coloured background to a pitch.

        Args:
            fig (plotly.graph_objects.Figure): Figure with pitch markings
                already drawn.
            dimensions (PitchDimensions): Dimensions of the pitch.

        Returns:
            plotly.graph_objects.Figure
        """
        return fig.add_hrect(
            y0=0,
            y1=dimensions.pitch_width_metres,
            fillcolor=self.colour,
            layer="below",
        )


class AttackVsDefenceBackground(PitchBackground):
    """Colour each half of the pitch for a team, left=attack, right=defence."""

    def __init__(self, attack_colour: str, defence_colour: str):
        """Colour each half of the pitch per team, left=attack, right=defence.

        Args:
            attack_colour (str): Colour for the attacking team's half, the left
                side of the pitch.
            defence_colour (str): Colour for the defending team's half, the
                right side of the pitch.
        """
        self.attack_colour = attack_colour
        self.defence_colour = defence_colour

    def add_background(self, fig: go.Figure, dimensions: PitchDimensions) -> go.Figure:
        """Add attacking and defending team backgrounds to a pitch.

        Follows the standard convention for horizontal pitches whereby the left
        hand side represents the attacking team and the right hand side the
        defending team.

        Args:
            fig (plotly.graph_objects.Figure): Figure with pitch markings
                already drawn.
            dimensions (PitchDimensions): Dimensions of the pitch.

        Returns:
            plotly.graph_objects.Figure
        """
        fig = fig.add_shape(
            type="rect",
            y0=0,
            y1=dimensions.pitch_width_metres,
            x0=0,
            x1=dimensions.pitch_mid_length_metres,
            line_color=self.attack_colour,
            fillcolor=self.attack_colour,
            layer="below",
        )
        fig = fig.add_shape(
            type="rect",
            y0=0,
            y1=dimensions.pitch_width_metres,
            x0=dimensions.pitch_mid_length_metres,
            x1=dimensions.pitch_length_metres,
            line_color=self.defence_colour,
            fillcolor=self.defence_colour,
            layer="below",
        )
        return fig


class VerticalStripesBackground(PitchBackground):
    """Vertical stripes using specified colour cycle."""

    def __init__(self, colours: List[str], num_stripes: int = 10):
        """Vertical stripes using specified colour cycle.

        Args:
            colours (list[str]): A list of colours to cycle through for the
                stripes.
            num_stripes (int): Number of vertical stripes to use, default 10.
        """
        self.colours = colours
        self.num_stripes = num_stripes

    def add_background(
        self,
        fig: go.Figure,
        dimensions: PitchDimensions,
    ) -> go.Figure:
        """Add vertically-striped background to a pitch.

        Args:
            fig (plotly.graph_objects.Figure): Figure with pitch markings
                already drawn.
            dimensions (PitchDimensions): Dimensions of the pitch.

        Returns:
            plotly.graph_objects.Figure
        """
        stripe_metres = dimensions.pitch_length_metres / self.num_stripes
        colour_cycle = itertools.cycle(self.colours)

        for index, colour in zip(range(self.num_stripes), colour_cycle):
            x0 = index * stripe_metres
            x1 = x0 + stripe_metres
            fig = fig.add_shape(
                type="rect",
                y0=0,
                y1=dimensions.pitch_width_metres,
                x0=x0,
                x1=x1,
                line_color=colour,
                fillcolor=colour,
                layer="below",
            )
        return fig


class HorizontalStripesBackground(PitchBackground):
    """Horizontal stripes using specified colour cycle."""

    def __init__(self, colours: List[str], num_stripes: int = 10):
        """Horizontal stripes using specified colour cycle.

        Args:
            colours (list[str]): A list of colours to cycle through for the
                stripes.
            num_stripes (int): Number of horizontal stripes to use, default 10.
        """
        self.colours = colours
        self.num_stripes = num_stripes

    def add_background(self, fig: go.Figure, dimensions: PitchDimensions) -> go.Figure:
        """Add vertically-striped background to a pitch.

        Args:
            fig (plotly.graph_objects.Figure): Figure with pitch markings
                already drawn.
            dimensions (PitchDimensions): Dimensions of the pitch.

        Returns:
            plotly.graph_objects.Figure
        """
        stripe_metres = dimensions.pitch_width_metres / self.num_stripes
        colour_cycle = itertools.cycle(self.colours)

        for index, colour in zip(range(self.num_stripes), colour_cycle):
            y0 = index * stripe_metres
            y1 = y0 + stripe_metres
            fig = fig.add_shape(
                type="rect",
                y0=y0,
                y1=y1,
                x0=0,
                x1=dimensions.pitch_length_metres,
                line_color=colour,
                fillcolor=colour,
                layer="below",
            )
        return fig


class ChequeredBackground(PitchBackground):
    """Chequered pitch using two alternating colours."""

    def __init__(
        self,
        colours: List[str],
        num_horizontal_stripes: int = 10,
        num_vertical_stripes: int = 10,
    ):
        """Chequered pitch using two alternating colours.

        Args:
            colours (list[str]): A list of two colours to alternate for the
                chequered effect.
            num_horizontal_stripes (int): Number of horizontal stripes in the
                chequered effect (i.e. number of rows).
            num_vertical_stripes (int): Number of vertical stripes in the
                chequered effect (i.e. number of columns).

        Raises:
            ValueError: If `colours` does not have length 2.
        """
        if len(colours) != 2:
            raise ValueError(
                f"{self.__class__.__name__} expects `colours` to have length 2"
                f", input was {colours}."
            )
        self.colours = colours
        self.num_horizontal_stripes = num_horizontal_stripes
        self.num_vertical_stripes = num_vertical_stripes

    def add_background(self, fig: go.Figure, dimensions: PitchDimensions) -> go.Figure:
        """Add vertically-striped background to a pitch.

        Args:
            fig (plotly.graph_objects.Figure): Figure with pitch markings
                already drawn.
            dimensions (PitchDimensions): Dimensions of the pitch.

        Returns:
            plotly.graph_objects.Figure
        """
        stripe_height_metres = (
            dimensions.pitch_width_metres / self.num_horizontal_stripes
        )
        stripe_width_metres = dimensions.pitch_length_metres / self.num_vertical_stripes

        for row_index in range(self.num_horizontal_stripes):
            colour_cycle = itertools.cycle(self.colours)
            if row_index % 2 == 1:
                # alternate first colour per row
                next(colour_cycle)

            column_iterator = zip(
                range(self.num_vertical_stripes),
                colour_cycle,
            )
            for column_index, colour in column_iterator:
                x0 = column_index * stripe_width_metres
                x1 = x0 + stripe_width_metres
                y0 = row_index * stripe_height_metres
                y1 = y0 + stripe_height_metres
                fig = fig.add_shape(
                    type="rect",
                    y0=y0,
                    y1=y1,
                    x0=x0,
                    x1=x1,
                    line_color=colour,
                    fillcolor=colour,
                    layer="below",
                )
        return fig
