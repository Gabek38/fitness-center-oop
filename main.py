# main.py
# Entry point for the OOP-refactored Campus Fitness Center.
# AI assistance (Claude by Anthropic) was used in this project per course policy.

from fitness_center import FitnessCenter

if __name__ == "__main__":
    center = FitnessCenter("Campus Fitness Center")
    center.run()