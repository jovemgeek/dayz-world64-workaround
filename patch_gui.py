"""File-picker front end for the same exact-build, copy-only patcher."""
import argparse
import tempfile
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from patch_world64 import patch

TEXT = {
    "pt": {
        "intro": "Este assistente cria uma COPIA corrigida do executavel.\n\n1. Selecione o DayZServer_x64.exe ORIGINAL.\n2. Escolha onde salvar a nova pasta.\n\nEle nao instala, inicia ou para o servidor. Leia o guia antes de instalar. Ajuste experimental para um unico build.",
        "source": "Selecione o DayZServer_x64.exe original",
        "folder": "Onde salvar a pasta com a copia corrigida?",
        "success": "COPIA CRIADA E VERIFICADA\n\nArquivo para instalar:\n{output}\n\nO original nao foi alterado. A instalacao no servidor ainda NAO foi feita.\n\nSiga os passos 4 a 6 do README.pt-BR.md: backup, servidor parado, substituicao e verificacao.",
        "failure": "Nao foi possivel criar uma copia validada. Nao instale arquivos de uma tentativa com erro.\n\n{error}\n\nSe aparecer Unsupported executable, use o original do build suportado. Nao altere os hashes para forcar a aplicacao. Consulte a tabela de problemas do guia.",
    },
    "en": {
        "intro": "This wizard creates a patched COPY of the executable.\n\n1. Select your ORIGINAL DayZServer_x64.exe.\n2. Choose where to save the new folder.\n\nIt does not install, start or stop your server. Read the guide before installation. Experimental workaround for one exact build.",
        "source": "Select your original DayZServer_x64.exe",
        "folder": "Where should the new patched-copy folder be saved?",
        "success": "COPY CREATED AND VERIFIED\n\nFile to install:\n{output}\n\nThe original is unchanged. Server installation has NOT been performed.\n\nFollow steps 4 to 6 in docs/QUICK_START.md: backup, stop, replace and verify.",
        "failure": "Could not create a verified copy. Do not install files from a failed attempt.\n\n{error}\n\nFor Unsupported executable, use the original supported build. Do not change hashes to force the patch. See the troubleshooting table in the guide.",
    },
}


def create_copy(source, destination):
    # A fresh directory avoids replacing any installed executable or prior output.
    folder = Path(tempfile.mkdtemp(prefix="World64-", dir=destination))
    output = folder / "DayZServer_x64.exe"
    patch(source, output)
    return output


def main(language="en"):
    words = TEXT[language]
    root = tk.Tk()
    root.withdraw()
    try:
        if not messagebox.askokcancel("DayZ World64", words["intro"], parent=root):
            return
        source = filedialog.askopenfilename(title=words["source"], filetypes=[("DayZ server", "*.exe")], parent=root)
        if not source:
            return
        destination = filedialog.askdirectory(title=words["folder"], parent=root)
        if not destination:
            return
        try:
            output = create_copy(source, destination)
        except (OSError, ValueError) as error:
            messagebox.showerror("DayZ World64", words["failure"].format(error=error), parent=root)
            return
        messagebox.showinfo("DayZ World64", words["success"].format(output=output), parent=root)
    finally:
        root.destroy()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", choices=TEXT, default="en")
    main(parser.parse_args().language)
