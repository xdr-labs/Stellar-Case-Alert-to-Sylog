<h1 align="center">Stellar Relay</h1>

<p align="center">
  <strong>Stellar Cyber Alert와 Case를 안정적인 NDJSON Stream으로 전달합니다.</strong>
</p>

<p align="center">
  Stellar Cyber API를 polling하고 local queue/checkpoint를 유지하면서 활성화된 Alert/Case stream을 TCP collector로 전달하는 lightweight Python daemon입니다.
</p>

<p align="center">
  <a href="README.md">English</a> · <strong>한국어</strong> · <a href="https://stellar-relay.xdr.ooo/ko">제품 문서</a>
</p>

---

## 주요 기능

Stellar Relay는 **Stellar Cyber Alert와 Case**를 TCP 기반 NDJSON으로 전달합니다.

- Alert와 Case를 독립적으로 활성화
- SQLite queue/checkpoint로 상태 보존
- 한 줄에 하나의 JSON object 전송
- 첫 설정은 Interactive Setup Wizard 권장
- 자동화/문제 해결을 위한 Manual CLI 지원
- Wizard에서 systemd 설치·활성화·즉시 시작 가능

> Historical repository/option naming과 달리 실제 output은 **RFC 5424 Syslog가 아니라 NDJSON over TCP**입니다.

## 빠른 시작

```bash
git clone https://github.com/xdr-labs/Stellar-Case-Alert-to-Sylog.git
cd Stellar-Case-Alert-to-Sylog

python3 Stellar_Alert_Case_Syslog.py
```

명시적으로 Wizard를 실행하려면:

```bash
python3 Stellar_Alert_Case_Syslog.py --setup
```

Wizard에서는 다음을 설정합니다.

- Stellar Host / 이메일 형식 User ID / All-Access API Token
- Alert Forwarding 사용 여부
- Case Forwarding 사용 여부
- 활성화한 Stream의 Interval / Destination IP / TCP Port
- First-run Lookback
- systemd 자동 설치 및 시작 여부

API Token은 화면에 표시되지 않으며 systemd `ExecStart`에도 포함되지 않습니다.

### 기본값

| 항목 | 기본값 |
|---|---:|
| Alert | 활성화 |
| Alert Interval | 60초 |
| Alert Port | 5201 |
| Case | 비활성화 |
| Case Interval | 300초 |
| Case Port | 5202 |
| Initial Lookback | 48시간 |

`--initial-lookback-hours 0`은 최근 1분을 의미합니다.

## systemd 운영

Wizard에서 systemd 설치를 선택하면 다음 Service가 설치·활성화·시작됩니다.

```text
stellar-alert-case-syslog.service
```

운영 명령:

```bash
sudo systemctl status stellar-alert-case-syslog
sudo journalctl -u stellar-alert-case-syslog -f
sudo systemctl restart stellar-alert-case-syslog
```

Token은 root-only 권한의 다음 파일에 저장됩니다.

```text
/etc/default/stellar-alert-case-syslog
```

## Manual CLI

권장 Token 전달 방식:

```bash
export STELLAR_TOKEN='YOUR_TOKEN'
```

Alert only:

```bash
python3 Stellar_Alert_Case_Syslog.py \
  --host YOUR_STELLAR_HOST \
  --userid YOUR_USER_EMAIL \
  --alert-interval 60 \
  --alert-syslog-ip 10.10.10.20 \
  --alert-syslog-port 5201
```

Case only:

```bash
python3 Stellar_Alert_Case_Syslog.py \
  --host YOUR_STELLAR_HOST \
  --userid YOUR_USER_EMAIL \
  --case-interval 300 \
  --case-syslog-ip 10.10.10.20 \
  --case-syslog-port 5202
```

각 Stream은 `interval + destination IP + destination port` 세 옵션을 모두 지정해야 활성화됩니다.

## Case 기본값

| Option | Default |
|---|---:|
| `--case-min-score` | 10 |
| `--case-include-summary` | enabled |
| `--case-format-summary` | enabled |
| `--case-fetch-limit` | 200 |

필요하면 `--no-case-include-summary`, `--no-case-format-summary`를 사용할 수 있습니다.

## Local State

```text
~/.local/state/stellar_alert_case/
├── queue.db
├── logs/
└── stellar_alert_case.lock
```

Single-instance lock을 사용하므로 동일 state를 사용하는 두 프로세스를 동시에 실행할 수 없습니다.

## Backfill

```bash
python3 Stellar_Alert_Case_Syslog.py --backfill 3 ...
```

Backfill은 normal checkpoint를 무시하고 historical record를 다시 보낼 수 있으므로 테스트/복구 목적으로만 사용합니다.

## 상세 문서

현재 Operator Guide:

**https://stellar-relay.xdr.ooo/ko**

Quickstart, Configuration, systemd 운영, Output Format, Troubleshooting은 위 문서를 기준으로 합니다.

---

<p align="center">
  <strong>Poll. Queue. Forward. Keep the streams independent.</strong>
</p>
