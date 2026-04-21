"""
MAILFLOW — Entry Point
Slim CLI wrapper that initialises the Agent Coordinator and runs the pipeline.
"""

import sys
import logging
import argparse

# ── Logging Setup ────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("email_agent.log"),
        logging.StreamHandler(sys.stdout),
    ],
)


def main() -> int:
    print("=" * 55)
    print("   ✉  MAILFLOW — Agentic Email Support System")
    print("=" * 55)

    parser = argparse.ArgumentParser(description="MAILFLOW Email Support Agent")
    parser.add_argument(
        "--continuous", action="store_true",
        help="Run in continuous polling mode",
    )
    parser.add_argument(
        "--interval", type=int, default=300,
        help="Polling interval in seconds (default: 300)",
    )
    args = parser.parse_args()

    try:
        from coordinator import AgentCoordinator

        coordinator = AgentCoordinator()
        coordinator.run(continuous=args.continuous, interval=args.interval)
    except Exception as e:
        logging.error(f"System error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
