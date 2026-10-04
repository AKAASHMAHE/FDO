"""
Generate the FDO OWL ontology file.
"""

import sys
from pathlib import Path

# Add Backend root to Python import path.
BACKEND_ROOT = Path(__file__).resolve().parents[1]

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


from app.ontology.owl_builder import serialize_fdo_ontology


def main():
    ontology_directory = BACKEND_ROOT / "ontology"

    ontology_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = ontology_directory / "FDO.owl"

    serialize_fdo_ontology(
        str(output_file),
        format="xml",
    )

    print("FDO ontology generated successfully.")
    print(f"Output: {output_file}")


if __name__ == "__main__":
    main()