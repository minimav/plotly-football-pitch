"""Configuration for the dimensions of a football pitch to plot."""
from dataclasses import dataclass


@dataclass
class PitchDimensions:
    """Dimensions for a horizontal football pitch plot.

    All units are in metres. Length refers to the longer pitch dimension, which
    will be the plot's x-axis. Width refers to the shorter pitch dimension,
    which will be the plot's y-axis. The origin is the bottom left hand corner
    of the pitch.

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
