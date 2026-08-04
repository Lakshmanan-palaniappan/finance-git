"""
Application Entry Point
"""

from generators.simulator import BankingSimulator
from generators.common.logger import logger


def main():

    logger.info(
        "Starting Enterprise Banking Data Simulator..."
    )

    try:

        simulator = BankingSimulator()

        simulator.start()

    except KeyboardInterrupt:

        logger.info(
            "Application stopped by user."
        )

    except Exception:

        logger.exception(
            "Application terminated due to an unexpected error."
        )


if __name__ == "__main__":

    main()