import os, sys, re

#keywords
#remove targets
items = ['master_variance_diffuse',
         'master_variance_indirectdiffuse',
         'master_variance_specular',
         'master_variance_indirectspecular',
         'master_variance_variance',
         ]

wd = 'D:/WorkBench/Maya/Cornel/renderman/AovTest_0829154224/images'
os.chdir(wd)
frameNum = 2
frame = 1
tmpList = []
tmpCmd = 'exrmerge '
outPut = 'frame.%04d.exr'
#comparator
def comparator(item1, item2):
    value1 = re.findall(r'\d+', item1)
    value2 = re.findall(r'\d+', item2)
    if value1[-1] < value2[-1]:
        return -1
    elif value1[-1] < value2[-1]:
        return 1
    else:
        return 0
    
#List generation
dirFiles = os.listdir(wd)
newList = dirFiles[:]

for exr in dirFiles:
    for item in items:
        if item in exr:
            newList.remove(exr)       
#sorting
newList.sort(comparator)
            
while frame < 3:
    for exr in newList:
        if ('%04d' % frame) in exr:
            tmpList.append(exr)      
        else:
            
            for item in tmpList:
                tmpCmd = tmpCmd + ' ' +  item
            tmpCmd = tmpCmd + ' ' + outPut %frame
            print tmpCmd
            os.system(tmpCmd)
            if frame < 3:
                frame = frame + 1
            else:
                break   
            tmpCmd = 'exrmerge '
            tmpList[:] = []

