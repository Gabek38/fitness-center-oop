# fitness_center.py
# The FitnessCenter class is the central controller for the application.
# Replaces all global variables and scattered functions from the procedural version.
# Acts as a Facade: one clean interface that manages members, classes, and trainers.

from member import create_member
from fitness_class import FitnessClass
from trainer import Trainer
from billing import BillingService
from utils import read_int, read_nonempty, pause


class FitnessCenter:
    """
    Central management class for the Campus Fitness Center.
    All data lives here as private instance attributes instead of global variables.
    """

    def __init__(self, name="Campus Fitness Center"):
        self._name = name
        self._members = []
        self._classes = []
        self._trainers = []
        self._next_member_id = 1
        self._next_class_id = 1
        self._next_trainer_id = 1
        self._billing = BillingService()

    # --- Member management ---

    def add_member(self):
        print("\n=== Add New Member ===")
        name = read_nonempty("Name: ")
        print("Membership types: student, faculty, community")
        membership_type = input("Membership type: ").strip().lower()
        member = create_member(self._next_member_id, name, membership_type)
        self._members.append(member)
        print(f"Member added with id {self._next_member_id}")
        self._next_member_id += 1

    def list_members(self, show_details=True):
        print("\n=== Members ===")
        if not self._members:
            print("No members found.")
        for m in self._members:
            if show_details:
                print(m)
            else:
                print(f"[{m.id}] {m.name}")
        print()

    def find_member_by_id(self, member_id):
        for m in self._members:
            if m.id == member_id:
                return m
        return None

    def deactivate_member(self):
        print("\n=== Deactivate Member ===")
        self.list_members(show_details=False)
        mid = read_int("Enter member id to deactivate: ")
        member = self.find_member_by_id(mid)
        if member is None:
            print("Member not found.")
            return
        if not member.active:
            print("Member is already inactive.")
            return
        member.deactivate()
        print(f"Member {member.name} is now inactive.")

    def add_charge_to_member(self):
        print("\n=== Add Charge to Member ===")
        self.list_members(show_details=False)
        mid = read_int("Enter member id to charge: ")
        member = self.find_member_by_id(mid)
        if member is None:
            print("Member not found.")
            return
        try:
            amount = float(input("Charge amount: $"))
        except ValueError:
            print("Invalid amount.")
            return
        self._billing.charge_member(member, amount)

    def record_payment(self):
        print("\n=== Record Payment ===")
        self.list_members(show_details=False)
        mid = read_int("Enter member id: ")
        member = self.find_member_by_id(mid)
        if member is None:
            print("Member not found.")
            return
        try:
            amount = float(input("Payment amount: $"))
        except ValueError:
            print("Invalid amount.")
            return
        self._billing.record_payment(member, amount)

    # --- Class management ---

    def create_class(self):
        print("\n=== Create Fitness Class ===")
        name = read_nonempty("Class name: ")
        difficulty = input("Difficulty (beginner/intermediate/advanced): ").strip().lower()
        capacity = read_int("Capacity: ", min_value=1)
        fitness_class = FitnessClass(self._next_class_id, name, difficulty, capacity)
        self._classes.append(fitness_class)
        print(f"Fitness class created with id {self._next_class_id}")
        self._next_class_id += 1

    def list_classes(self, show_enrollment=True):
        print("\n=== Fitness Classes ===")
        if not self._classes:
            print("No classes found.")
        for c in self._classes:
            if show_enrollment:
                print(c)
            else:
                print(f"[{c.id}] {c.name}")
        print()

    def find_class_by_id(self, class_id):
        for c in self._classes:
            if c.id == class_id:
                return c
        return None

    def enroll_member_in_class(self):
        print("\n=== Enroll Member in Class ===")
        self.list_members(show_details=False)
        mid = read_int("Enter member id: ")
        member = self.find_member_by_id(mid)
        if member is None:
            print("Member not found.")
            return
        if not member.active:
            print("Cannot enroll an inactive member.")
            return
        self.list_classes(show_enrollment=False)
        cid = read_int("Enter class id: ")
        fclass = self.find_class_by_id(cid)
        if fclass is None:
            print("Class not found.")
            return
        if fclass.is_full():
            print("Class is full.")
            return
        if fclass.is_enrolled(mid):
            print("Member is already enrolled in this class.")
            return
        fclass.enroll(mid)
        print(f"Enrolled {member.name} in {fclass.name}.")
        # Polymorphism: get_class_fee() returns the right amount per subclass
        self._billing.charge_class_enrollment(member)

    def list_class_roster(self):
        print("\n=== Class Roster ===")
        self.list_classes(show_enrollment=False)
        cid = read_int("Enter class id: ")
        fclass = self.find_class_by_id(cid)
        if fclass is None:
            print("Class not found.")
            return
        print(f"\nRoster for {fclass.name}:")
        if not fclass.enrolled_ids:
            print("No members enrolled.")
            return
        for mid in fclass.enrolled_ids:
            m = self.find_member_by_id(mid)
            if m:
                print(f"- {m.name} ({m.membership_type})")

    # --- Trainer management ---

    def add_trainer(self):
        print("\n=== Add Trainer ===")
        name = read_nonempty("Trainer name: ")
        specialty = read_nonempty("Specialty (e.g., yoga, strength, cardio): ")
        trainer = Trainer(self._next_trainer_id, name, specialty)
        print("Enter trainer availability (e.g., Mon 9-11). Leave blank to stop.")
        while True:
            slot = input("Availability: ").strip()
            if not slot:
                break
            trainer.add_schedule_slot(slot)
        self._trainers.append(trainer)
        print(f"Trainer added with id {self._next_trainer_id}")
        self._next_trainer_id += 1

    def list_trainers(self, show_schedule=True):
        print("\n=== Trainers ===")
        if not self._trainers:
            print("No trainers found.")
        for t in self._trainers:
            if show_schedule:
                print(t)
            else:
                print(f"[{t.id}] {t.name}")
        print()

    def find_trainer_by_id(self, trainer_id):
        for t in self._trainers:
            if t.id == trainer_id:
                return t
        return None

    def update_trainer_schedule(self):
        print("\n=== Update Trainer Schedule ===")
        self.list_trainers(show_schedule=False)
        tid = read_int("Enter trainer id: ")
        trainer = self.find_trainer_by_id(tid)
        if trainer is None:
            print("Trainer not found.")
            return
        print("Current schedule:")
        for s in trainer.schedule:
            print(f"- {s}")
        print("1. Replace schedule")
        print("2. Add to schedule")
        choice = read_int("Choice: ", min_value=1, max_value=2)
        if choice == 1:
            new_slots = []
            print("Enter new availability (blank to finish):")
            while True:
                slot = input("Availability: ").strip()
                if not slot:
                    break
                new_slots.append(slot)
            trainer.replace_schedule(new_slots)
        else:
            print("Enter additional availability (blank to finish):")
            while True:
                slot = input("Availability: ").strip()
                if not slot:
                    break
                trainer.add_schedule_slot(slot)
        print("Updated schedule:")
        for s in trainer.schedule:
            print(f"- {s}")

    # --- Reporting ---

    def show_summary_report(self):
        print("\n=== Summary Report ===")
        total = len(self._members)
        active = sum(1 for m in self._members if m.active)
        total_balance = sum(m.balance for m in self._members)
        print(f"Total members: {total}")
        print(f"Active members: {active}")
        print(f"Total outstanding balance: ${total_balance:.2f}")
        print("\nClasses:")
        for c in self._classes:
            print(f"- {c.name} ({c.difficulty}): {c.enrollment_count}/{c.capacity} enrolled")
        print("\nTrainers:")
        for t in self._trainers:
            print(f"- {t.name} ({t.specialty})")
        print()

    # --- Menus ---

    def member_menu(self):
        while True:
            print("\n=== Member Menu ===")
            print("1. Add member")
            print("2. List members")
            print("3. Deactivate member")
            print("4. Add charge to member")
            print("5. Record payment from member")
            print("6. Back to main menu")
            choice = read_int("Choice: ", min_value=1, max_value=6)
            if choice == 1:
                self.add_member()
            elif choice == 2:
                self.list_members()
            elif choice == 3:
                self.deactivate_member()
            elif choice == 4:
                self.add_charge_to_member()
            elif choice == 5:
                self.record_payment()
            elif choice == 6:
                break
            pause()

    def classes_menu(self):
        while True:
            print("\n=== Classes Menu ===")
            print("1. Create fitness class")
            print("2. List fitness classes")
            print("3. Enroll member in class")
            print("4. Show class roster")
            print("5. Back to main menu")
            choice = read_int("Choice: ", min_value=1, max_value=5)
            if choice == 1:
                self.create_class()
            elif choice == 2:
                self.list_classes()
            elif choice == 3:
                self.enroll_member_in_class()
            elif choice == 4:
                self.list_class_roster()
            elif choice == 5:
                break
            pause()

    def trainer_menu(self):
        while True:
            print("\n=== Trainer Menu ===")
            print("1. Add trainer")
            print("2. List trainers")
            print("3. Update trainer schedule")
            print("4. Back to main menu")
            choice = read_int("Choice: ", min_value=1, max_value=4)
            if choice == 1:
                self.add_trainer()
            elif choice == 2:
                self.list_trainers()
            elif choice == 3:
                self.update_trainer_schedule()
            elif choice == 4:
                break
            pause()

    def run(self):
        """Main application loop."""
        while True:
            print(f"\n=== {self._name} Management ===")
            print("1. Manage members")
            print("2. Manage classes")
            print("3. Manage trainers")
            print("4. Show summary report")
            print("5. Exit")
            choice = read_int("Choice: ", min_value=1, max_value=5)
            if choice == 1:
                self.member_menu()
            elif choice == 2:
                self.classes_menu()
            elif choice == 3:
                self.trainer_menu()
            elif choice == 4:
                self.show_summary_report()
                pause()
            elif choice == 5:
                print("Goodbye!")
                break