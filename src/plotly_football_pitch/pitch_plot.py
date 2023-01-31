"""Create a plotly figure of a football pitch."""
from typing import Optional

try:
    from typing import TypeAlias  # type:ignore
except ImportError:
    from typing_extensions import TypeAlias

import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from plotly_football_pitch.pitch_dimensions import PitchDimensions


PlotlyFigure: TypeAlias = plotly.graph_objs._figure.Figure


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
        plotly.graph_objs._figure.Figure

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
    pitch_colour: Optional[str] = None,
    figure_width_pixels: int = 800,
    figure_height_pixels: int = 600,
) -> PlotlyFigure:
    """Create a plotly figure of a football pitch with markings.

    Args:
        dimensions (PitchDimensions): Dimensions of the pitch to plot.
        marking_colour (str): Colour of the pitch markings, default "black".
        marking_width (int): Width of the pitch markings, default 4.
        pitch_colour (Optional[str]): Background colour of the pitch. The
            default None results in a transparent background.
        figure_width_pixels (int): Width of the figure, default 800. This
            corresponds to the long axis of the pitch (pitch length).
        figure_height_pixels (int): Height of the figure, default 600. This
            corresponds to the short axis of the pitch (pitch width).

    Returns:
        plotly.graph_objs._figure.Figure
    """
    pitch_marking_style = {
        "mode": "lines",
        "line": {"color": marking_colour, "width": marking_width},
        "hoverinfo": "skip",
    }
    spot_style = {
        "mode": "markers",
        "line": {"color": marking_colour, "width": marking_width},
        "hoverinfo": "skip",
    }

    pitch_markings = [
        # touchline
        go.Scatter(
            x=[0, dimensions.pitch_length_metres, dimensions.pitch_length_metres, 0, 0],
            y=[0, 0, dimensions.pitch_width_metres, dimensions.pitch_width_metres, 0],
            **pitch_marking_style,
        ),
        # halfway line
        go.Scatter(
            x=[dimensions.pitch_mid_length_metres, dimensions.pitch_mid_length_metres],
            y=[0, dimensions.pitch_width_metres],
            **pitch_marking_style,
        ),
        # penalty boxes
        go.Scatter(
            x=[
                0,
                dimensions.penalty_box_length_metres,
                dimensions.penalty_box_length_metres,
                0,
            ],
            y=[
                dimensions.penalty_box_width_min_metres,
                dimensions.penalty_box_width_min_metres,
                dimensions.penalty_box_width_max_metres,
                dimensions.penalty_box_width_max_metres,
            ],
            **pitch_marking_style,
        ),
        go.Scatter(
            x=[
                dimensions.pitch_length_metres,
                dimensions.pitch_length_metres - dimensions.penalty_box_length_metres,
                dimensions.pitch_length_metres - dimensions.penalty_box_length_metres,
                dimensions.pitch_length_metres,
            ],
            y=[
                dimensions.penalty_box_width_min_metres,
                dimensions.penalty_box_width_min_metres,
                dimensions.penalty_box_width_max_metres,
                dimensions.penalty_box_width_max_metres,
            ],
            **pitch_marking_style,
        ),
        # six yard boxes
        go.Scatter(
            x=[
                0,
                dimensions.six_yard_box_length_metres,
                dimensions.six_yard_box_length_metres,
                0,
            ],
            y=[
                dimensions.six_yard_box_width_min_metres,
                dimensions.six_yard_box_width_min_metres,
                dimensions.six_yard_box_width_max_metres,
                dimensions.six_yard_box_width_max_metres,
            ],
            **pitch_marking_style,
        ),
        go.Scatter(
            x=[
                dimensions.pitch_length_metres,
                dimensions.pitch_length_metres - dimensions.six_yard_box_length_metres,
                dimensions.pitch_length_metres - dimensions.six_yard_box_length_metres,
                dimensions.pitch_length_metres,
            ],
            y=[
                dimensions.six_yard_box_width_min_metres,
                dimensions.six_yard_box_width_min_metres,
                dimensions.six_yard_box_width_max_metres,
                dimensions.six_yard_box_width_max_metres,
            ],
            **pitch_marking_style,
        ),
        # penalty spots
        go.Scatter(
            x=[dimensions.penalty_spot_length_metres],
            y=[dimensions.pitch_mid_width_metres],
            **spot_style,
        ),
        go.Scatter(
            x=[dimensions.pitch_length_metres - dimensions.penalty_spot_length_metres],
            y=[dimensions.pitch_mid_width_metres],
            **spot_style,
        ),
        # centre spot
        go.Scatter(
            x=[dimensions.pitch_mid_length_metres],
            y=[dimensions.pitch_mid_width_metres],
            **spot_style,
        ),
    ]

    fig = make_subplots()
    for markings in pitch_markings:
        fig.add_trace(markings)

    # centre circle
    fig.add_shape(
        type="circle",
        xref="x",
        yref="y",
        x0=dimensions.pitch_mid_length_metres + dimensions.centre_circle_radius_metres,
        y0=dimensions.pitch_mid_width_metres + dimensions.centre_circle_radius_metres,
        x1=dimensions.pitch_mid_length_metres - dimensions.centre_circle_radius_metres,
        y1=dimensions.pitch_mid_width_metres - dimensions.centre_circle_radius_metres,
        line=pitch_marking_style["line"],
    )

    # penalty box arcs
    path = make_ellipse_arc_svg_path(
        x_centre=dimensions.penalty_spot_length_metres,
        y_centre=dimensions.pitch_mid_width_metres,
        a=dimensions.penalty_spot_length_metres,
        b=dimensions.penalty_spot_length_metres,
        start_angle=-np.pi / 3,
        end_angle=np.pi / 3,
        num_points=60,
    )
    fig.add_shape(
        type="path",
        path=path,
        line=pitch_marking_style["line"],
    )
    path = make_ellipse_arc_svg_path(
        x_centre=dimensions.pitch_length_metres - dimensions.penalty_spot_length_metres,
        y_centre=dimensions.pitch_mid_width_metres,
        a=dimensions.penalty_spot_length_metres,
        b=dimensions.penalty_spot_length_metres,
        start_angle=2 * np.pi / 3,
        end_angle=4 * np.pi / 3,
        num_points=60,
    )
    fig.add_shape(
        type="path",
        path=path,
        line=pitch_marking_style["line"],
    )
    fig.add_hrect(
        y0=0,
        y1=dimensions.pitch_width_metres,
        fillcolor=pitch_colour,
        layer="below",
    )

    fig.update_layout(
        height=figure_height_pixels,
        width=figure_width_pixels,
        xaxis_range=[0, dimensions.pitch_length_metres],
        yaxis_range=[0, dimensions.pitch_width_metres],
    )
    fig.update_layout(showlegend=False)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig


def add_heatmap(fig: PlotlyFigure, data: np.ndarray) -> PlotlyFigure:
    """Add a heatmap to an existing figure.

    Args:
        fig (plotly.graph_objs._figure.Figure): Figure on which to add heatmap.
            Expected to have axis ranges directly set so that
            `fig.layout.xaxis.range` and `fig.layout.yaxis.range` are not None.
        data (np.ndarray):
            2-dimensional arrays of values to plot on the figure. Number of
            grid squares in each dimension will be inferred from the shape of
            this array.

    Returns:
        plotly.graph_objs._figure.Figure
    """
    _, pitch_length_metres = fig.layout.xaxis.range
    _, pitch_width_metres = fig.layout.yaxis.range

    dx = pitch_length_metres / data.shape[1]
    dy = pitch_width_metres / data.shape[0]
    heatmap = go.Heatmap(
        z=data,
        dx=dx,
        dy=dy,
        y0=dy / 2,
        x0=dx / 2,
        colorscale=px.colors.sequential.Reds,
        hovertemplate="%{z}<extra></extra>",
    )
    fig.add_trace(heatmap)
    return fig
