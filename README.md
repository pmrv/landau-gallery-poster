# landau poster gallery

The notebooks behind the figures on the [landau](https://github.com/eisenforschung/landau) poster. Each one is a short introduction to a part of landau and saves its figures next to the notebook.

| Notebook | What it shows |
|---|---|
| `Intro/MgCa_Phasediagram_Construction.ipynb` | How a phase diagram is built from free energies |
| `Ideal/Ideal_Solution.ipynb` | The simplest binary phase diagram and a 1D cut |
| `Ase/Solid_Gas_ASE.ipynb` | Phases from ASE thermochemistry |
| `Ase/Sublimation_ASE.ipynb` | A sublimation curve from ASE (not on the poster) |
| `Point/Point_Defects_Exact.ipynb` | A compound with point defects |
| `CuPt/cupt_ordering.ipynb` | From structures and phonons to a phase diagram, and colouring phase fields |
| `RealWorld/MgCa_Phasediagram_Full.ipynb` | The full Mg–Ca diagram |
| `RealWorld/AuCu_Phasediagrams.ipynb` | Au–Cu from three DFT functionals |

## Running

Install [pixi](https://pixi.sh), then:

```
pixi run lab      # open the notebooks in JupyterLab
pixi run all      # re-run every notebook
pixi run ideal    # re-run one notebook; see pixi.toml for the names
```
