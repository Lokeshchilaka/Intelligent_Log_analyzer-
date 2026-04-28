import subprocess

# get last 100 logs
logs = subprocess.getoutput("journalctl -n 100")

# split logs into lines
lines = logs.split("\n")

# store errors
errors = []

# filter errors
for line in lines:
    if "error" in line.lower() or "failed" in line.lower():
        errors.append(line)

# print results
print("===== ERROR SUMMARY =====\n")

if len(errors) == 0:
    print("No errors found.")
else:
    for err in errors:
        print(err)
print("\nTOTAL ERRORS:", len(errors))
