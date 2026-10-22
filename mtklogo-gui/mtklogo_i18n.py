"""
Lightweight translation for the mtklogo GUI (without gettext/lrelease).

* The source text is ENGLISH: if there is no translation, it appears in English.
* Detected language (in this order): MTKLOGO_GUI_LANG, LANGUAGE, LC_ALL, LC_MESSAGES,
  LANG and, finally, the system language according to Qt. Ex.: MTKLOGO_GUI_LANG=de ./app
* Built-in catalogs: pt, de, es, fr.
* To ADD a language without recompiling: create ~/mtklogo-gui/lang/<code>.json
  with {"English text": "translation", ...} (copy the CATALOG["de"] keys below).
  The same applies to script v2: ~/mtklogo-gui/lang/<code>.sh (see suggested /lang/).
"""
from __future__ import annotations

import json
import os
from pathlib import Path

CATALOG: dict[str, dict[str, str]] = {
    "pt": {
        "Original (lopestom fork)": "Original (fork lopestom)",
        "Suggested (script v2 + patched mtklogo + new yaml)": "Sugerido (script v2 + mtklogo patchado + yaml novo)",
        "Folder…": "Pasta…",
        "Open": "Abrir",
        "Choose logo.bin…": "Escolher logo.bin…",
        "▶  Run mtklogos.sh": "▶  Executar mtklogos.sh",
        "■  Stop": "■  Parar",
        "Clear": "Limpar",
        "Manual input for the script (Enter sends)": "Entrada manual para o script (Enter envia)",
        "Send": "Enviar",
        "Set:": "Conjunto:",
        "Working folder:": "Pasta de trabalho:",
        "Ready.": "Pronto.",
        "Folder with mtklogos.sh, mtklogo and logo.bin": "Pasta com mtklogos.sh, mtklogo e logo.bin",
        "Custom": "Personalizada",
        "Choose your logo.bin": "Escolha o seu logo.bin",
        "Logo images (*.bin);;All files (*)": "Imagens de logo (*.bin);;Todos os arquivos (*)",
        "Replace logo.bin?": "Substituir logo.bin?",
        "A logo.bin already exists in:\n{path}\n\nReplace it with the selected file?\n(the original, if already used by the script, is kept in backup/)":
            "Já existe um logo.bin em:\n{path}\n\nSubstituir pelo arquivo escolhido?\n(o original, se já usado pelo script, fica guardado em backup/)",
        "Copy error": "Erro ao copiar",
        "logo.bin copied to {path}": "logo.bin copiado para {path}",
        "Script not found": "Script não encontrado",
        "{script} does not exist in:\n{path}\n\nUse “Folder…” to choose the correct folder.":
            "{script} não existe em:\n{path}\n\nUse “Pasta…” para escolher a pasta correta.",
        "Start error": "Erro ao iniciar",
        "Running {script} (PID {pid})…": "Executando {script} (PID {pid})…",
        "Stopping the script…": "Encerrando o script…",
        "— Script finished (exit code {code}) —": "— Script finalizado (código de saída {code}) —",
        "Finished (code {code}).": "Finalizado (código {code}).",
        "Waiting for your answer…": "Aguardando sua resposta…",
        "Running…": "Executando…",
        "The script asks for the number of an option:": "O script pede o número de uma opção:",
        "The script is waiting for input:": "O script está aguardando uma entrada:",
        "Cancel?": "Cancelar?",
        "Cancelling stops the script.\nDo you really want to stop the execution?":
            "Cancelar encerra o script.\nDeseja realmente parar a execução?",
        "The script asks for a choice": "O script pede uma escolha",
        "Select an option:": "Selecione uma opção:",
        "The script asks for a value": "O script pede um valor",
        "Input:": "Entrada:",
        "Script confirmation": "Confirmação do script",
        "The script is waiting": "O script aguarda",
        "Continue": "Continuar",
        "Failed to send: the script is no longer reading input.": "Falha ao enviar: o script não está mais lendo a entrada.",
        "Script running": "Script em execução",
        "The script is still running. Stop it and quit?": "O script ainda está rodando. Encerrar e sair?",
        "Warning: this program was made for Linux.": "Aviso: este programa foi feito para Linux.",
    },
    "de": {
        "Original (lopestom fork)": "Original (lopestom-Fork)",
        "Suggested (script v2 + patched mtklogo + new yaml)": "Vorschlag (Skript v2 + gepatchtes mtklogo + neue yaml)",
        "Folder…": "Ordner…",
        "Open": "Öffnen",
        "Choose logo.bin…": "logo.bin wählen…",
        "▶  Run mtklogos.sh": "▶  mtklogos.sh ausführen",
        "■  Stop": "■  Stopp",
        "Clear": "Leeren",
        "Manual input for the script (Enter sends)": "Manuelle Eingabe für das Skript (Enter sendet)",
        "Send": "Senden",
        "Set:": "Variante:",
        "Working folder:": "Arbeitsordner:",
        "Ready.": "Bereit.",
        "Folder with mtklogos.sh, mtklogo and logo.bin": "Ordner mit mtklogos.sh, mtklogo und logo.bin",
        "Custom": "Benutzerdefiniert",
        "Choose your logo.bin": "Wählen Sie Ihre logo.bin",
        "Logo images (*.bin);;All files (*)": "Logo-Images (*.bin);;Alle Dateien (*)",
        "Replace logo.bin?": "logo.bin ersetzen?",
        "A logo.bin already exists in:\n{path}\n\nReplace it with the selected file?\n(the original, if already used by the script, is kept in backup/)":
            "In diesem Ordner existiert bereits eine logo.bin:\n{path}\n\nMit der gewählten Datei ersetzen?\n(Das Original wird, falls vom Skript schon verwendet, in backup/ aufbewahrt)",
        "Copy error": "Kopierfehler",
        "logo.bin copied to {path}": "logo.bin nach {path} kopiert",
        "Script not found": "Skript nicht gefunden",
        "{script} does not exist in:\n{path}\n\nUse “Folder…” to choose the correct folder.":
            "{script} existiert nicht in:\n{path}\n\nWählen Sie über „Ordner…“ den richtigen Ordner.",
        "Start error": "Startfehler",
        "Running {script} (PID {pid})…": "{script} läuft (PID {pid})…",
        "Stopping the script…": "Skript wird beendet…",
        "— Script finished (exit code {code}) —": "— Skript beendet (Exit-Code {code}) —",
        "Finished (code {code}).": "Beendet (Code {code}).",
        "Waiting for your answer…": "Warte auf Ihre Antwort…",
        "Running…": "Läuft…",
        "The script asks for the number of an option:": "Das Skript fragt nach der Nummer einer Option:",
        "The script is waiting for input:": "Das Skript wartet auf eine Eingabe:",
        "Cancel?": "Abbrechen?",
        "Cancelling stops the script.\nDo you really want to stop the execution?":
            "Abbrechen beendet das Skript.\nWollen Sie die Ausführung wirklich stoppen?",
        "The script asks for a choice": "Das Skript verlangt eine Auswahl",
        "Select an option:": "Wählen Sie eine Option:",
        "The script asks for a value": "Das Skript verlangt einen Wert",
        "Input:": "Eingabe:",
        "Script confirmation": "Bestätigung des Skripts",
        "The script is waiting": "Das Skript wartet",
        "Continue": "Weiter",
        "Failed to send: the script is no longer reading input.": "Senden fehlgeschlagen: Das Skript liest keine Eingabe mehr.",
        "Script running": "Skript läuft",
        "The script is still running. Stop it and quit?": "Das Skript läuft noch. Beenden und schließen?",
        "Warning: this program was made for Linux.": "Warnung: Dieses Programm wurde für Linux entwickelt.",
    },
    "es": {
        "Original (lopestom fork)": "Original (fork de lopestom)",
        "Suggested (script v2 + patched mtklogo + new yaml)": "Sugerido (script v2 + mtklogo parcheado + yaml nuevo)",
        "Folder…": "Carpeta…",
        "Open": "Abrir",
        "Choose logo.bin…": "Elegir logo.bin…",
        "▶  Run mtklogos.sh": "▶  Ejecutar mtklogos.sh",
        "■  Stop": "■  Detener",
        "Clear": "Limpiar",
        "Manual input for the script (Enter sends)": "Entrada manual para el script (Enter envía)",
        "Send": "Enviar",
        "Set:": "Conjunto:",
        "Working folder:": "Carpeta de trabajo:",
        "Ready.": "Listo.",
        "Folder with mtklogos.sh, mtklogo and logo.bin": "Carpeta con mtklogos.sh, mtklogo y logo.bin",
        "Custom": "Personalizada",
        "Choose your logo.bin": "Elija su logo.bin",
        "Logo images (*.bin);;All files (*)": "Imágenes de logo (*.bin);;Todos los archivos (*)",
        "Replace logo.bin?": "¿Reemplazar logo.bin?",
        "A logo.bin already exists in:\n{path}\n\nReplace it with the selected file?\n(the original, if already used by the script, is kept in backup/)":
            "Ya existe un logo.bin en:\n{path}\n\n¿Reemplazarlo por el archivo elegido?\n(el original, si el script ya lo usó, se conserva en backup/)",
        "Copy error": "Error al copiar",
        "logo.bin copied to {path}": "logo.bin copiado a {path}",
        "Script not found": "Script no encontrado",
        "{script} does not exist in:\n{path}\n\nUse “Folder…” to choose the correct folder.":
            "{script} no existe en:\n{path}\n\nUse «Carpeta…» para elegir la carpeta correcta.",
        "Start error": "Error al iniciar",
        "Running {script} (PID {pid})…": "Ejecutando {script} (PID {pid})…",
        "Stopping the script…": "Deteniendo el script…",
        "— Script finished (exit code {code}) —": "— Script finalizado (código de salida {code}) —",
        "Finished (code {code}).": "Finalizado (código {code}).",
        "Waiting for your answer…": "Esperando su respuesta…",
        "Running…": "Ejecutando…",
        "The script asks for the number of an option:": "El script pide el número de una opción:",
        "The script is waiting for input:": "El script espera una entrada:",
        "Cancel?": "¿Cancelar?",
        "Cancelling stops the script.\nDo you really want to stop the execution?":
            "Cancelar detiene el script.\n¿Realmente desea detener la ejecución?",
        "The script asks for a choice": "El script pide una elección",
        "Select an option:": "Seleccione una opción:",
        "The script asks for a value": "El script pide un valor",
        "Input:": "Entrada:",
        "Script confirmation": "Confirmación del script",
        "The script is waiting": "El script espera",
        "Continue": "Continuar",
        "Failed to send: the script is no longer reading input.": "Error al enviar: el script ya no lee la entrada.",
        "Script running": "Script en ejecución",
        "The script is still running. Stop it and quit?": "El script sigue en ejecución. ¿Detenerlo y salir?",
        "Warning: this program was made for Linux.": "Aviso: este programa fue hecho para Linux.",
    },
    "fr": {
        "Original (lopestom fork)": "Original (fork de lopestom)",
        "Suggested (script v2 + patched mtklogo + new yaml)": "Suggéré (script v2 + mtklogo corrigé + nouveau yaml)",
        "Folder…": "Dossier…",
        "Open": "Ouvrir",
        "Choose logo.bin…": "Choisir logo.bin…",
        "▶  Run mtklogos.sh": "▶  Lancer mtklogos.sh",
        "■  Stop": "■  Arrêter",
        "Clear": "Effacer",
        "Manual input for the script (Enter sends)": "Saisie manuelle pour le script (Entrée envoie)",
        "Send": "Envoyer",
        "Set:": "Variante :",
        "Working folder:": "Dossier de travail :",
        "Ready.": "Prêt.",
        "Folder with mtklogos.sh, mtklogo and logo.bin": "Dossier contenant mtklogos.sh, mtklogo et logo.bin",
        "Custom": "Personnalisé",
        "Choose your logo.bin": "Choisissez votre logo.bin",
        "Logo images (*.bin);;All files (*)": "Images de logo (*.bin);;Tous les fichiers (*)",
        "Replace logo.bin?": "Remplacer logo.bin ?",
        "A logo.bin already exists in:\n{path}\n\nReplace it with the selected file?\n(the original, if already used by the script, is kept in backup/)":
            "Un logo.bin existe déjà dans :\n{path}\n\nLe remplacer par le fichier choisi ?\n(l'original, s'il a déjà servi au script, est conservé dans backup/)",
        "Copy error": "Erreur de copie",
        "logo.bin copied to {path}": "logo.bin copié vers {path}",
        "Script not found": "Script introuvable",
        "{script} does not exist in:\n{path}\n\nUse “Folder…” to choose the correct folder.":
            "{script} n'existe pas dans :\n{path}\n\nUtilisez « Dossier… » pour choisir le bon dossier.",
        "Start error": "Erreur de démarrage",
        "Running {script} (PID {pid})…": "Exécution de {script} (PID {pid})…",
        "Stopping the script…": "Arrêt du script…",
        "— Script finished (exit code {code}) —": "— Script terminé (code de sortie {code}) —",
        "Finished (code {code}).": "Terminé (code {code}).",
        "Waiting for your answer…": "En attente de votre réponse…",
        "Running…": "En cours…",
        "The script asks for the number of an option:": "Le script demande le numéro d'une option :",
        "The script is waiting for input:": "Le script attend une saisie :",
        "Cancel?": "Annuler ?",
        "Cancelling stops the script.\nDo you really want to stop the execution?":
            "Annuler arrête le script.\nVoulez-vous vraiment arrêter l'exécution ?",
        "The script asks for a choice": "Le script demande un choix",
        "Select an option:": "Sélectionnez une option :",
        "The script asks for a value": "Le script demande une valeur",
        "Input:": "Saisie :",
        "Script confirmation": "Confirmation du script",
        "The script is waiting": "Le script attend",
        "Continue": "Continuer",
        "Failed to send: the script is no longer reading input.": "Échec de l'envoi : le script ne lit plus la saisie.",
        "Script running": "Script en cours",
        "The script is still running. Stop it and quit?": "Le script est toujours en cours. L'arrêter et quitter ?",
        "Warning: this program was made for Linux.": "Attention : ce programme est conçu pour Linux.",
    },
    "ru": {
        "Original (lopestom fork)": "Оригинал (fork от lopestom)",
        "Suggested (script v2 + patched mtklogo + new yaml)": "Предложенный (script v2 + mtklogo patchado + yaml novo)",
        "Folder…": "Папка…",
        "Open": "Открыть",
        "Choose logo.bin…": "Выберите logo.bin…",
        "▶  Run mtklogos.sh": "▶  Начать mtklogos.sh",
        "■  Stop": "■  Стоп",
        "Clear": "Очистить",
        "Manual input for the script (Enter sends)": "Ручной ввод в скрипт (Enter отправить)",
        "Send": "Отправить",
        "Set:": "Выбрать:",
        "Working folder:": "Рабочая папка:",
        "Ready.": "Готово.",
        "Folder with mtklogos.sh, mtklogo and logo.bin": "Папка с mtklogos.sh , mtklogo и logo.bin",
        "Custom": "Пользовательский",
        "Choose your logo.bin": "Выберите свой logo.bin",
        "Logo images (*.bin);;All files (*)": "Изображения логотипа (*.bin);;Все файлы (*)",
        "Replace logo.bin?": "Заменить logo.bin?",
        "A logo.bin already exists in:\n{path}\n\nReplace it with the selected file?\n(the original, if already used by the script, is kept in backup/)":
            "Уже существует файл logo.bin:\n{path}\n\nЗаменить выбранным файлом?\n(исходный файл, если он уже используется скриптом, сохраняется в папке backup/)",
        "Copy error": "Ошибка копирования",
        "logo.bin copied to {path}": "logo.bin скопирован в {path}",
        "Script not found": "Скрипт не найден",
        "{script} does not exist in:\n{path}\n\nUse “Folder…” to choose the correct folder.":
            "{script} не существует в:\n{path}\n\nИспользуйте "Папка…", чтобы выбрать правильную папку.",
        "Start error": "Ошибка при запуске",
        "Running {script} (PID {pid})…": "Запуск {script} (PID {pid})…",
        "Stopping the script…": "Закрытие скрипта…",
        "— Script finished (exit code {code}) —": "— Готовый скрипт (код завершения {code}) —",
        "Finished (code {code}).": "Завершено (код {code}).",
        "Waiting for your answer…": "Ожидание вашего ответа…",
        "Running…": "Пуск…",
        "The script asks for the number of an option:": "Скрипт запрашивает номер опции:",
        "The script is waiting for input:": "Скрипт ожидает ввода данных:",
        "Cancel?": "Отменить?",
        "Cancelling stops the script.\nDo you really want to stop the execution?":
            "Отмена завершает работу скрипта.\nТы действительно хочешь остановиться?",
        "The script asks for a choice": "Сценарий запрашивает выбор",
        "Select an option:": "Выберите один из вариантов:",
        "The script asks for a value": "Скрипт запрашивает значение",
        "Input:": "Ввод:",
        "Script confirmation": "Подтверждение сценария",
        "The script is waiting": "Сценарий ожидает",
        "Continue": "Продолжать",
        "Failed to send: the script is no longer reading input.": "Не удалось отправить: скрипт больше не считывает вводимые данные.",
        "Script running": "Запущенный скрипт",
        "The script is still running. Stop it and quit?": "Сценарий все еще запущен. Закрыть все и выйти?",
        "Warning: this program was made for Linux.": "Внимание: эта программа была создана для Linux.",
    },
}

