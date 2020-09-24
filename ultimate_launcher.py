import os

f = open("c:\\temp\\temp.py", "w")
f.write(open("main.py").read())
f.close()
'''
# Clears output folder
os.system(r'cmd /c rmdir /s /q c:\\Users\Vlad\Desktop\python\\temp\\temp')
# PyInstaller on the copy of main.py
os.system(r'cmd /k C:\\Users\Vlad\PycharmProjects\Ultimate_Parser\\venv\Scripts\pyinstaller.exe --distpath C:\Users\Vlad\Desktop\python\temp c:\temp\temp.py')
os.system(r'cmd /k start ')
# Calls the exe obtained from line above
subprocess.call(r"C:\\Users\Vlad\Desktop\python\\temp\\temp\\temp.exe")
'''