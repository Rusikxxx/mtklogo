#!/usr/bin/env python3
"""
mtklogo GUI - minimalist graphical interface (Qt) for the `mtklogos.sh` script.

The script runs EXACTLY as is (`bash ./mtklogos.sh`), without any modifications
 to its processes. The GUI only:

  * captures stdout+stderr in real time (with ANSI colors);
  * detects when the script is stopped waiting for input (via /proc, reading if
   any process in the tree is blocked in read(0, ...));
  * displays the appropriate dialog:

      - bash `select` menu -> list of options
      - `read` with text -> text field
      - [y/N], (y/n), yes/no -> Yes/No
      - "Press Enter" -> Continue button

  * sends the response to the script's stdin.

Only environment change: COLUMNS=1, so that the bash `select` prints one option
 per line (makes the menu easier to read). It doesn't change the script's logic.

Works with PySide6 (preferred) or PyQt5.
"""
from __future__ import annotations

import codecs
import os
import platform
import re
import shutil
import filecmp
import signal
import subprocess
import sys
import time
from pathlib import Path

import mtklogo_i18n
from mtklogo_i18n import _

try:
    from PySide6 import QtCore, QtGui, QtWidgets
    Signal = QtCore.Signal
    QT_API = "PySide6"
except ImportError:  # pragma: no cover
    try:
        from PyQt5 import QtCore, QtGui, QtWidgets
        Signal = QtCore.pyqtSignal
        QT_API = "PyQt5"
    except ImportError:
        sys.exit("Qt not found. Install it with:  pip install PySide6   (or PyQt5)")

APP_VERSION = "1.2"
SCRIPT_NAME = "mtklogos.sh"
SEED_FILES = ("mtklogo", "mtklogos.sh", "mtklogo.yaml")
SET_LABELS = (
    ("original", "Original (lopestom fork)"),
    ("suggested", "Suggested (script v2 + patched mtklogo + new yaml)"),
)
PS3 = "#? "              # standard `select` prompt in bash
IDLE_SECONDS = 0.15      # Minimum silence on the way out before considering a prompt.

# --------------------------------------------------------------------------- #
#  Process inspection (Linux): who is blocked from reading stdin?
# --------------------------------------------------------------------------- #
_READ_SYSCALL = {"x86_64": 0, "aarch64": 63, "arm64": 63, "riscv64": 63,
                 "i386": 3, "i686": 3, "armv7l": 3, "armv8l": 3}


def _children_map() -> dict[int, list[int]]:
    tree: dict[int, list[int]] = {}
    for entry in os.listdir("/proc"):
        if not entry.isdigit():
            continue
        try:
            with open(f"/proc/{entry}/stat") as fh:
                stat = fh.read()
            ppid = int(stat.rsplit(")", 1)[1].split()[1])
        except (OSError, ValueError, IndexError):
            continue
        tree.setdefault(ppid, []).append(int(entry))
    return tree


def process_tree(root: int) -> list[int]:
    tree, out, stack = _children_map(), [root], [root]
    while stack:
        for child in tree.get(stack.pop(), []):
            out.append(child)
            stack.append(child)
    return out


def stdin_waiters(root: int, stdin_fd: int | None = None):
    """PIDs (from the script and its descendants) are blocked in read() from OUR stdin.

    It only counts if it reads fd 0 *and* whose fd 0 is the same pipe that the GUI opened:
    This ignores `read` from internal script pipes (e.g., `while read ... < <(cmd)`).
    Returns None if it is not possible to inspect (different architecture, /proc
    restricted...). In this case, the GUI uses a time-based heuristic.
    """
    nr = _READ_SYSCALL.get(platform.machine())
    if nr is None:
        return None
    target = None
    if stdin_fd is not None:
        try:
            target = os.readlink(f"/proc/self/fd/{stdin_fd}")
        except OSError:
            target = None
    readable, waiting = False, []
    for pid in process_tree(root):
        try:
            with open(f"/proc/{pid}/syscall") as fh:
                parts = fh.read().split()
        except OSError:
            continue
        readable = True
        if len(parts) >= 2 and parts[0] == str(nr) and parts[1] == "0x0":
            if target is not None:
                try:
                    if os.readlink(f"/proc/{pid}/fd/0") != target:
                        continue
                except OSError:
                    continue
            waiting.append(pid)
    return waiting if readable else None