LANG = "en"        # base code in use (en, pt, de, es, fr, ...)
LOCALE = "en_US"   # complete locale (used to load Qt translations)
_extra: dict[str, str] = {}


def _norm(value: str):
    """'pt_BR.UTF-8@x' -> ('pt', 'pt_BR'); 'C'/'POSIX' -> ('en','en_US')."""
    value = value.strip()
    if not value:
        return None
    if value in ("C", "POSIX"):
        return "en", "en_US"
    code = value.split(".")[0].split("@")[0].replace("-", "_")
    base = code.split("_")[0].lower()
    if not base.isalpha():
        return None
    return base, (code if "_" in code else base)


def available_languages(extra_dirs=()) -> set[str]:
    langs = set(CATALOG) | {"en"}
    for d in extra_dirs:
        langs |= {p.stem for p in Path(d).glob("*.json")} if Path(d).is_dir() else set()
    return langs


def detect_language(extra_dirs=(), qt_fallback: str | None = None):
    """Returns (base, locale) of the 1st candidate with translation; otherwise ('en', 'en_US')."""
    avail = available_languages(extra_dirs)
    seen_any = False
    for var in ("MTKLOGO_GUI_LANG", "LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"):
        for part in os.environ.get(var, "").split(":"):
            parsed = _norm(part)
            if not parsed:
                continue
            seen_any = True
            if parsed[0] in avail:
                return parsed
            if parsed[0] == "en":
                return parsed
    if not seen_any and qt_fallback:
        parsed = _norm(qt_fallback)
        if parsed and parsed[0] in avail:
            return parsed
    return "en", "en_US"


