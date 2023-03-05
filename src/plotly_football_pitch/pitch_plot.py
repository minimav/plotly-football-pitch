"""Create a plotly figure of a football pitch."""
from typing import Optional

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from plotly_football_pitch.pitch_background import PitchBackground
from plotly_football_pitch.pitch_dimensions import PitchDimensions, PitchOrientation


def make_ellipse_arc_svg_path(
    x_centre: float = 0.0,
    y_centre: float = 0.0,
    a: float = 1.0,
    b: float = 1.0,
    start_angle: float = 0.0,
    end_angle: float = 2 * np.pi,
    num_points: int = 100,
    closed: bool = False,
) -> str:
    """Create an SVG path for an arc of an ellipse.

    Defaults produce the full perimeter of a circle of radius 1 centred on the
    origin.

    Args:
        x_centre (float): x-coordinate of the centre of the ellipse, default
            0.0.
        y_centre (float): y-coordinate of the centre of the ellipse, default
            0.0.
        a (float): 'Radius' of the ellipse in the direction of the x-axis,
            default 1.0.
        b (float): 'Radius' of the ellipse in the direction of the y-axis,
            default 1.0.
        start_angle (float): Angle in radians from which the arc should start
            being drawn in an anticlockwise direction, default 0.
        end_angle (float): Angle in radians at which the arc should terminate,
            being drawn in an anticlockwise direction, default 2 * pi.
        num_points (int): Number of points in the interpolation of the arc,
            default 100.
        closed (bool): Whether the arc should be closed, default False.

    Returns:
        plotly.graph_objects.Figure

    .. _Plotly forums
       https://community.plotly.com/t/arc-shape-with-path/7205/4
    """
    t = np.linspace(start_angle, end_angle, num_points)
    xs = x_centre + a * np.cos(t)
    ys = y_centre + b * np.sin(t)
    coords = [f"{x}, {y}" for x, y in zip(xs, ys)]
    path = f"M {'L'.join(coords)}"
    if closed:
        path += " Z"
    return path


