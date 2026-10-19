# mtklogo GUI (v1.1)

> **New in 1.1:** Ready AppImage (`mtklogo-gui-1.1-x86_64.AppImage`), **set selector**
> Comparring (Original × Suggested), with button **Choose logo.bin…**, folder `suggested/` (script v2 + patched mtklogo + new yaml)
> and correction in prompt detection (ignores `read` from script internal pipes).
> Details and justifications in `ANALYSIS_AND_SUGGESTIONS.md`.

## AppImage (simplest)

```bash
chmod +x mtklogo-gui-1.1-x86_64.AppImage
./mtklogo-gui-1.1-x86_64.AppImage
```
* On the first run it creates `~/mtklogo-gui/original/` and `~/mtklogo-gui/suggested/` (with a `logo.bin` of **example**). Everything the script generates 
(`logo/`, `out/`, `backup/`) is in these folders. Use **Choose logo.bin…** to bring yours.
* No FUSE (`libfuse2`)? `./mtklogo-gui-1.1-x86_64.AppImage --appimage-extract-and-run`
* Requires glibc ≥ 2.34 (Ubuntu 22.04+, Debian 12+, Fedora 35+, Arch…) because of the `mtklogo` binary. Qt/xcb are built-in.

## From sources

`./run.sh` opens the original pool; **`./run.sh suggested`** opens the suggested set (`suggested/` folder).

Minimalist graphical interface (Python + Qt) for `mtklogos.sh`.

The script runs **exactly as is** (`bash ./mtklogos.sh`): the GUI only captures the output in real time and respond to his questions through dialogue.

## Content

| Archive | Description |
|---|---|
| `mtklogo_gui.py` | The graphical interface (PySide6, with fallback to PyQt5) |
| `run.sh` | Launcher: use the system Qt or create a `.venv` with PySide6 |
| `requirements.txt` | Python Dependency (`PySide6-Essentials`) |
| `mtklogos.sh` | Original script (**unchanged**) |
| `mtklogo` | Linux binary x86-64 v1.0.1 (identical to the latest upstream release) |
| `mtklogo.yaml` | Fork profiles **+ 8 merged upstream profiles** (see below) |
| `logo.bin` | example `logo.bin` from repository (replace with yours) |
| `suggested/` | `mtklogos.sh` v2, `mtklogo.yaml` with `exp_*` fixes/profiles, `mtklogo` patched |
| `mtklogo-improvements.patch` | Rust source code patch (apply over `cyberknight777/mtklogo`) |
| `ANALYSIS_AND_SUGGESTIONS.md` | Script, yaml and source code analysis |
