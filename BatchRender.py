import os
import subprocess
from subprocess import PIPE, Popen


def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )

    return process.communicate()[0]

directory = 'D:'
sourceDir = 'H:\BugattiType35'
desDir = 'D:\BugattiType35'

#Specify Shot & Range
#shotNum = input('Shot Number: ')
shotNum = 3
outPutDir = 'H:\Shot' + str(shotNum)
sF = input('sF: ')
eF = input('eF: ')

#Commands

l1 = directory
l2 = 'rd /s /q ' + desDir
l3 = 'robocopy ' + sourceDir + ' ' + desDir + ' /e'
l4 = 'cd C:\Program Files\Autodesk\Maya2016\\bin\n'
l5 = '"C:\Program Files\Autodesk\Maya2016\\bin\Render.exe" -r rman -s ' + str(sF) + ' -e ' + str(eF) + ' -proj ' + desDir + ' -rd '+ outPutDir + ' ' + desDir + '\scenes\Shot' + str(shotNum) + '.mb'

#Fetching Project files

cmdline(l1)
if os.path.exists(desDir):
    cmdline(l2)
    print ('Existed Project Deleted. Now Fetching...')
else:
    print ('Project does not exist. Now Fetching...')
cmdline(l3)
print ('Fetching Completed')
print ('Starting Render')
cmdline(l4)
cmdline(l5)




