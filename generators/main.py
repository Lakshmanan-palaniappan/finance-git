"""
Enterprise Banking Simulator

Application Entry Point
"""

from generators.common.logger import logger
from generators.simulator import BankingSimulator


def main():

    logger.info("=" * 80)

    logger.info(
        "Enterprise Banking Data Simulator"
    )

    logger.info("=" * 80)

    simulator = BankingSimulator()

    try:

        simulator.start()

    except KeyboardInterrupt:

        logger.info(
            "Simulator stopped by user."
        )

    except Exception as ex:

        logger.exception(
            f"Simulator failed: {ex}"
        )

        raise


if __name__ == "__main__":

    main()