def make_pitch_figure(
    dimensions: PitchDimensions,
    marking_colour: str = "black",
    marking_width: int = 4,
    pitch_background: Optional[PitchBackground] = None,
    figure_width_pixels: int = 800,
    figure_height_pixels: int = 600,
    orientation: PitchOrientation = PitchOrientation.HORIZONTAL,
) -> go.Figure:
    """Create a plotly figure of a football pitch with markings.

    Some markings which appear in both team's halves e.g. penalty box arc, are
    defined in terms of the attacking team and the defending team. For a
    horizontally oriented pitch the attacking team's half is the left hand one,
    while for a vertically oriented one their half is the bottom one.

    Args:
        dimensions (PitchDimensions): Dimensions of the pitch to plot.
        marking_colour (str): Colour of the pitch markings, default "black".
        marking_width (int): Width of the pitch markings, default 4.
        pitch_background (Optional[PitchBackground]): Strategy for plotting a
            background colour to the pitch. The default of None results in a
            transparent background.
        figure_width_pixels (int): Width of the figure, default 800. This
            corresponds to the long axis of the pitch (pitch length).
        figure_height_pixels (int): Height of the figure, default 600. This
            corresponds to the short axis of the pitch (pitch width).
        orientation (PitchOrientation): Orientation of the pitch, defaults to
            a horizontal pitch.

    Returns:
        plotly.graph_objects.Figure
    """
    pitch_marking_style = {
        "mode": "lines",
        "line": {"color": marking_colour, "width": marking_width},
        "hoverinfo": "skip",
        "showlegend": False,
    }
    spot_style = {
        "mode": "markers",
        "line": {"color": marking_colour},
        "hoverinfo": "skip",
        "showlegend": False,
    }

    touchline = {
        "x": [0, dimensions.pitch_length_metres, dimensions.pitch_length_metres, 0, 0],
        "y": [0, 0, dimensions.pitch_width_metres, dimensions.pitch_width_metres, 0],
    }

    halfway_line = {
        "x": [dimensions.pitch_mid_length_metres, dimensions.pitch_mid_length_metres],
        "y": [0, dimensions.pitch_width_metres],
    }

    # attacking team's half is left for horizontal pitches (bottom for
    # vertical after rotation)
    penalty_boxes = {
        "attacking_team": {
            "x": [
                0,
                dimensions.penalty_box_length_metres,
                dimensions.penalty_box_length_metres,
                0,
            ],
            "y": [
                dimensions.penalty_box_width_min_metres,
                dimensions.penalty_box_width_min_metres,
                dimensions.penalty_box_width_max_metres,
                dimensions.penalty_box_width_max_metres,
            ],
        },
        "defending_team": {
            "x": [
                dimensions.pitch_length_metres,
                dimensions.pitch_length_metres - dimensions.penalty_box_length_metres,
                dimensions.pitch_length_metres - dimensions.penalty_box_length_metres,
                dimensions.pitch_length_metres,
            ],
            "y": [
                dimensions.penalty_box_width_min_metres,
                dimensions.penalty_box_width_min_metres,
                dimensions.penalty_box_width_max_metres,
                dimensions.penalty_box_width_max_metres,
            ],
        },
    }

    six_yard_boxes = {
        "attacking_team": {
            "x": [
                0,
                dimensions.six_yard_box_length_metres,
                dimensions.six_yard_box_length_metres,
                0,
            ],
            "y": [
                dimensions.six_yard_box_width_min_metres,
                dimensions.six_yard_box_width_min_metres,
                dimensions.six_yard_box_width_max_metres,
                dimensions.six_yard_box_width_max_metres,
            ],
        },
        "defending_team": {
            "x": [
                dimensions.pitch_length_metres,
                dimensions.pitch_length_metres - dimensions.six_yard_box_length_metres,
                dimensions.pitch_length_metres - dimensions.six_yard_box_length_metres,
                dimensions.pitch_length_metres,
            ],
            "y": [
                dimensions.six_yard_box_width_min_metres,
                dimensions.six_yard_box_width_min_metres,
                dimensions.six_yard_box_width_max_metres,
                dimensions.six_yard_box_width_max_metres,
            ],
        },
    }

    penalty_spots = {
        "attacking_team": {
            "x": [dimensions.penalty_spot_length_metres],
            "y": [dimensions.pitch_mid_width_metres],
        },
        "defending_team": {
            "x": [
                dimensions.pitch_length_metres - dimensions.penalty_spot_length_metres
            ],
            "y": [dimensions.pitch_mid_width_metres],
        },
    }

    centre_spot = {
        "x": [dimensions.pitch_mid_length_metres],
        "y": [dimensions.pitch_mid_width_metres],
    }

    pitch_marking_coordinates_with_style = [
        (touchline, pitch_marking_style),
        (halfway_line, pitch_marking_style),
        (penalty_boxes["attacking_team"], pitch_marking_style),
        (penalty_boxes["defending_team"], pitch_marking_style),
        (six_yard_boxes["attacking_team"], pitch_marking_style),
        (six_yard_boxes["defending_team"], pitch_marking_style),
        (penalty_spots["attacking_team"], spot_style),
        (penalty_spots["defending_team"], spot_style),
        (centre_spot, spot_style),
    ]

    pitch_markings = [
        go.Scatter(
            **orientation.switch_axes_if_required(marking_coordinates),
            **style,
        )
        for marking_coordinates, style in pitch_marking_coordinates_with_style
    ]

    fig = make_subplots()
    for markings in pitch_markings:
        fig.add_trace(markings)

    centre_circle = {
        "x0": dimensions.pitch_mid_length_metres
        + dimensions.centre_circle_radius_metres,
        "y0": dimensions.pitch_mid_width_metres
        + dimensions.centre_circle_radius_metres,
        "x1": dimensions.pitch_mid_length_metres
        - dimensions.centre_circle_radius_metres,
        "y1": dimensions.pitch_mid_width_metres
        - dimensions.centre_circle_radius_metres,
    }
    fig.add_shape(
        type="circle",
        xref="x",
        yref="y",
        line=pitch_marking_style["line"],
        name=None,
        **orientation.switch_axes_if_required(
            centre_circle, keys_to_switch=[("x0", "y0"), ("x1", "y1")]
        ),
    )

    penalty_box_arcs = {
        "attacking_team": {
            "x_centre": dimensions.penalty_spot_length_metres,
            "y_centre": dimensions.pitch_mid_width_metres,
        },
        "defending_team": {
            "x_centre": dimensions.pitch_length_metres
            - dimensions.penalty_spot_length_metres,
            "y_centre": dimensions.pitch_mid_width_metres,
        },
    }
    start_angle = {
        "attacking_team": {
            PitchOrientation.HORIZONTAL: -np.pi / 3,
            PitchOrientation.VERTICAL: np.pi / 6,
        },
        "defending_team": {
            PitchOrientation.HORIZONTAL: 2 * np.pi / 3,
            PitchOrientation.VERTICAL: -5 * np.pi / 6,
        },
    }
    end_angle = {
        "attacking_team": {
            PitchOrientation.HORIZONTAL: np.pi / 3,
            PitchOrientation.VERTICAL: 5 * np.pi / 6,
        },
        "defending_team": {
            PitchOrientation.HORIZONTAL: 4 * np.pi / 3,
            PitchOrientation.VERTICAL: -np.pi / 6,
        },
    }

    path = make_ellipse_arc_svg_path(
        **orientation.switch_axes_if_required(
            penalty_box_arcs["attacking_team"],
            keys_to_switch=[("x_centre", "y_centre")],
        ),
        start_angle=start_angle["attacking_team"][orientation],
        end_angle=end_angle["attacking_team"][orientation],
        a=dimensions.penalty_spot_length_metres,
        b=dimensions.penalty_spot_length_metres,
        num_points=60,
    )
    fig.add_shape(
        type="path",
        path=path,
        line=pitch_marking_style["line"],
        name=None,
    )
    path = make_ellipse_arc_svg_path(
        **orientation.switch_axes_if_required(
            penalty_box_arcs["defending_team"],
            keys_to_switch=[("x_centre", "y_centre")],
        ),
        start_angle=start_angle["defending_team"][orientation],
        end_angle=end_angle["defending_team"][orientation],
        a=dimensions.penalty_spot_length_metres,
        b=dimensions.penalty_spot_length_metres,
        num_points=60,
    )
    fig.add_shape(
        type="path",
        path=path,
        line=pitch_marking_style["line"],
        name=None,
    )

    if pitch_background is not None:
        fig = pitch_background.add_background(fig, dimensions, orientation)

    axes_ranges = {
        "xaxis_range": [0, dimensions.pitch_length_metres],
        "yaxis_range": [0, dimensions.pitch_width_metres],
    }
    fig.update_layout(
        height=figure_height_pixels,
        width=figure_width_pixels,
        **orientation.switch_axes_if_required(
            axes_ranges, keys_to_switch=[("xaxis_range", "yaxis_range")]
        ),
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig


def add_heatmap(fig: go.Figure, data: np.ndarray, **kwargs) -> go.Figure:
    """Add a heatmap to an existing figure.

    Args:
        fig (plotly.graph_objects.Figure): Figure on which to add heatmap.
            Expected to have axis ranges directly set so that
            `fig.layout.xaxis.range` and `fig.layout.yaxis.range` are not None.
        data (np.ndarray):
            2-dimensional arrays of values to plot on the figure. Number of
            grid squares in each dimension will be inferred from the shape of
            this array. The i'th row of the array corresponds to the i'th row
            of the grid on the pitch starting from the bottom, while the j'th
            column of the array corresponds to the j'th column of the grid
            starting from the left hand side. Thus, in particular, `data[0, 0]`
            corresponds to the bottom left grid square.

    Returns:
        plotly.graph_objects.Figure
    """
    if "colorscale" not in kwargs:
        kwargs["colorscale"] = px.colors.sequential.Reds
    if "hovertemplate" not in kwargs:
        kwargs["hovertemplate"] = "%{z}<extra></extra>"

    _, plot_width = fig.layout.xaxis.range
    _, plot_height = fig.layout.yaxis.range

    dx = plot_width / data.shape[1]
    dy = plot_height / data.shape[0]
    heatmap = go.Heatmap(z=data, dx=dx, dy=dy, y0=dy / 2, x0=dx / 2, **kwargs)
    fig.add_trace(heatmap)
    return fig
