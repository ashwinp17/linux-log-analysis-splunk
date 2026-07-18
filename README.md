# Linux Log Analysis, Python Automation, and Splunk Visualization

## Project Overview

This project demonstrates a Security Operations Center workflow by manually analyzing Linux authentication logs, automating suspicious-event detection with Python, and using Splunk Enterprise to investigate and visualize possible brute-force activity.

**Workflow:** Monitor → Detect → Analyze → Visualize → Alert → Report

## Tools Used

- Visual Studio Code
- Python
- Google Sheets
- Splunk Enterprise
- Docker Desktop
- Windows Subsystem for Linux
- LogHub Linux log dataset

## Manual Log Analysis

I manually reviewed Linux authentication logs and documented suspicious events, including:

- Authentication failures
- Unknown-user attempts
- Repeated login attempts
- Attempts targeting the root account
- Abnormal process activity

**Example log entry:**

```text
Jun 14 15:16:01 combo sshd(pam_unix)[19939]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4
```

**Classification:** Suspicious

**Reasoning:** This entry is an SSH authentication failure from `218.188.2.4`. The `uid=0` and `euid=0` fields reflect the privilege level of the sshd/PAM process performing the authentication check, not the username being attempted. Because `logname=` is blank, this individual line does not identify the targeted account. I classified it as suspicious because the same source IP appears repeatedly in the surrounding logs, which is consistent with automated credential guessing or brute-force activity.

**Benign comparison log entries:**

```text
Jun 28 04:03:15 combo su(pam_unix)[10735]: session opened for user cyrus by (uid=0)
Jun 28 04:03:16 combo su(pam_unix)[10735]: session closed for user cyrus
```

**Classification:** Benign / expected activity

**Reasoning:** These entries show a local user session opening and closing normally one second later. There are no failed passwords, unknown users, or repeated login attempts from an external source. I would treat this as expected activity unless additional surrounding events or account context indicated otherwise.

## Python Automation

I created `log_analysis.py` to:

- Read the Linux log file
- Analyze lines 200–500
- Detect suspicious authentication activity
- Classify suspicious events
- Export results to `suspicious_logs.csv`

The script identified **148 suspicious entries**.

## Splunk Investigation

I uploaded the Linux log dataset into Splunk Enterprise and used SPL searches to investigate suspicious authentication activity.

### Key Findings

- **Total Linux events:** 1,294
- **Suspicious authentication events:** 512 Suspicious authentication events accounted for 512 of 1,294 total events (~40%) — a significant share, not an isolated anomaly.
- **Source hosts identified:** 39
- **Most active source:** 150.183.249.110
- **Attempts from the most active source:** 80

## Splunk Dashboard

The dashboard includes:

1. Authentication Failures Over Time
2. Top Sources of Authentication Failures

![Final Splunk Security Dashboard](Screenshots/15_Final_Splunk_Security_Dashboard.png)

## Splunk Alert

I created a scheduled alert named:

**Potential SSH Brute-Force Activity**

The alert detects source hosts generating five or more suspicious authentication events within the previous 24 hours.

![Splunk Brute-Force Alert](Screenshots/17_Splunk_Brute_Force_Alert.png)

## Recommended Security Actions

- Review successful logins following failed attempts
- Disable direct root SSH login
- Require SSH key authentication
- Implement rate limiting or account lockout
- Block confirmed malicious sources
- Continue monitoring authentication logs

## Skills Demonstrated

- Linux log analysis
- Python scripting
- Security automation
- Splunk log ingestion
- SPL searching
- Field extraction with `rex`
- Statistical analysis with `stats`
- Dashboard creation
- Brute-force detection
- Alert configuration
- SOC reporting

## Project Files

- `Linux_2k.log`
- `log_analysis.py`
- `suspicious_logs.csv`
- `Linux Log Manual Findings.xlsx`
- `Linux Log Analysis Final Findings.pdf`
- `Screenshots/`

## Conclusion

This project demonstrated how manual investigation, Python automation, and SIEM analysis can work together in a SOC workflow.
