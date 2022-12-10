from pkgutil import iter_modules

EXTENSIONS = [module.name for module in iter_modules(["F:\\Acrylic-Original\\cogs"], f'cogs.')]