text = "Sample00\n①\n②\n③\n写真-1"
lines = text.split('\n')

result = []
for i in range(len(lines)):
    if lines[i] == "写真-1":
        result.append(lines[i-1] + ', ' + lines[i])
    else:
        result.append(lines[i])

output = '\n'.join(result)
print(lines)