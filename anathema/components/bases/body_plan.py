from __future__ import annotations

from ecstremity import Component


class BodyPlan(Component):

    def __init__(
            self,
            head_count: int,
            eye_count: int,
            arm_count: int,
            leg_count: int,
            symmetric: bool
        ) -> None:
        self.head_count = head_count
        self.eye_count = eye_count * head_count
        self.arm_count = arm_count
        self.leg_count = leg_count
        self.symmetric = symmetric
