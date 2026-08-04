"""
Application Entry Point
"""

from generators.simulator import BankingSimulator


def main():

    simulator = BankingSimulator()

    simulator.start()


if __name__ == "__main__":

    main()