# --------------------------------------------------------------------------- #
#  Log with ANSI color support and \r
# --------------------------------------------------------------------------- #
_CSI = re.compile(r"\x1b\[([0-?]*)[ -/]*([@-~])")
_PARTIAL_ESC = re.compile(r"\x1b(\[[0-?]*[ -/]*)?\Z")
_OTHER_ESC = re.compile(r"\x1b[()][0-9A-Za-z]|\x1b[=>78]")
_SPLIT = re.compile(r"(\r\n|\n|\r)")

_ANSI_COLORS = {
    30: "#6b7280", 31: "#ff6b6b", 32: "#7ee787", 33: "#e3b341",
    34: "#79a8ff", 35: "#d2a8ff", 36: "#56d4dd", 37: "#d8dee9",
    90: "#9aa4b2", 91: "#ff8f8f", 92: "#9bf2a3", 93: "#f2cc60",
    94: "#a5c4ff", 95: "#e2c5ff", 96: "#7fe6ee", 97: "#ffffff",
}
NOTE_COLOR = "#f0a35e"


class AnsiLog(QtWidgets.QPlainTextEdit):
    """Read-only log area. Maintains `tail` (current line without ANSI code)."""

    def __init__(self, on_line=None):
        super().__init__()
        self.on_line = on_line
        self.setReadOnly(True)
        self.setMaximumBlockCount(50000)
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.setFont(QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.FixedFont))
        self.setStyleSheet("QPlainTextEdit { background:#10141a; color:#d8dee9; }")
        self.reset_state()

    def reset_state(self):
        self.tail = ""
        self._cr = False
        self._carry = ""
        self._fg = None
        self._bold = False

    # -- formatting ---------------------------------------------------------
    def _fmt(self, color=None, bold=None):
        fmt = QtGui.QTextCharFormat()
        color = color or self._fg
        if color:
            fmt.setForeground(QtGui.QColor(color))
        if self._bold if bold is None else bold:
            fmt.setFontWeight(QtGui.QFont.Bold)
        return fmt

    def _sgr(self, params: str):
        codes = [int(p) if p.isdigit() else 0 for p in params.split(";")] or [0]
        i = 0
        while i < len(codes):
            c = codes[i]
            if c == 0:
                self._fg, self._bold = None, False
            elif c == 1:
                self._bold = True
            elif c == 22:
                self._bold = False
            elif c in _ANSI_COLORS:
                self._fg = _ANSI_COLORS[c]
            elif c == 39:
                self._fg = None
            elif c in (38, 48):          # Extended color: ignores arguments
                i += 2 if i + 1 < len(codes) and codes[i + 1] == 5 else 4
            i += 1

    # -- writing ------------------------------------------------------------
    def _insert(self, text: str, fmt=None):
        cur = self.textCursor()
        cur.movePosition(QtGui.QTextCursor.End)
        cur.insertText(text, fmt or self._fmt())

    def _newline(self):
        line = self.tail
        self._insert("\n", QtGui.QTextCharFormat())
        self.tail, self._cr = "", False
        if self.on_line:
            self.on_line(line)

    def _text(self, text: str):
        if self._cr:                      # '\r' isolated: overwrites the line
            cur = self.textCursor()
            cur.movePosition(QtGui.QTextCursor.End)
            cur.movePosition(QtGui.QTextCursor.StartOfBlock, QtGui.QTextCursor.KeepAnchor)
            cur.removeSelectedText()
            self.tail, self._cr = "", False
        self._insert(text)
        self.tail += text

    def _emit(self, segment: str):
        for part in _SPLIT.split(segment):
            if part in ("\n", "\r\n"):
                self._newline()
            elif part == "\r":
                self._cr = True
            elif part:
                self._text(part)

    def feed(self, text: str):
        sb = self.verticalScrollBar()
        at_bottom = sb.value() >= sb.maximum() - 4
        text, self._carry = self._carry + text, ""
        m = _PARTIAL_ESC.search(text)
        if m:                              # ANSI sequence cut in half
            self._carry, text = text[m.start():], text[:m.start()]
        text = _OTHER_ESC.sub("", text)
        pos = 0
        for m in _CSI.finditer(text):
            self._emit(text[pos:m.start()])
            if m.group(2) == "m":
                self._sgr(m.group(1))
            pos = m.end()
        self._emit(text[pos:])
        if at_bottom:
            sb.setValue(sb.maximum())

    def note(self, text: str):
        """Write a note (e.g., "answer sent") and break the line."""
        self._insert(text + "\n", self._fmt(NOTE_COLOR, True))
        self.tail, self._cr = "", False
        sb = self.verticalScrollBar()
        sb.setValue(sb.maximum())


