import subprocess
f = open("c:\\temp\\temp.py", "w")
f.write(open("main.py").read())
f.close()
subprocess.call("\"C:\\Users\\Vlad\\AppData\\Local\\Programs\\Python\\Python38-32\\Scripts\\pyinstaller.exe\" --distpath \"c:\\temp\" c:\\temp\\temp.py")
subprocess.call("C:\\temp\\temp\\temp.exe")
