"""DotSmith Braille Embosser CAD models.

### Printed Parts list:
1. Left end cap, with motors and electronics.
2. Right end cap, with belt idlers.
3. Embossing head, with embossing pins (bottom side, has solenoid).
4. Embossing head, with anvil plate only (top side).
    * Uses M3 bolt heads as the strike surface.
6. Paper feed plate (left and right halves).
    * Has space for threaded rod to go all the way though to hold in place.
    * Acts as back side against paper feed rollers.
7. Paper feed rollers.

### BOM:
1. 3D printed parts
2. 8mm linear rods
3. 8mm linear bearings
4. GT2 belt
5. GT2 pulleys
6. 2x NEMA 17 stepper motors (to move the embossing head and anvil)
7. Threaded rod (to hold paper feed plate in place)
8. 608 bearings (as belt idlers)
9. M3 screw kit
10. Solenoid (to actuate embossing pins)
11. PCB (to control everything)
12. 12V power supply
13. O-rings for paper feed rollers.
14. NEMA 14 stepper motors (to move paper feed rollers).
15. IR sensors (to detect paper).
"""

from dataclasses import dataclass
from pathlib import Path

import build123d as bd
from build123d_ease import show
from loguru import logger


@dataclass
class Spec:
    """Specification for part1."""

    part1_radius: float = 20

    def __post_init__(self) -> None:
        """Post initialization checks."""
        assert self.part1_radius > 0, "part1_radius must be positive"


def make_part1(spec: Spec) -> bd.Part:
    """Create a CAD model of part1."""
    p = bd.Part(None)

    p += bd.Cylinder(radius=spec.part1_radius, height=20)

    return p


if __name__ == "__main__":
    parts = {
        "part1": show(make_part1(Spec())),
    }

    logger.info("Showing CAD model(s)")

    (export_folder := Path(__file__).parent.with_name("build")).mkdir(
        exist_ok=True
    )
    for name, part in parts.items():
        assert isinstance(
            part, bd.Part | bd.Solid | bd.Compound
        ), f"{name} is not an expected type ({type(part)})"
        if not part.is_manifold:
            logger.warning(f"Part '{name}' is not manifold")

        bd.export_stl(part, str(export_folder / f"{name}.stl"))
        bd.export_step(part, str(export_folder / f"{name}.step"))