# --------------------------------------------------------------------------- #
#  Reading the process in thread
# --------------------------------------------------------------------------- #
class Reader(QtCore.QThread):
    chunk = Signal(bytes)
    done = Signal(int)

    def __init__(self, proc: subprocess.Popen, parent=None):
        super().__init__(parent)
        self.proc = proc

    def run(self):
        fd = self.proc.stdout.fileno()
        while True:
            try:
                data = os.read(fd, 65536)
            except OSError:
                break
            if not data:
                break
            self.chunk.emit(data)
        self.done.emit(self.proc.wait())


# --------------------------------------------------------------------------- #
#  Menu/Question Detection
# --------------------------------------------------------------------------- #
_MENU_START = re.compile(r"^\s*\d+\) ")
_MENU_ITEM = re.compile(r"(\d+)\) (.*?)(?=\s{2,}\d+\) |\s*$)")
_YES_NO = re.compile(
    r"[\[(]\s*(y(?:es)?|s(?:im|í|i)?|j(?:a)?|o(?:ui)?)\s*/\s*(n(?:o|ão|ao|ein|on)?)\s*[\])]", re.IGNORECASE)
_ENTER = re.compile(
    r"(press|hit|pressione|tecle|aperte|pulse|presione|appuyez)\W+(the\s+|sur\s+|la\s+tecla\s+)?(enter|return|entrée|entree|intro)"
    r"|eingabetaste|enter-taste|any key|qualquer tecla|cualquier tecla|toute touche|beliebige taste",
    re.IGNORECASE)


def parse_menu_line(line: str):
    if not _MENU_START.match(line):
        return []
    return [(int(n), label.strip()) for n, label in _MENU_ITEM.findall(line)]


def install_qt_translations(app, base, locale, bundle, here):
    """Instala qtbase_<idioma>.qm (textos padrão do Qt: OK, Cancel, Yes, No, diálogos de arquivo...)."""
    dirs = [d for d in ((bundle / "qt-translations") if bundle else None, here / "qt-translations") if d and d.is_dir()]
    try:
        dirs.append(Path(QtCore.QLibraryInfo.path(QtCore.QLibraryInfo.TranslationsPath)))      # PySide6
    except AttributeError:
        dirs.append(Path(QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)))  # PyQt5
    if base == "en":
        return None
    qloc = QtCore.QLocale("pt_BR" if base == "pt" else locale)
    tr = QtCore.QTranslator(app)
    for d in dirs:
        if tr.load(qloc, "qtbase", "_", str(d)):
            app.installTranslator(tr)
            return tr
    return None


# --------------------------------------------------------------------------- #
#  Writable workspace (AppImage is read-only)
# --------------------------------------------------------------------------- #
def find_bundle() -> Path | None:
    """Folder containing the bundled file sets. (AppImage or ./bundle)."""
    candidates = []
    if os.environ.get("APPDIR"):
        candidates.append(Path(os.environ["APPDIR"]) / "usr/share/mtklogo-gui")
    candidates.append(Path(__file__).resolve().parent / "bundle")
    return next((c for c in candidates if (c / "original").is_dir()), None)


