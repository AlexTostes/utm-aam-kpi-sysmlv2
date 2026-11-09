"""Replace the package cells of the notebooks with the current .sysml sources (markdown and %viz cells kept)."""
import json, re, sys, glob
pk = {}
for f in sys.argv[2:]:
    src = open(f, encoding="utf-8").read()
    for m in re.finditer(r"^package (\w+) \{.*?^\}", src, re.S | re.M):
        pk[m.group(1)] = m.group(0)
nb = json.load(open(sys.argv[1], encoding="utf-8"))
n = 0
for c in nb["cells"]:
    if c["cell_type"] == "code":
        m = re.match(r"package (\w+) \{", "".join(c["source"]))
        if m:
            text = pk[m.group(1)]
            c["source"] = [l + "\n" for l in text.split("\n")[:-1]] + [text.split("\n")[-1]]
            c["outputs"] = []; c["execution_count"] = None; n += 1
json.dump(nb, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(sys.argv[1], n, "package cells updated")
