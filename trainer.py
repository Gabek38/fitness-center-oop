# trainer.py
# Defines the Trainer class.
# Encapsulates trainer data and schedule management.

class Trainer:
    """
    Represents a fitness center trainer.
    Replaces the plain dictionary used in the procedural version.
    """

    def __init__(self, trainer_id, name, specialty):
        self._id = trainer_id
        self._name = name
        self._specialty = specialty
        self._schedule = []

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def specialty(self):
        return self._specialty

    @property
    def schedule(self):
        return list(self._schedule)

    def add_schedule_slot(self, slot):
        """Add a single availability slot."""
        self._schedule.append(slot)

    def replace_schedule(self, new_schedule):
        """Replace the entire schedule."""
        self._schedule = list(new_schedule)

    def __str__(self):
        schedule_str = ", ".join(self._schedule) if self._schedule else "No availability"
        return f"[{self._id}] {self._name} - {self._specialty} (Schedule: {schedule_str})"