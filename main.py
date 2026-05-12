class Member:
    """Base class demonstrating Encapsulation."""
    def __init__(self, member_id, name):
        self._member_id = member_id  # Protected attribute (Encapsulation)
        self.name = name

    def get_details(self):
        """Standard display for a basic member."""
        return f"Member ID: {self._member_id} | Name: {self.name}"