def seed_workspace(bundle: Path, root: Path) -> dict:
        """Copy the packaged files to ~/mtklogo-gui/<set>/ (without touching
        in logo.bin/logo/out/user backup). In a new version of the app, overwrite
        mtklogo/mtklogos.sh/mtklogo.yaml saving .bak of what the user has edited."""
    sets = {}
    for key, label in SET_LABELS:
        src, dst = bundle / key, root / key
        if not src.is_dir():
            continue
        dst.mkdir(parents=True, exist_ok=True)
        stamp = dst / ".seed_version"
        fresh = not stamp.exists() or stamp.read_text().strip() != APP_VERSION
        for name in SEED_FILES:
            s_, d_ = src / name, dst / name
            if not s_.exists():
                continue
            if not d_.exists():
                shutil.copy2(s_, d_)
            elif fresh and not filecmp.cmp(s_, d_, shallow=False):
                if name != "mtklogo":
                    shutil.copy2(d_, d_.with_name(name + ".bak"))
                shutil.copy2(s_, d_)
            if name in ("mtklogo", "mtklogos.sh"):
                d_.chmod(0o755)
        if (src / "lang").is_dir() and (fresh or not (dst / "lang").is_dir()):
            shutil.copytree(src / "lang", dst / "lang", dirs_exist_ok=True)
        sample = bundle / "example" / "logo.bin"
        if sample.exists() and not (dst / "logo.bin").exists():
            shutil.copy2(sample, dst / "logo.bin")
        stamp.write_text(APP_VERSION)
        sets[_(label)] = dst
    return sets


