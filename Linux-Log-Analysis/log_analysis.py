import csv

# Open and read the Linux log file
with open("Linux_2k.log", "r", encoding="utf-8", errors="replace") as file:
    logs = file.readlines()

# Focus on lines 200 through 500
subset_logs = logs[199:500]

# Store suspicious entries
suspicious_entries = []

for line in subset_logs:
    lower_line = line.lower()

    if "failed password" in lower_line:
        suspicious_entries.append(("Failed Login", line.strip()))

    elif "authentication failure" in lower_line:
        suspicious_entries.append(("Authentication Failure", line.strip()))

    elif "user unknown" in lower_line or "invalid user" in lower_line:
        suspicious_entries.append(("Unknown User", line.strip()))

    elif "exited abnormally" in lower_line:
        suspicious_entries.append(("Abnormal Exit", line.strip()))

# Display results
print("=== Suspicious Log Entries: Lines 200–500 ===")

for event_type, entry in suspicious_entries:
    print(f"[{event_type}] {entry}")

print(f"\nTotal suspicious entries found: {len(suspicious_entries)}")

# Export results to CSV
with open("suspicious_logs.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Type", "Log Entry"])
    writer.writerows(suspicious_entries)

print("Results saved to suspicious_logs.csv")