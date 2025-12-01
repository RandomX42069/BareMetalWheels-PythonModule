$varscall = "InsertHere"  

if ($varscall) {
    & $varscall
}

nuitka --msvc=latest --standalone --onefile bareMetal.py
