import subprocess
from datetime import datetime

# STEP 1 — basic inputs
n = input("Enter number of log lines: ")
filename = input("Enter file name (e.g., report.txt): ")

# STEP 2 — ask for time filter
choice = input("Do you want to filter by time? (yes/no): ").lower()

if choice == "yes":
    print("\nEnter date and time details")

    date = input("Enter date (YYYY-MM-DD): ")

    hour = input("Enter hour (HH): ")
    minute = input("Enter minute (MM): ")
    second = input("Enter second (SS): ")

    time_filter = f"{date} {hour}:{minute}:{second}"

    command = f'journalctl --since "{time_filter}" -n {n}'

else:
    command = f'journalctl -n {n}'

# STEP 3 — get logs
logs = subprocess.getoutput(command)

# STEP 4 — split logs
lines = logs.split("\n")

# STEP 5 — counters
error_count = 0
failed_count = 0
errors = []

# STEP 6 — process logs
for line in lines:
    lower_line = line.lower()

    if "error" in lower_line or "failed" in lower_line:
        parts = line.split()

        if len(parts) >= 3:
            timestamp = " ".join(parts[:3])
        else:
            timestamp = "UNKNOWN"

        message = " ".join(parts[3:])
        errors.append((timestamp, message))

        if "error" in lower_line:
            error_count += 1
        if "failed" in lower_line:
            failed_count += 1

# STEP 7 — colors
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

print("\n===== ERROR SUMMARY =====\n")

if len(errors) == 0:
    print(GREEN + "No errors found." + RESET)
else:
    for ts, msg in errors:
        print(RED + f"[{ts}] {msg}" + RESET)

print("\nERROR COUNT:", error_count)
print("FAILED COUNT:", failed_count)

# STEP 8 — save report
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(filename, "w") as file:
    file.write(f"Report generated at: {now}\n")

    if choice == "yes":
        file.write(f"Filtered since: {time_filter}\n")

    file.write("\n")

    for ts, msg in errors:
        file.write(f"[{ts}] {msg}\n")

    file.write("\nSUMMARY:\n")
    file.write(f"ERROR COUNT: {error_count}\n")
    file.write(f"FAILED COUNT: {failed_count}\n")

print(f"\nReport saved to {filename}")
