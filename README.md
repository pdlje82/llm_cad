# llm_cad

Self-contained, parametric 3D CAD generation in Python. Geometry is built with
[CadQuery](https://cadquery.readthedocs.io/) (primary API) and optionally
[build123d](https://build123d.readthedocs.io/) (experimental), then exported to
industry-standard interchange formats — **STEP**, IGES, STL — that open cleanly
in Autodesk Inventor and other CAD packages.

## Setup

The project is scoped to a conda environment named `env_llm_cad` (Python 3.11).
Nothing is installed globally.

### 1. Create the environment

CadQuery is installed from **conda-forge** (do *not* pip-install cadquery):

```powershell
mamba env create -f environment.yml
```

or, to recreate from scratch:

```powershell
mamba create -n env_llm_cad -c conda-forge python=3.11 cadquery -y
conda activate env_llm_cad
pip install build123d
```

### 2. Activate and verify

```powershell
conda activate env_llm_cad
python -c "import cadquery; print('cadquery', cadquery.__version__)"
python -c "import build123d; print('build123d', build123d.__version__)"
```

## Running the examples

Activate the environment first, then run any example standalone from the repo
root. Generated files land in the `output_dir` configured in `settings.yml`
(`D:/CAD/llm_cad/output` by default).

```powershell
conda activate env_llm_cad

python examples/01_basic_box.py            # -> output/basic_box.step + .stl
python examples/02_bracket.py              # -> output/bracket.step
python examples/03_assembly.py             # -> output/assembly.step
python examples/04_plane.py                # -> output/plane.step
```

| Script | What it builds | Exports |
|--------|----------------|---------|
| `01_basic_box.py` | Parametric box | STEP, STL |
| `02_bracket.py`   | L-shaped mounting bracket: 2 base holes, 1 wall hole, filleted inner corner | STEP |
| `03_assembly.py`  | Two-part assembly (bolt through plate) using the Assembly API | STEP |
| `04_plane.py`     | Zero-thickness rectangular planar face | STEP |

All dimensions are in millimetres.

Default dimensions and the output directory are defined in `settings.yml`.
Edit that file to change geometry parameters.

## Opening STEP files in Autodesk Inventor

1. Launch Autodesk Inventor.
2. **File ▸ Open**, set the file type filter to *STEP Files (\*.stp; \*.step)*,
   and select a file from `output/` (e.g. `basic_box.step`).
3. In the import dialog, keep the default options (Inventor reads the B-rep
   solid directly). Choose to create a part (`.ipt`) for single solids, or an
   assembly (`.iam`) when opening `assembly.step`.
4. Click **OK / Open**. The solid appears as imported geometry.

STL files (e.g. `basic_box.stl`) can be brought in via **File ▸ Open** with the
*STL* filter, but they import as a mesh body, not a solid — see limitations.

## Known limitations

- **No parametric history tree in Inventor.** STEP/IGES carry only the final
  B-rep geometry, not the feature/parameter history. In Inventor the imported
  part is "dumb" solid geometry — there are no editable extrude/hole/fillet
  features and no driving dimensions. To change a dimension, edit the Python
  parameters here and re-export.
- **Mesh vs B-rep.** STEP and IGES are exact boundary representations (true
  curved/planar faces). STL is a triangulated mesh approximation — fine for
  visualization or 3D printing, lossy and non-editable as CAD. Prefer STEP for
  anything that must round-trip through Inventor.
- **IGES is legacy.** STEP (AP214/AP242) is the more robust, modern interchange
  format and is the default in this project; IGES is offered only as an option.
- **Assemblies.** `assembly.step` exports the positioned parts as a STEP
  assembly. Mate/constraint relationships are not transferred — only the placed
  geometry.

## Project layout

```
llm_cad/
├── environment.yml      # conda environment spec
├── settings.yml         # geometry parameters and output directory
├── README.md
├── CLAUDE.md            # hard project constraints
├── examples/
│   ├── _common.py       # shared export helper (STEP default, no fallbacks)
│   ├── geometry.py      # reusable object-oriented CadQuery models
│   ├── 01_basic_box.py
│   ├── 02_bracket.py
│   ├── 03_assembly.py
│   └── 04_plane.py
└── output/              # generated STEP/IGES/STL (gitignored)
```

## Conventions

See [CLAUDE.md](CLAUDE.md) for the enforced rules: STEP is the default export,
exports never fail silently (they raise), every script runs standalone, and
CadQuery is the primary API.
