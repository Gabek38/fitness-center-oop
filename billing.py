# billing.py
# Handles all billing operations.
# Separated into its own class to follow the Single Responsibility Principle.

class BillingService:
    """
    Manages charges and payments for fitness center members.
    Separating billing from member data is an OOP best practice.
    """

    @staticmethod
    def charge_member(member, amount):
        """Add a manual charge to a member's balance."""
        if amount <= 0:
            print("Charge amount must be positive.")
            return False
        member.add_charge(amount)
        print(f"Added ${amount:.2f} to {member.name}'s balance.")
        return True

    @staticmethod
    def record_payment(member, amount):
        """Record a payment from a member."""
        if amount <= 0:
            print("Payment amount must be positive.")
            return False
        member.record_payment(amount)
        print(f"Recorded payment of ${amount:.2f} from {member.name}.")
        return True

    @staticmethod
    def charge_class_enrollment(member):
        """
        Charge a member for enrolling in a class.
        Calls member.get_class_fee() — polymorphism handles the discount
        automatically based on the member's subclass type.
        No if/elif chain needed here.
        """
        fee = member.get_class_fee()
        member.add_charge(fee)
        print(
            f"Charged ${fee:.2f} for class enrollment "
            f"(base ${member.BASE_CLASS_FEE:.2f}, type: {member.membership_type})."
        )
        return fee