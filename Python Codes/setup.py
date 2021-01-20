import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable("Initial_Window.py", base=base, icon="Images_IG/IconExe2.ico")
]

packages = ["idna", "PyQt5", "numpy", "moduleAI", "encodings"]

options = {
    "build_exe": {
        "packages": packages,
        "include_files": [
            "Images_IG",
            "Save",
            "Text",
            "Ddl_mkl/libiomp5md.dll",
            "Ddl_mkl/mkl_intel_thread.dll",
            "Ddl_mkl/mkl_rt.dll",
        ],
        "excludes": ["Tkinter"],
    }
}

setup(
    options=options,
    name="Test1",
    version="2.0",
    description="Projet Echec pour Module TDLog",
    install_requires=["numpy == 1.19.3", "PyQt5>=5.15.2", "PyQt5-sip>=12.8.1"],
    executables=executables,
)
