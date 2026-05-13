# member.py
# Defines the Member base class and subclasses.
# Demonstrates inheritance and polymorphism.

class Member:
    """
    Base class representing a fitness center member.
    Encapsulates member data using private attributes and properties.
    """

    BASE_CLASS_FEE = 10.0

    def __init__(self, member_id, name):
        self._id = member_id
        self._name = name
        self._active = True
        self._balance = 0.0

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def active(self):
        return self._active

    @property
    def balance(self):
        return self._balance

    @property
    def membership_type(self):
        return "base"

    def deactivate(self):
        """Mark this member as inactive."""
        self._active = False

    def add_charge(self, amount):
        """Add a charge to the member's balance."""
        self._balance += amount

    def record_payment(self, amount):
        """Subtract a payment from the member's balance."""
        self._balance -= amount

    def get_class_fee(self):
        """
        Returns the class enrollment fee.
        Overridden by subclasses to apply discounts (polymorphism).
        """
        return self.BASE_CLASS_FEE

    def __str__(self):
        status = "Active" if self._active else "Inactive"
        return (
            f"[{self._id}] {self._name} "
            f"({self.membership_type}, {status}) "
            f"Balance: ${self._balance:.2f}"
        )


class StudentMember(Member):
    """Student members receive a 50% discount on class fees."""

    @property
    def membership_type(self):
        return "student"

    def get_class_fee(self):
        return self.BASE_CLASS_FEE * 0.5


class FacultyMember(Member):
    """Faculty members receive a 25% discount on class fees."""

    @property
    def membership_type(self):
        return "faculty"

    def get_class_fee(self):
        return self.BASE_CLASS_FEE * 0.75


class CommunityMember(Member):
    """Community members pay the full base fee."""

    @property
    def membership_type(self):
        return "community"

    def get_class_fee(self):
        return self.BASE_CLASS_FEE


def create_member(member_id, name, membership_type):
    """
    Factory function: returns the correct Member subclass
    based on the membership_type string.
    """
    membership_type = membership_type.strip().lower()
    if membership_type == "student":
        return StudentMember(member_id, name)
    elif membership_type == "faculty":
        return FacultyMember(member_id, name)
    else:
        if membership_type not in ("community",):
            print("Unknown membership type. Defaulting to 'community'.")
        return CommunityMember(member_id, name)