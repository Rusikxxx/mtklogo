## Script v2
The prompts in suggested/mtklogos.sh follow the same language as the GUI, and questions become [y/N], [s/N], [j/N] or [o/N].

### Add another language (without recompiling)
For example, for Italian (it):
* Create `~home/mtklogo-gui/lang/it.json` with {"English text": "translation"}. The keys are in CATALOG["en"], in the mtklogo_i18n.py file.

  - Optional: copy `~home/mtklogo-gui/suggested/lang/en.sh` to `~home/mtklogo-gui/lang/it.sh` and translate.

The missing words will appear in English.

### Details to know
1) If you have already used version 1.1, when opening version 1.2 the files in `~home/mtklogo-gui/suggested/` auto updated.

2) The AppImage menu shortcut now has a name and description in all five languages.

### Files:

mtklogo-gui-1.2-x86_64.AppImage
mtklogo-gui-1.2-x86_64.AppImage.sha256
mtklogo-gui-1.2-fonts.zip
ANALYSIS_AND_SUGGESTIONS.md
suggested/mtklogos.sh
suggested/lang/en.sh
