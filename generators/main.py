"""
Enterprise Banking Simulator

Application Entry Point
Supports:
    - Local execution
    - Databricks Jobs
    - Future DAB deployment
"""

import argparse

from generators.common.config import JOB_DEFAULT_MODE
from generators.common.logger import logger
from generators.simulator import BankingSimulator


def parse_arguments():
    """
    Command-line arguments.

    Examples
    --------
    python -m generators.main

    python -m generators.main --mode full

    python -m generators.main --mode master

    python -m generators.main --mode streaming

    python -m generators.main --mode cdc
    """

    parser = argparse.ArgumentParser(
        description="Enterprise Banking Data Simulator"
    )

    parser.add_argument(
        "--mode",
        default=JOB_DEFAULT_MODE,
        choices=[
            "full",
            "master",
            "cdc",
            "streaming",
        ],
        help="Simulation mode",
    )

    return parser.parse_args()


def banner(mode: str):

    logger.info("=" * 80)

    logger.info(
        "Enterprise Banking Data Simulator"
    )

    logger.info(
        f"Execution Mode : {mode.upper()}"
    )

    logger.info("=" * 80)


def main():

    args = parse_arguments()

    banner(args.mode)

    simulator = BankingSimulator()

    try:

        #
        # Current simulator only exposes start().
        #
        # Until we refactor BankingSimulator,
        # every mode calls start().
        #
        # Later we'll add:
        #
        # simulator.generate_master()
        # simulator.generate_cdc()
        # simulator.generate_streaming()
        #
        simulator.start()

        logger.info(
            "Simulation completed successfully."
        )

    except KeyboardInterrupt:

        logger.warning(
            "Simulation stopped by user."
        )

    except Exception as ex:

        logger.exception(
            f"Simulation failed: {ex}"
        )

        raise


if __name__ == "__main__":

    main()