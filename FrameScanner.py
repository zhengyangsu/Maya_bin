import os
import re

desDir = 'H:/RenderTest'
frames = []
totalFrame = 140
dontFrame = 0
missingFrameCounter = 0
file = open("H:/renderTask.txt", "w")

for i in range (totalFrame + 1):
    exist = False
    frames.append(exist)
    
frames[0] = True

for item in os.listdir(desDir):
    frame = int(re.findall('\d+', item)[1])
    print (frame)
    frames[frame] = True



for i in range (totalFrame + 1):
    if frames[i] == False:
        missingFrameCounter += 1 
        file.write("Missing: " + str(i) + "\n")
        print ("Missing: " + str(i))

print ("\nFinished frame: " +  str(totalFrame - missingFrameCounter )+ "\n" +
       "Total missing frame Count: " + str(missingFrameCounter))
    
file.write("\nFinished frame: " +  str(totalFrame - missingFrameCounter )+ "\n" + "Total missing frame Count: " + str(missingFrameCounter))

file.close()
