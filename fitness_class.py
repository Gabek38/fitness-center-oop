# fitness_class.py
# Defines the FitnessClass class.
# Encapsulates class data and enrollment logic.

class FitnessClass:
    """
    Represents a fitness class offered at the center.
    Replaces the plain dictionary used in the procedural version.
    """

    VALID_DIFFICULTIES = ("beginner", "intermediate", "advanced")

    def __init__(self, class_id, name, difficulty, capacity):
        self._id = class_id
        self._name = name
        self._capacity = capacity
        self._enrolled_ids = []

        difficulty = difficulty.strip().lower()
        if difficulty not in self.VALID_DIFFICULTIES:
            print("Unknown difficulty. Defaulting to 'beginner'.")
            difficulty = "beginner"
        self._difficulty = difficulty

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def difficulty(self):
        return self._difficulty

    @property
    def capacity(self):
        return self._capacity

    @property
    def enrolled_ids(self):
        return list(self._enrolled_ids)

    @property
    def enrollment_count(self):
        return len(self._enrolled_ids)

    def is_full(self):
        return len(self._enrolled_ids) >= self._capacity

    def is_enrolled(self, member_id):
        return member_id in self._enrolled_ids

    def enroll(self, member_id):
        """Enroll a member by ID. Returns True on success."""
        if self.is_full() or self.is_enrolled(member_id):
            return False
        self._enrolled_ids.append(member_id)
        return True

    def __str__(self):
        return (
            f"[{self._id}] {self._name} "
            f"({self._difficulty}, capacity {self._capacity}, "
            f"enrolled {self.enrollment_count})"
        )