def set_language(base: str, locale: str | None = None, extra_dirs=()):
    """Activates the language; loads extra catalogs (JSON) that overwrite the embedded ones."""
    global LANG, LOCALE, _extra
    LANG, LOCALE = base, locale or base
    _extra = {}
    for d in extra_dirs:
        f = Path(d) / f"{base}.json"
        if f.is_file():
            try:
                _extra.update(json.loads(f.read_text(encoding="utf-8")))
            except (OSError, ValueError):
                pass


def _(text: str, **kw) -> str:
    out = _extra.get(text) or CATALOG.get(LANG, {}).get(text) or text
    return out.format(**kw) if kw else out
 script espera",
        "Continue": "Continuar",
        "Failed to send: the script is no longer reading input.": "Error al enviar: el script ya no lee la entrada.",
        "Script running": "Script en ejecución",
        "The script is still running. Stop it and quit?": "El script sigue en ejecución. ¿Detenerlo y salir?",
        "Warning: this program was made for Linux.": "Aviso: este programa fue hecho para Linux.",
    },
    "fr": {
        "Original (lopestom fork)": "Original (fork de lopestom)",
        "Suggested (script v2 + patched mtklogo + new yaml)": "Suggéré (script v2 + mtklogo corrigé + nouveau yaml)",
        "Folder…": "Dossier…",
        "Open": "Ouvrir",
        "Choose logo.bin…": "Choisir logo.bin…",
        "▶  Run mtklogos.sh": "▶  Lancer mtklogos.sh",
        "■  Stop": "■  Arrêter",
        "Clear": "Effacer",
        "Manual input for the script (Enter sends)": "Saisie manuelle pour le script (Entrée envoie)",
        "Send": "Envoyer",
        "Set:": "Variante :",
        "Working folder:": "Dossier de travail :",
        "Ready.": "Prêt.",
        "Folder with mtklogos.sh, mtklogo and logo.bin": "Dossier contenant mtklogos.sh, mtklogo et logo.bin",
        "Custom": "Personnalisé",
        "Choose your logo.bin": "Choisissez votre logo.bin",
        "Logo images (*.bin);;All files (*)": "Images de logo (*.bin);;Tous les fichiers (*)",
        "Replace logo.bin?": "Remplacer logo.bin ?",
        "A logo.bin already exists in:\n{path}\n\nReplace it with the selected file?\n(the original, if already used by the script, is kept in backup/)":
            "Un logo.bin existe déjà dans :\n{path}\n\nLe remplacer par le fichier choisi ?\n(l'original, s'il a déjà servi au script, est conservé dans backup/)",
        "Copy error": "Erreur de copie",
        "logo.bin copied to {path}": "logo.bin copié vers {path}",
        "Script not found": "Script introuvable",
        "{script} does not exist in:\n{path}\n\nUse “Folder…” to choose the correct folder.":
            "{script} n'existe pas dans :\n{path}\n\nUtilisez « Dossier… » pour choisir le bon dossier.",
        "Start error": "Erreur de démarrage",
        "Running {script} (PID {pid})…": "Exécution de {script} (PID {pid})…",
        "Stopping the script…": "Arrêt du script…",
        "— Script finished (exit code {code}) —": "— Script terminé (code de sortie {code}) —",
        "Finished (code {code}).": "Terminé (code {code}).",
        "Waiting for your answer…": "En attente de votre réponse…",
        "Running…": "En cours…",
        "The script asks for the number of an option:": "Le script demande le numéro d'une option :",
        "The script is waiting for input:": "Le script attend une saisie :",
        "Cancel?": "Annuler ?",
        "Cancelling stops the script.\nDo you really want to stop the execution?":
            "Annuler arrête le script.\nVoulez-vous vraiment arrêter l'exécution ?",
        "The script asks for a choice": "Le script demande un choix",
        "Select an option:": "Sélectionnez une option :",
        "The script asks for a value": "Le script demande une valeur",
        "Input:": "Saisie :",
        "Script confirmation": "Confirmation du script",
        "The script is waiting": "Le script attend",
        "Continue": "Continuer",
        "Failed to send: the script is no longer reading input.": "Échec de l'envoi : le script ne lit plus la saisie.",
        "Script running": "Script en cours",
        "The script is still running. Stop it and quit?": "Le script est toujours en cours. L'arrêter et quitter ?",
        "Warning: this program was made for Linux.": "Attention : ce programme est conçu pour Linux.",
    },
}

