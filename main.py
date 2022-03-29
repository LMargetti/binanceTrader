from pathlib import Path

cwd = Path.cwd()
# print(cwd.stem)
print(cwd.parents[0].stem)

# for par in list(cwd.parents):
#     print(par.stem)
