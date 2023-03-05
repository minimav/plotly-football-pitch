"""Configuration for the dimensions/orientation of a football pitch to plot."""
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple


@dataclass
class PitchDimensions:
    """Dimensions for a football pitch plot.

    All units are in metres. Length refers to the longer pitch dimension, which
    for a horizontal pitch will be the plot's x-axis. Width refers to the
    shorter pitch dimension, which for a horizontal pitch will be the plot's
    y-axis. The axes will be reversed for a vertical pitch.

    The origin is the bottom left hand corner of the pitch.

    """

    pitch_width_metres: int = 68
    pitch_length_metres: int = 105

    @property
    def pitch_mid_length_metres(self):
        """Distance of the centre line in metres from goal lines."""
        return self.pitch_length_metres / 2

    @property
    def pitch_mid_width_metres(self):
        """Distance in metres from side lines to the centre spot."""
        return self.pitch_width_metres / 2

    @property
    def penalty_box_length_metres(self):
        """Penalty box length in metres (18 yards in metres)."""
        return 18 / 1.09361

    @property
    def penalty_box_width_metres(self):
        """Width of the penalty box in metres."""
        return self.pitch_width_metres * 0.6

    @property
    def penalty_box_width_max_metres(self):
        """Metres from the bottom touchline to top of penalty box."""
        outside_box_metres = self.pitch_width_metres - self.penalty_box_width_metres
        return self.pitch_width_metres - outside_box_metres / 2

    @property
    def penalty_box_width_min_metres(self):
        """Metres from the bottom touchline to bottom of penalty box."""
        outside_box_metres = self.pitch_width_metres - self.penalty_box_width_metres
        return outside_box_metres / 2

    @property
    def six_yard_box_length_metres(self):
        """Six yard box length in metres (6 yards in metres)."""
        return self.penalty_box_length_metres / 3

    @property
    def six_yard_box_width_metres(self):
        """Width of the six yard box in metres."""
        return self.pitch_width_metres * 0.3

    @property
    def six_yard_box_width_max_metres(self):
        """Metres from the bottom touchline to top of six yard box."""
        outside_box_metres = self.pitch_width_metres - self.six_yard_box_width_metres
        return self.pitch_width_metres - outside_box_metres / 2

    @property
    def six_yard_box_width_min_metres(self):
        """Metres from the bottom touchline to bottom of six yard box."""
        outside_box_metres = self.pitch_width_metres - self.six_yard_box_width_metres
        return outside_box_metres / 2

    @property
    def penalty_spot_length_metres(self):
        """Penalty spot distance from goal line (12 yards in metres)."""
        return 2 * self.penalty_box_length_metres / 3

    @property
    def centre_circle_radius_metres(self):
        """Radius of the centre circle in metres."""
        return self.pitch_length_metres / 10


class PitchOrientation(Enum):
    """Orientation of a pitch.

    Horizontal means that the plot's x-axis will represent the longer dimension
    of the pitch, and the plot's y-axis will represent the shorter dimension of
    the pitch. The axes are reversed for a vertically oriented pitch.
    """

    HORIZONTAL = 0
    VERTICAL = 1

    def switch_axes_if_required(
        self,
        coordinate_data: dict,
        keys_to_switch: Optional[List[Tuple[str, str]]] = None,
    ) -> dict:
        """Switch axes of data for vertically oriented pitches.

        Args:
            coordinate_data (dict): Data to show on the plot. Keys will refer
                to plot axes e.g. 'x', 'y', 'x0' or 'y1'.
            keys_to_switch (Optional[list[tuple[str, str]]]): Pairs for keys in
                `coordinate_data` to swap for a vertically oriented pitch.
                Defaults to [('x', 'y')], which will work for plotting lines
                and scatter points. Only keys present in some tuple will be
                included in the output, therefore no additional key-value pairs
                should be included in `coordinate_data`.

        Returns:
            dict: Dictionary with coordinate data whose axes have been switched
                for a vertically oriented pitch.
        """
        if keys_to_switch is None:
            keys_to_switch = [("x", "y")]

        if self == PitchOrientation.HORIZONTAL:
            return coordinate_data
        else:
            switched_coordinate_data = {}
            for key_1, key_2 in keys_to_switch:
                switched_coordinate_data[key_1] = coordinate_data[key_2]
                switched_coordinate_data[key_2] = coordinate_data[key_1]
            return switched_coordinate_data
