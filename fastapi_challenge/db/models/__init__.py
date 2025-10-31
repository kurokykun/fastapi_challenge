"""fastapi_challenge models.

This package exposes model modules and provides a helper to import all
model modules dynamically. Importing `fastapi_challenge.db.models` will not
automatically pull every ORM class into the local namespace; use
`load_all_models()` or import specific classes when needed to keep
imports explicit and modular.
"""

import pkgutil
from pathlib import Path
from typing import List


def load_all_models() -> None:
    """Load all models from this folder.

    This is useful during Alembic autogenerate or other initialization steps
    which need all model modules to be imported so SQLAlchemy metadata is
    populated.
    """
    package_dir = Path(__file__).resolve().parent
    modules = pkgutil.walk_packages(
        path=[str(package_dir)],
        prefix="fastapi_challenge.db.models.",
    )
    for module in modules:
        __import__(module.name)


__all__: List[str] = ["load_all_models"]
