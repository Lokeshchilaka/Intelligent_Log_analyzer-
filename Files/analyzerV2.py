import subprocess

# STEP 1 — take user input
n = input("Enter number of log lines: ")

# STEP 2 — get logs
logs = subprocess.getoutput(f"journalctl -n {n}")

# STEP 3 — split logs
lines = logs.split("\n")

# STEP 4 — counters + storage
error_count = 0
failed_count = 0
errors = []

# STEP 5 — process logs
for line in lines:
    if "error" in line.lower():
        error_count += 1
        errors.append(line)

    if "failed" in line.lower():
        failed_count += 1
        errors.append(line)

# STEP 6 — print results
print("\n===== ERROR SUMMARY =====\n")

if len(errors) == 0:
    print("No errors found.")
else:
    for err in errors:
        print(err)

print("\nERROR COUNT:", error_count)
print("FAILED COUNT:", failed_count)

# STEP 7 — save report
with open("report.txt", "w") as file:
    file.write("ERROR COUNT: " + str(error_count) + "\n")
    file.write("FAILED COUNT: " + str(failed_count) + "\n")

print("\nReport saved to report.txt")
