"""Checagem estrutural do KPI_Framework.sysml (nao substitui o parser da OMG/Pilot)."""
import re, sys
src = open(sys.argv[1], encoding="utf-8").read()

# remove comentarios e strings
code = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
code = re.sub(r"//[^\n]*", "", code)
code = re.sub(r'"[^"]*"', '""', code)

# 1. chaves balanceadas, ponto e virgula fora de corpo
depth = 0
for i, ch in enumerate(code):
    depth += ch == "{"
    depth -= ch == "}"
    assert depth >= 0, f"chave fechada a mais perto de {code[max(0,i-80):i]}"
assert depth == 0, "chaves desbalanceadas"

# 2. pacotes e nomes declarados por pacote
pkgs = {}
for m in re.finditer(r"^package (\w+) \{(.*?)^\}", code, flags=re.S | re.M):
    pkgs[m.group(1)] = m.group(2)
decl = {p: set(re.findall(r"\b(?:def|dependency)\s+(?:<'[^']+'>\s+)?(\w+)", b)) for p, b in pkgs.items()}
enums = {n: set(re.findall(r"enum (\w+);", b)) for n, b in re.findall(r"enum def (\w+) \{(.*?)\}", pkgs["KPI_Taxonomy"], flags=re.S)}
imports = {p: re.findall(r"private import (\w+)::\*;", b) for p, b in pkgs.items()}
LIB = {"ScalarValues": {"Real", "Natural", "String", "Integer", "Boolean"}}

def visible(p):
    v = set(decl[p])
    for imp in imports[p]:
        v |= decl.get(imp, set()) | LIB.get(imp, set())
    return v

errors = []
for p, b in pkgs.items():
    vis = visible(p)
    for t in re.findall(r"(?<![:\w])(?::|:>)\s*(\w+)\s*[;{=]", b):
        if t not in vis:
            errors.append((p, "tipo", t))
    for c in re.findall(r"frame concern \w+ : (\w+);", b):
        if c not in vis:
            errors.append((p, "concern", c))
    for t in re.findall(r"@(\w+)", b):
        if t not in vis:
            errors.append((p, "metadata", t))
    for e, lit in re.findall(r"\b(\w+)::(\w+);", b):
        if e in enums:
            if lit not in enums[e]:
                errors.append((p, "enum", f"{e}::{lit}"))
        elif e in decl:
            if lit not in decl[e]:
                errors.append((p, "ref", f"{e}::{lit}"))
        else:
            errors.append((p, "pkg", e))
    for a, z in re.findall(r"dependency \w+ from ([\w:]+) to ([\w:]+);", b):
        for r in (a, z):
            if "::" in r:
                q, n = r.split("::")
                if n not in decl.get(q, set()):
                    errors.append((p, "dep", r))
            elif r not in vis:
                errors.append((p, "dep", r))

# 3. contagens
kpis = re.findall(r"calc def <'((?:UTM|AAM)-[A-Z]+-\d\d)'>", src)
pos = re.findall(r"requirement def PO_\w+", code)
deps = re.findall(r"dependency t_\w+", code)
diag = re.findall(r"dependency d_\w+", code)
print("KPIs:", len(kpis), "unicos:", len(set(kpis)), "| POs:", len(pos), "| rastreios KPI->PO:", len(deps), "| diagnosticos:", len(diag))
print("erros:", errors or "nenhum")
