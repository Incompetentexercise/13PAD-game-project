@echo off
pyinstaller --onefile main.pyw
move dist\main.exe
del main.spec
rmdir /S /Q dist
rmdir /S /Q build
