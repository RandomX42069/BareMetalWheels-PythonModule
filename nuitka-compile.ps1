$varscall = "InsertHere"  

if ($varscall) {
    & $varscall
}

nuitka --msvc --standalone --onefile bareMetal.py
