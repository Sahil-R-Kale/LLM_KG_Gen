# LLM_KG_Gen
Extracts subject–relation–object triples from unstructured text using an LLM and optionally visualizes the output as a knowledge graph.

---

## Requirements

```bash
pip install -r requirements.txt
```

---

## Usage

Run the script from the terminal with the required parameters:

```bash
python main.py --input_path path/to/input.txt [--output_dir path/to/output_dir] [--model MODEL_NAME] [--visualize]
```

### Arguments

- `--input_path`: Path to the input text file containing raw text (required).
- `--output_dir`: Directory where the output JSON file will be saved (default: `outputs`).
- `--model`: LLM model name to use (default: `gpt-4o`).
- `--visualize`: Flag to display a graph visualization of extracted triples.

---

## Example

Given an input file `inputs/spaceX.txt` with the following content:

```
In 2020, Elon Musk, the CEO of Tesla and SpaceX, announced that SpaceX would collaborate with NASA to launch the Artemis program's first cargo payload.
```

Run the tool:

```bash
python main.py --input_path inputs/spaceX.txt --output_dir outputs --visualize
```

Output file `outputs/triples_spaceX.txt.json` will contain triples like:

```json
[
  [
    "Elon_Musk",
    "CEO",
    "Tesla"
  ],
  [
    "Elon_Musk",
    "CEO",
    "SpaceX"
  ],
  [
    "SpaceX",
    "partneredWith",
    "NASA"
  ],
  [
    "SpaceX",
    "launchProgram",
    "Artemis_program"
  ],
...
]
```

A visualization window will open showing the knowledge graph.

---
