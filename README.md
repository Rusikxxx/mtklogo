# mtklogo GUI (v1.2)

## **New in 1.2:
- The GUI now follows your computer's system language, with English as the default. The new version is 1.2, in the file mtklogo-gui-1.2-x86_64.AppImage (50 MB).
- Languages ​​included: `Brazilian Portuguese`, `English`, `German`, `Spanish`, and `French`. If you use another language, everything will be in English.

## **New in 1.1:
- ** Ready AppImage (`mtklogo-gui-1.2-x86_64.AppImage`), **set selector**
- Comparring (Original × Suggested), with button **Choose logo.bin…**, folder `suggested/` (script v2 + patched mtklogo + new yaml) and correction in prompt detection (ignores `read` from script internal pipes).
- Details and justifications in `ANALYSIS_AND_SUGGESTIONS.md`.

## AppImage (simplest)

```bash
chmod +x mtklogo-gui-1.2-x86_64.AppImage
./mtklogo-gui-1.2-x86_64.AppImage
```
* On the first run it creates `~home/mtklogo-gui/original/` and `~home/mtklogo-gui/suggested/` (with a `logo.bin` of **example**). Everything the script generates 
(`logo/`, `out/`, `backup/`) is in these folders. Use **Choose logo.bin…** to bring yours.
* No FUSE (`libfuse2`)? `./mtklogo-gui-1.2-x86_64.AppImage --appimage-extract-and-run`
* Requires glibc ≥ 2.34 (Ubuntu 22.04+, Debian 12+, Fedora 35+, Arch…) because of the `mtklogo` binary. Qt/xcb are built-in.

> [!NOTE]  
> A folder named `~home/mtklogo-gui` is created with two other subfolders `~home/mtklogo-gui/suggested` and `~home/mtklogo-gui/original`.
> Set your selection to `original` or `suggested` so that each subfolder contains the png files from your logo.bin file, located in `~home/mtklogo-gui/suggested/logo` and `~home/mtklogo-gui/original/logo`.
>
> It is in this `/logo` subfolder that you should place your modified png images or modify the png images directly in this subfolder.
>
> <details><summary> Example - Click to open</summary>
> <p>
> <img width="982" height="375" alt="6" src="https://github.com/user-attachments/assets/98037276-cba4-435f-8a82-17fb62a6a423" />
> </p>
> </details>

## From sources

`./run.sh` opens the original pool; **`./run.sh suggested`** opens the suggested set (`suggested/` folder).

Minimalist graphical interface (Python + Qt) for `mtklogos.sh`.

The script runs **exactly as is** (`bash ./mtklogos.sh`): the GUI only captures the output in real time and respond to his questions through dialogue.

### Detection
- The GUI reads `MTKLOGO_GUI_LANG`, `LANGUAGE`, `LC_ALL`, `LC_MESSAGES`, and `LANG`, in that order. To test another language without changing the system:
```bash
MTKLOGO_GUI_LANG=de ./mtklogo-gui-1.2-x86_64.AppImage
```

- All 45 GUI texts are translated in windows and dialogs. The standard Qt buttons (`OK`, `Cancel`, `Yes`, `No`, and `file dialogs`) are also included in `German`, `Spanish`, `French`, and `Brazilian Portuguese`.

> [!NOTE]  
> I had chosen only one language for the AppImage v1.1 to reduce its size and facilitate quick testing and now I've decided include only a few (approximately 840 KB) for further improvements and language choices.
>
> So now all multilingual users can add more languages ​​if they wish.

 * You can read [mtklogo_gui_Claude-AI_prompt2](https://github.com/lopestom/mtklogo/blob/mtklogo_v1.2/mtklogo_gui_Claude-AI_prompt2.md) to understand how to add more languages ​​and, if possible, contribute to the project.
 
## Content

| File | Description |
|---|---|
| `eng.sh` | script Messages of mtklogos.sh (`English = default`) |
| `mtklogos.sh` | Original script (**unchanged**) |
| `mtklogo` | Linux binary x86-64 v1.0.1 (identical to the latest upstream release) |
| `logo.bin` | example `logo.bin` from repository (replace with yours) |
| `suggested/` | `mtklogos.sh` v2, `mtklogo.yaml` with `exp_*` fixes/profiles, `mtklogo` patched |
| `mtklogo-gui-1.2-fonts.zip` | All files from mtklogo_v1.1 (`./run.sh` included) |
| `ANALYSIS_AND_SUGGESTIONS.md` | Script, yaml and source code analysis |

mtklogo-gui-1.2-fonts.zip

## Illustrative images
<details><summary> Screenshots - Click to open</summary>
<p>
<img width="1283" height="824" alt="1" src="https://github.com/user-attachments/assets/70c5ebdf-8124-4e5c-a0e7-bc82e1a4f0c0" />
<img width="1283" height="816" alt="2" src="https://github.com/user-attachments/assets/f6ae8dee-be4f-49fb-9ea2-caf61e66b547" />
<img width="1283" height="816" alt="3" src="https://github.com/user-attachments/assets/9ae7aea9-e1bc-4a88-8698-cbc865ef342f" />
<img width="1284" height="816" alt="4" src="https://github.com/user-attachments/assets/6c158f3d-5623-4f22-b73d-fff05a0258fc" />
<img width="1283" height="816" alt="5" src="https://github.com/user-attachments/assets/03eb7cfe-a87a-4b24-ab9a-a41cab91a2ae" />
</p>
</details>

## To do
If you wish to submit a patch/fix from elsewhere (another project, idea, etc.), it is imperative that you retain ownership of the work of the person you wish to include. This will ensure that credit is given where it is deserved and that [open source principles](http://opensource.org/docs/osd) are respected. Your contribution to the project will still be acknowledged, as you will be permanently listed as a committer.

Read [suggestions-not-applied](https://github.com/lopestom/mtklogo/blob/mtklogo_v1.2/ANALYSIS_AND_SUGGESTIONS.md#suggestions-not-applied) for more ideas and to avoid duplication, or to save time on new ways to contribute.

### Analysis and suggestions from claude.ai
You can read [ANALYSIS_AND_SUGGESTIONS.md](https://github.com/lopestom/mtklogo/blob/mtklogo_v1.2/ANALYSIS_AND_SUGGESTIONS.md) if you want.

## Contributing
The real objective of contributing will be improvements in making the mtklogo binary file simpler, better, smaller and adding more resolutions or new resolutions/sizes/dimensions/colors to correctly decompress the `logo.bin` file.

For more details read first the [CONTRIBUTING.md](https://github.com/lopestom/mtklogo/blob/mtklogo_v1.2/CONTRIBUTING.md) file before send a PR or any modifications.

## Authors
This project would not have been possible without the mtklogo binary file created by @arlept and the modifications/improvements (suggested option) made by @cyberknight777.
