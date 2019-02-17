D:
rd /s /q BugattiType35
del /q Render.bat
robocopy H:\BugattiType35 D:\BugattiType35 /e
copy H:\Render.bat D:\Render.bat
notepad Render.bat