# --------------------------------------------------------------------------- #
#  Main window
# --------------------------------------------------------------------------- #
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, workdir: Path, sets: dict | None = None):
        super().__init__()
        self.setWindowTitle("mtklogo GUI")
        self.sets = sets or {}
        self.resize(900, 620)

        self.workdir = workdir
        self.proc = None
        self.reader = None
        self._running = False
        self._dialog_open = False
        self._reset_run_state()

        # --- widgets
        self.dir_edit = QtWidgets.QLineEdit(str(workdir))
        self.dir_edit.setReadOnly(True)
        self.btn_dir = QtWidgets.QPushButton(_("Folder…"))
        self.btn_open = QtWidgets.QPushButton(_("Open"))
        self.btn_logo = QtWidgets.QPushButton(_("Choose logo.bin…"))
        self.combo = None
        if self.sets:
            self.combo = QtWidgets.QComboBox()
            self.combo.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
            self.combo.setMinimumContentsLength(22)
            for label, path in self.sets.items():
                self.combo.addItem(label, str(path))
            self.combo.currentIndexChanged.connect(self._set_changed)
        self.log = AnsiLog(on_line=self._on_line)
        self.btn_run = QtWidgets.QPushButton(_("▶  Run mtklogos.sh"))
        self.btn_stop = QtWidgets.QPushButton(_("■  Stop"))
        self.btn_clear = QtWidgets.QPushButton(_("Clear"))
        self.input = QtWidgets.QLineEdit()
        self.input.setPlaceholderText(_("Manual input for the script (Press Enter to sends)"))
        self.btn_send = QtWidgets.QPushButton(_("Send"))

        top = QtWidgets.QHBoxLayout()
        top.addWidget(QtWidgets.QLabel(_("Set:") if self.combo else _("Working folder:")))
        if self.combo:
            top.addWidget(self.combo)
        top.addWidget(self.dir_edit, 1)
        top.addWidget(self.btn_dir)
        top.addWidget(self.btn_open)
        top.addWidget(self.btn_logo)

        bottom = QtWidgets.QHBoxLayout()
        bottom.addWidget(self.btn_run)
        bottom.addWidget(self.btn_stop)
        bottom.addWidget(self.btn_clear)
        bottom.addSpacing(16)
        bottom.addWidget(self.input, 1)
        bottom.addWidget(self.btn_send)

        root = QtWidgets.QVBoxLayout()
        root.addLayout(top)
        root.addWidget(self.log, 1)
        root.addLayout(bottom)
        central = QtWidgets.QWidget()
        central.setLayout(root)
        self.setCentralWidget(central)
        self.statusBar().showMessage(_("Ready."))

        # --- signs
        self.btn_run.clicked.connect(self.start)
        self.btn_stop.clicked.connect(self.stop)
        self.btn_clear.clicked.connect(self.log.clear)
        self.btn_dir.clicked.connect(self.choose_dir)
        self.btn_open.clicked.connect(self.open_dir)
        self.btn_logo.clicked.connect(self.choose_logo)
        self.btn_send.clicked.connect(self._manual_send)
        self.input.returnPressed.connect(self._manual_send)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self._poll)

        self._update_buttons()

    # ------------------------------------------------------------------ state
    def _reset_run_state(self):
        self._menu_buf: list = []
        self._pending_menu = None
        self._menus: dict = {}
        self._menu_stack: list = []
        self._last_line = ""
        self._last_data = time.monotonic()
        self._need_new_data = False
        self._sent_at = 0.0
        self._decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")

    def _update_buttons(self):
        run = self._running
        self.btn_run.setEnabled(not run)
        self.btn_stop.setEnabled(run)
        self.btn_dir.setEnabled(not run)
        self.btn_logo.setEnabled(not run)
        if self.combo:
            self.combo.setEnabled(not run)
        self.btn_send.setEnabled(run)
        self.input.setEnabled(run)

    def _status(self, msg: str):
        self.statusBar().showMessage(msg)

    # ------------------------------------------------------------ folder / actions
    def choose_dir(self):
        d = QtWidgets.QFileDialog.getExistingDirectory(
            self, _("Folder with mtklogos.sh, mtklogo and logo.bin"), str(self.workdir))
        if d:
            self.workdir = Path(d)
            self.dir_edit.setText(d)
            if self.combo:
                self.combo.blockSignals(True)
                idx = self.combo.findText(_("Custom"))
                if idx < 0:
                    self.combo.addItem(_("Custom"), d)
                    idx = self.combo.count() - 1
                self.combo.setItemData(idx, d)
                self.combo.setCurrentIndex(idx)
                self.combo.blockSignals(False)

    def _set_changed(self, _index):
        path = self.combo.currentData()
        if path:
            self.workdir = Path(path)
            self.dir_edit.setText(path)

    def choose_logo(self):
        f, _filter = QtWidgets.QFileDialog.getOpenFileName(
            self, _("Choose your logo.bin"), str(Path.home()), _("Logo images (*.bin);;All files (*)"))
        if not f:
            return
        dest = self.workdir / "logo.bin"
        if dest.exists() and not filecmp.cmp(f, dest, shallow=False):
            r = QtWidgets.QMessageBox.question(
                self, _("Replace logo.bin?"),
                _("A logo.bin already exists in:\n{path}\n\nReplace it with the selected file?\n(the original, if already used by the script, is kept in backup/)",
                  path=self.workdir))
            if r != QtWidgets.QMessageBox.Yes:
                return
        try:
            shutil.copy2(f, dest)
        except OSError as exc:
            QtWidgets.QMessageBox.critical(self, _("Copy error"), str(exc))
            return
        self._status(_("logo.bin copied to {path}", path=self.workdir))

    def open_dir(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(str(self.workdir)))

    # -------------------------------------------------------------- executar
    def start(self):
        if self._running:
            return
        script = self.workdir / SCRIPT_NAME
        if not script.is_file():
            QtWidgets.QMessageBox.critical(
                self, _("Script not found"),
                _("{script} does not exist in:\n{path}\n\nUse “Folder…” to choose the correct folder.",
                  script=SCRIPT_NAME, path=self.workdir))
            return
        self.log.clear()
        self.log.reset_state()
        self._reset_run_state()
        env = os.environ.copy()
        env["COLUMNS"] = "1"          # `select` prints one option per line.
        env["MTKLOGO_GUI_LANG"] = mtklogo_i18n.LANG   # The v2 script speaks the same language as the GUI.
        try:
            self.proc = subprocess.Popen(
                ["bash", f"./{SCRIPT_NAME}"], cwd=str(self.workdir), env=env,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, bufsize=0, start_new_session=True)
        except OSError as exc:
            QtWidgets.QMessageBox.critical(self, _("Start error"), str(exc))
            return
        self._running = True
        self.reader = Reader(self.proc, self)
        self.reader.chunk.connect(self._on_chunk)
        self.reader.done.connect(self._on_done)
        self.reader.start()
        self.timer.start()
        self._update_buttons()
        self._status(_("Running {script} (PID {pid})…", script=SCRIPT_NAME, pid=self.proc.pid))

    def stop(self):
        if not self._running or self.proc is None:
            return
        self._signal_group(signal.SIGTERM)
        QtCore.QTimer.singleShot(2000, lambda: self._signal_group(signal.SIGKILL))
        self._status(_("Stopping the script…"))

    def _signal_group(self, sig):
        if self.proc is not None and self.proc.poll() is None:
            try:
                os.killpg(self.proc.pid, sig)
            except (ProcessLookupError, PermissionError):
                pass

    # ------------------------------------------------------------ real-time output
    def _on_chunk(self, data: bytes):
        self._last_data = time.monotonic()
        self._need_new_data = False
        self.log.feed(self._decoder.decode(data))

    def _on_done(self, code: int):
        tail = self._decoder.decode(b"", final=True)
        if tail:
            self.log.feed(tail)
        self.timer.stop()
        self._running = False
        self._menu_buf = []
        if self.log.tail:
            self.log.feed("\n")
        self.log.note(_("— Script finished (exit code {code}) —", code=code))
        self._status(_("Finished (code {code}).", code=code))
        self._update_buttons()

    def _on_line(self, line: str):
        items = parse_menu_line(line)
        if items:
            self._menu_buf.extend(items)
            return
        self._finalize_menu()
        if line.strip():
            self._last_line = line.strip()

    def _finalize_menu(self):
        if self._menu_buf:
            self._pending_menu = sorted(dict(self._menu_buf).items())
            self._menu_buf = []

    # --------------------------------------------------------- detect prompts
    def _poll(self):
        if not self._running or self._dialog_open or self.proc is None:
            return
        now = time.monotonic()
        if now - self._last_data < IDLE_SECONDS:
            return
        waiters = stdin_waiters(self.proc.pid, self.proc.stdin.fileno())
        if self._need_new_data:
            # Response sent; just ask again if the script has gone back to waiting.
            if waiters and now - self._sent_at > 0.6:
                self._need_new_data = False
            else:
                return
        tail = self.log.tail
        if waiters is None:                       # without /proc: time heuristic
            if not tail.strip() or now - self._last_data < 1.0:
                return
        elif not waiters:                         # Something is still working.
            return
        self._handle_prompt(tail, waiters[-1] if waiters else None)

    def _handle_prompt(self, tail: str, pid):
        self._finalize_menu()
        is_select = tail.endswith(PS3)
        menu = None
        if is_select:
            key = pid if pid is not None else "?"
            if self._pending_menu:
                self._menus[key] = self._pending_menu
                self._menu_stack.append(self._pending_menu)
                self._pending_menu = None
            menu = self._menus.get(key)
            if menu is None and pid is None and self._menu_stack:
                menu = self._menu_stack[-1]
        self._dialog_open = True
        self._status(_("Waiting for your answer…"))
        try:
            answer = self._ask_until_answered(tail, is_select, menu)
        finally:
            self._dialog_open = False
        if answer is None:
            self.stop()
            return
        if self._running:
            self._send(*answer)
            self._status(_("Running…"))

    def _ask_until_answered(self, tail, is_select, menu):
        """Returns (sent_text, displayed_text) or None if the user cancels."""
        while True:
            plain = tail.strip()
            if is_select and menu:
                res = self.ask_choice(menu)
                answer = (str(res[0]), f"{res[0]}  ({res[1]})") if res else None
            elif is_select:
                text = self.ask_text(_("The script asks for the number of an option:"))
                answer = (text, text) if text is not None else None
            elif (m := _YES_NO.search(plain)):
                yes, no = m.group(1).lower(), m.group(2).lower()
                r = self.ask_yes_no(plain)
                answer = ((yes, yes) if r else (no, no)) if r is not None else None
            elif _ENTER.search(plain):
                answer = ("", "⏎") if self.ask_enter(plain) else None
            else:
                label = plain or self._last_line or _("The script is waiting for input:")
                text = self.ask_text(label)
                answer = (text, text) if text is not None else None
            if answer is not None:
                return answer
            r = QtWidgets.QMessageBox.question(
                self, _("Cancel?"),
                _("Cancelling stops the script.\nDo you really want to stop the  running process?"))
            if r == QtWidgets.QMessageBox.Yes:
                return None

    # ---------------------------------------------------------------- dialogues
    def ask_choice(self, menu):
        dlg = QtWidgets.QDialog(self)
        dlg.setWindowTitle(_("The script asks for a choice"))
        lst = QtWidgets.QListWidget()
        for num, label in menu:
            item = QtWidgets.QListWidgetItem(f"{num})  {label}")
            item.setData(QtCore.Qt.UserRole, (num, label))
            lst.addItem(item)
        lst.setCurrentRow(0)
        box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        box.accepted.connect(dlg.accept)
        box.rejected.connect(dlg.reject)
        lst.itemActivated.connect(lambda _i: dlg.accept())
        lay = QtWidgets.QVBoxLayout(dlg)
        lay.addWidget(QtWidgets.QLabel(_("Select an option:")))
        lay.addWidget(lst)
        lay.addWidget(box)
        dlg.resize(360, min(150 + 26 * len(menu), 560))
        if dlg.exec() and lst.currentItem():
            return lst.currentItem().data(QtCore.Qt.UserRole)
        return None

    def ask_text(self, label: str):
        text, ok = QtWidgets.QInputDialog.getText(
            self, _("The script asks for a value"), label.strip() or _("Input:"))
        return text.strip() if ok else None

    def ask_yes_no(self, question: str):
        r = QtWidgets.QMessageBox.question(
            self, _("Script confirmation"), question,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No)
        return r == QtWidgets.QMessageBox.Yes

    def ask_enter(self, text: str):
        box = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Information, _("The script is waiting"), text,
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel, self)
        box.button(QtWidgets.QMessageBox.Ok).setText(_("Continue"))
        return box.exec() == QtWidgets.QMessageBox.Ok

    # ------------------------------------------------------------------- send
    def _send(self, text: str, shown: str | None = None):
        if not self._running or self.proc is None or self.proc.stdin is None:
            return
        try:
            self.proc.stdin.write((text + "\n").encode())
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError, ValueError):
            self._status(_("Failed to send: the script is no longer reading input."))
            return
        self.log.note(shown if shown is not None else text)
        self._need_new_data = True
        self._sent_at = time.monotonic()

    def _manual_send(self):
        if self._running:
            self._send(self.input.text())
            self.input.clear()

    # ------------------------------------------------------------------ close
    def closeEvent(self, event):
        if self._running:
            r = QtWidgets.QMessageBox.question(
                self, _("Script running"),
                _("The script is still running. Stop it and quit?"))
            if r != QtWidgets.QMessageBox.Yes:
                event.ignore()
                return
            self._signal_group(signal.SIGKILL)
            if self.reader:
                self.reader.wait(3000)
        event.accept()


def main():
    if sys.platform != "linux":
        print(_("Warning: this program was made for Linux."), file=sys.stderr)
    here = Path(__file__).resolve().parent
    explicit = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else None
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("mtklogo GUI")
    bundle = find_bundle()
    home = Path(os.environ.get("MTKLOGO_GUI_HOME", Path.home() / "mtklogo-gui"))
    extra = [home / "lang"] + ([bundle / "lang"] if bundle else [])
    base, loc = mtklogo_i18n.detect_language(extra, QtCore.QLocale.system().name())
    mtklogo_i18n.set_language(base, loc, extra)
    translator = install_qt_translations(app, base, loc, bundle, here)   # Qt's OK/Cancel/Yes/No buttons
    sets, workdir = {}, explicit or here
    if bundle and explicit is None:
        sets = seed_workspace(bundle, home)
        workdir = next(iter(sets.values()), here)
    win = MainWindow(workdir, sets)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
