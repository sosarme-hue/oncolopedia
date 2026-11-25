"""Divide un fichero con bloques '=== ruta' en varios ficheros (ruta relativa a src/)."""
import os, sys
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
cur, buf, n = None, [], 0
def flush():
    global n
    if cur:
        fp = os.path.join(root, cur)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, "w", encoding="utf-8").write("\n".join(buf).strip() + "\n")
        n += 1
for line in open(sys.argv[1], encoding="utf-8").read().split("\n"):
    if line.startswith("=== "):
        flush(); cur, buf = line[4:].strip(), []
    else:
        buf.append(line)
flush()
print(n, "ficheros")
