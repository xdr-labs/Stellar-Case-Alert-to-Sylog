"""Regression coverage for first-run lookback defaults and explicit overrides."""

import importlib.util
from pathlib import Path
import sqlite3
import unittest
from unittest.mock import patch


RUNTIME_PATH = Path(__file__).resolve().parents[1] / "Stellar_Alert_Case_Syslog.py"
SPEC = importlib.util.spec_from_file_location("stellar_relay", RUNTIME_PATH)
relay = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(relay)


class InitialLookbackTest(unittest.TestCase):
    def test_default_is_one_hour_for_cli_and_fetch(self):
        self.assertEqual(relay.INITIAL_LOOKBACK_HOURS, 1)
        self.assertEqual(relay.parse_args([]).initial_lookback_hours, 1)
        self.assertEqual(relay.initial_lookback_ms(), 60 * 60 * 1000)

    def test_explicit_overrides_still_work(self):
        self.assertEqual(
            relay.parse_args(["--initial-lookback-hours", "48"]).initial_lookback_hours, 48
        )
        self.assertEqual(
            relay.parse_args(["--initial-lookback-hours", "0"]).initial_lookback_hours, 0
        )

    def test_first_run_case_uses_one_hour_and_alert_uses_stable_cutoff(self):
        with sqlite3.connect(":memory:") as conn:
            relay.db_init(conn)
            with patch.object(relay, "now_ms", return_value=10_000_000):
                self.assertEqual(relay.case_fetch_from_ts(conn), 6_400_000)
                self.assertEqual(
                    relay._alert_fetch_lower_bound_ms(
                        conn, stable_upper_bound_ms=9_880_000
                    ),
                    6_280_000,
                )


if __name__ == "__main__":
    unittest.main()
