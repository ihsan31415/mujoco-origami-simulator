# Examples

Runnable snippets showing how to use the library. Each script bootstraps the
package onto `sys.path` so they work directly from a checkout:

```bash
. .venv/bin/activate
python examples/01_evaluate_reference.py
```

| Script | Shows |
|---|---|
| [`01_evaluate_reference.py`](01_evaluate_reference.py) | Evaluate a reference crease pattern and print its fitness score |
| [`02_json_input.py`](02_json_input.py) | Save and load creases via JSON (`save_creases_to_json` / `load_creases_from_json`) |
| [`03_inspect_pattern.py`](03_inspect_pattern.py) | Inspect the reconstructed face graph (faces, hinges, loop edges) |
| [`04_evaluate_population.py`](04_evaluate_population.py) | Score a small population, optionally in parallel with `workers` |
| [`05_plot_pattern.py`](05_plot_pattern.py) | Plot a crease pattern with `plot_pattern` (Mountain/Valley, face indices, 180° labels) |
