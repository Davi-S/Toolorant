Set objShell = CreateObject("WScript.Shell")
objShell.Run ".venv\Scripts\activate && python src\desktop.py", 0, True
Set objShell = Nothing