LANG = "en"        # base code in use (en, pt, de, es, fr, ...)
LOCALE = "en_US"   # complete locale (used to load Qt translations)
_extra: dict[str, str] = {}


def _norm(value: str):
    """'pt_BR.UTF-8@x' -> ('pt', 'pt_BR'); 'C'/'POSIX' -> ('en','en_US')."""
    value = value.strip()
    if not value:
        return None
    if value in ("C", "POSIX"):
        return "en", "en_US"
    code = value.split(".")[0].split("@")[0].replace("-", "_")
    base = code.split("_")[0].lower()
    if not base.isalpha():
        return None
    return base, (code if "_" in code else base)


def available_languages(extra_dirs=()) -> set[str]:
    langs = set(CATALOG) | {"en"}
    for d in extra_dirs:
        langs |= {p.stem for p in Path(d).glob("*.json")} if Path(d).is_dir() else set()
    return langs


def detect_language(extra_dirs=(), qt_fallback: str | None = None):
    """Returns (base, locale) of the 1st candidate with translation; otherwise ('en', 'en_US')."""
    avail = available_languages(extra_dirs)
    seen_any = False
    for var in ("MTKLOGO_GUI_LANG", "LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"):
        for part in os.environ.get(var, "").split(":"):
            parsed = _norm(part)
            if not parsed:
                continue
            seen_any = True
            if parsed[0] in avail:
                return parsed
            if parsed[0] == "en":
                return parsed
    if not seen_any and qt_fallback:
        parsed = _norm(qt_fallback)
        if parsed and parsed[0] in avail:
            return parsed
    return "en", "en_US"


def set_language(base: str, locale: str | None = None, extra_dirs=()):
    """Activates the language; loads extra catalogs (JSON) that overwrite the embedded ones."""
    global LANG, LOCALE, _extra
    LANG, LOCALE = base, locale or base
    _extra = {}
    for d in extra_dirs:
        f = Path(d) / f"{base}.json"
        if f.is_file():
            try:
                _extra.update(json.loads(f.read_text(encoding="utf-8")))
            except (OSError, ValueError):
                pass


def _(text: str, **kw) -> str:
    out = _extra.get(text) or CATALOG.get(LANG, {}).get(text) or text
    return out.format(**kw) if kw else out
