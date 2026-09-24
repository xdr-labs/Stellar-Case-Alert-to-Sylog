<h1 align="center">Stellar Relay</h1>

<p align="center">
  <strong>Forward Stellar Cyber alerts and cases as reliable NDJSON streams.</strong>
</p>

<p align="center">
  A lightweight Python daemon that polls Stellar Cyber, queues records locally, and forwards enabled Alert and Case streams to a TCP collector.
</p>

<p align="center">
  <strong>English</strong> · <a href="README.ko.md">한국어</a> · <a href="https://stellar-relay.xdr.ooo/">Product Website</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-2563EB?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/output-NDJSON-16A34A?style=flat-square" alt="NDJSON">
  <img src="https://img.shields.io/badge/transport-TCP-7C3AED?style=flat-square" alt="TCP">
  <img src="https://img.shields.io/badge/state-SQLite-0F766E?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite">
</p>

---

## What it does

Stellar Relay forwards **Stellar Cyber Alerts and Cases** to a remote collector over TCP as newline-delimited JSON.

- Alert and Case streams can be enabled independently.
- SQLite stores durable queue and checkpoint state.
- One JSON object is sent per line.
- Interactive setup is the recommended first-run path.
- Manual CLI execution remains available for automation and troubleshooting.
- The setup wizard can install, enable, and start a systemd service automatically.

> Despite historical repository and option naming, the output is **NDJSON over TCP**, not RFC 5424 syslog text.

## Data flow

```mermaid
flowchart LR
    S["Stellar Cyber API"] --> P["Stellar Relay<br/>Alert / Case Pollers"]
    P --> Q["SQLite Queue<br/>Checkpoints"]
    Q --> T["TCP Sender"]
    T --> C["Remote Collector<br/>NDJSON"]
```

## Quick start

Clone the repository:

```bash
git clone https://github.com/xdr-labs/Stellar-Case-Alert-to-Sylog.git
cd Stellar-Case-Alert-to-Sylog
```

Start the setup wizard:

```bash
python3 Stellar_Alert_Case_Syslog.py
```

or explicitly:

```bash
python3 Stellar_Alert_Case_Syslog.py --setup
```

The wizard asks for:

- Stellar host, user ID, and All-Access API token
- whether to enable Alert forwarding
- whether to enable Case forwarding
- interval, destination IP, and destination TCP port for each enabled stream
- first-run lookback
- whether to install and start the systemd service

The API token is entered without echo and is not embedded in the systemd `ExecStart` command.

### Wizard defaults

| Setting | Default |
|---|---:|
| Alert forwarding | enabled |
| Alert interval | 60 seconds |
| Alert destination port | 5201 |
| Case forwarding | disabled |
| Case interval | 300 seconds |
| Case destination port | 5202 |
| Initial lookback | 48 hours |

`--initial-lookback-hours 0` means the last 1 minute.

## systemd operation

If you answer **Yes** to systemd installation, the wizard installs and starts:

```text
stellar-alert-case-syslog.service
```

Useful commands:

```bash
sudo systemctl status stellar-alert-case-syslog
sudo journalctl -u stellar-alert-case-syslog -f
sudo systemctl restart stellar-alert-case-syslog
```

The service token is stored in:

```text
/etc/default/stellar-alert-case-syslog
```

with root-only permissions.

## Manual CLI

Set the token with an environment variable:

```bash
export STELLAR_TOKEN='YOUR_TOKEN'
```

Alert only:

```bash
python3 Stellar_Alert_Case_Syslog.py \
  --host YOUR_STELLAR_HOST \
  --userid YOUR_USER_ID \
  --alert-interval 60 \
  --alert-syslog-ip 10.10.10.20 \
  --alert-syslog-port 5201
```

Case only:

```bash
python3 Stellar_Alert_Case_Syslog.py \
  --host YOUR_STELLAR_HOST \
  --userid YOUR_USER_ID \
  --case-interval 300 \
  --case-syslog-ip 10.10.10.20 \
  --case-syslog-port 5202
```

Alert + Case:

```bash
python3 Stellar_Alert_Case_Syslog.py \
  --host YOUR_STELLAR_HOST \
  --userid YOUR_USER_ID \
  --alert-interval 60 \
  --alert-syslog-ip 10.10.10.20 \
  --alert-syslog-port 5201 \
  --case-interval 300 \
  --case-syslog-ip 10.10.10.20 \
  --case-syslog-port 5202
```

Each enabled stream requires all three stream options together: interval, destination IP, and destination port.

## Current Case defaults

| Option | Default |
|---|---:|
| `--case-min-score` | 10 |
| `--case-include-summary` | enabled |
| `--case-format-summary` | enabled |
| `--case-fetch-limit` | 200 |

Use `--no-case-include-summary` or `--no-case-format-summary` when required.

## Local state

Default state is stored under:

```text
~/.local/state/stellar_alert_case/
├── queue.db
├── logs/
└── stellar_alert_case.lock
```

The single-instance lock prevents two copies from using the same runtime state simultaneously.

## Backfill

Historical re-fetch is available with:

```bash
python3 Stellar_Alert_Case_Syslog.py --backfill 3 ...
```

Backfill intentionally ignores normal checkpoints and can resend historical records. Use it only for controlled testing or recovery.

## Documentation

The operator-focused guide is maintained at:

**https://stellar-relay.xdr.ooo/**

It contains the current Quickstart, configuration reference, service operations, output format, and troubleshooting guidance.

---

<p align="center">
  <strong>Poll. Queue. Forward. Keep the streams independent.</strong>
</p>
