import pymel.core as pm
import random

class UI(object):
    def __init__(self):
        self.selectionSet = []
        self.myWinName = 'Object_Instancer'
        self.window_development = True
        self.rx_cb = False
        self.ry_cb = False
        self.rz_cb = False
        self.tx_cb = False
        self.ty_cb = False
        self.tz_cb = False
        self.targetNum = 0
        self.rotationRan = 0
        self.translationRan = 0
        self.uv_coord = [0,0]
        self.locList = []
        
       
#--------------------UI Generation--------------------#   
    def uIGenerator(self):
                
        if  pm.window(self.myWinName, query=True, exists=True):
            pm.deleteUI(self.myWinName)
        
        try:
            if pm.windowPref(self.myWinName, query=True, exists=True) and self.window_development:
                pm.windowPref(self.myWinName, remove=True)
        except RuntimeError:
            pass
        
        myWindow = pm.window(self.myWinName, title = 'Object Instancer', widthHeight=[600,300])
        
        base = pm.verticalLayout()
        
        with base:
            with pm.verticalLayout() as header:
                
                title = pm.text(label = 'Object Instancer'.upper())  
                pm.separator()
                
            with pm.verticalLayout() as target:
                
                self.targetInstances = pm.intSliderGrp(label="Target Instances", field = True, minValue = 0,  maxValue = 1000, changeCommand = self.storeTargetInstances)
                
                pm.separator()
            
            with pm.verticalLayout() as randomization:
                
                title3 = pm.text(label = 'Randomization')
                self.rotation = pm.checkBoxGrp(numberOfCheckBoxes = 3, label = "Rotation    ", labelArray3 =  ("RotateX","RotateY","RotateZ"),changeCommand = self.storeRotations)
                self.translation = pm.checkBoxGrp(numberOfCheckBoxes = 3, label = "Translation    ", labelArray3 =  ("TransX","TransY","TransZ"), changeCommand = self.storeTranslation)
                pm.separator()
    
                              
            with pm.verticalLayout() as Randomness:
                
                self.rRPecentage = pm.floatSliderGrp(label="Rotation Randomness", field = True, minValue = 0,  maxValue = 100)
                self.tRPecentage = pm.floatSliderGrp(label="Translation Randomness", field = True, minValue = 0,  maxValue = 100)
             
            with pm.horizontalLayout() as Button:
                
                pm.button(label='Generate', backgroundColor=[0,1,0.5], align='left', command=self.generate)
            
        base.redistribute(.4)
        
        header.redistribute(1,.1)
            
        myWindow.show()
        
#private method    
#--------------------Setter--------------------#
    def storeTargetInstances(self, *args):
        self.targetNum = self.targetInstances.getValue()
    
    def storeRotationRan(self, *args):
        self.rotationRan = self.rRPecentage.getValue()
    
    def storeTranslationRan(self, *args):
        self.translationRan = self.tRPecentage.getValue()
    
    def storeRotations(self, *args):
        self.rx_cb = self.rotation.getValue1()
        self.ry_cb = self.rotation.getValue2()
        self.rz_cb = self.rotation.getValue3()
        
    def storeTranslation(self, *args):
        self.tx_cb = self.translation.getValue1()
        self.ty_cb = self.translation.getValue2()
        self.tz_cb = self.translation.getValue3()
#--------------------Getter--------------------#        
    def getTargetInstances(self):
        return self.targetNum
        
    def getRotationRan(self):
        return self.rotationRan
        
    def getTranslationRan(self):
        return self.translationRan     
           
    def getRotations(self, str):
        if str.upper() == 'X':
            return self.rx_cb
        elif str.upper() =='Y':
            return self.ry_cb
        elif str.upper() == 'Z':
            return self.rz_cb

    def getTranslation(self, str):
        if str.upper() == 'X':
            return self.tx_cb
        elif str.upper() =='Y':
            return self.ty_cb
        elif str.upper() == 'Z':
            return self.tz_cb
            
#Generator
    def randomLocGenerator(self, sel_surf):
        return
    
    
    def locGenerator(self, sel_surf):
        
        rangeNum = self.getTargetInstances()
        
        for num in range(rangeNum):
            self.uv_coord[0] = (num + 0.5) / float(rangeNum)
            
            for vNum in range(rangeNum):
                self.uv_coord[1] = (vNum + 0.5) / float(rangeNum)
                self.locList.append(self.createSurfAttachPoint(sel_surf, self.uv_coord))
       
    def meshGenerator(self, meshList):
        
        rangeNum = self.getTargetInstances()
        
        for num in range (rangeNum * rangeNum):
            objInst = pm.instance(random.choice(meshList))[0]
            objInst.setParent(self.locList[num])
            pm.xform(objInst, translation = [0,0,0], rotation = [0,0,0])
        
           
       
    def generate(self, *args):
        
        sel_surf = pm.ls(sl = True, dag = True, type = 'nurbsSurface')[0]
        obj_list = pm.ls(sl = True, dag = True, type = 'mesh')
        
        self.locGenerator(sel_surf)
        self.meshGenerator(obj_list)
        
        return
        
#private method

# 2 pieces of information are required
# - 1. Nurbsurface
# - 2. UV coordinate (u, v) 0.0 - 1.0  
  
    def createSurfAttachPoint(self, surf, uv_coord):
        '''
        @surf     : Using specified surface 
        @uv_coord : Construct a cMuscleSurfAttach node at specified UV
        '''
        print 'Creating a point on specified surface.'
        
        surf_attach = pm.createNode('cMuscleSurfAttach')
        surf_attach_transform = surf_attach.getParent()
        
        
        surf.worldSpace >> surf_attach.surfIn
        surf_attach.outTranslate >> surf_attach_transform.translate
        surf_attach.outRotate >> surf_attach_transform.rotate
        
        
        surf_attach.uLoc.set(uv_coord[0]*surf.spansU.get())
        surf_attach.vLoc.set(uv_coord[1]*surf.spansV.get())
        
        return surf_attach_transform
    
'''def createSurfAttachPoint(self, surf = None, uv_coord = [0.0, 0.0]):
    
        @surf     : Using specified surface 
        @uv_coord : Construct a cMuscleSurfAttach node at specified UV
        
        print 'Creating a point on specified surface.'
        
        surf_attach = pm.createNode('cMuscleSurfAttach')
        surf_attach_transform = surf_attach.getParent()
        
        
        surf.worldSpace >> surf_attach.surfIn
        surf_attach.outTranslate >> surf_attach_transform.translate
        surf_attach.outRotate >> surf_attach_transform.rotate
        
        
        surf_attach.uLoc.set(uv_coord[0]*surf.spansU.get())
        surf_attach.vLoc.set(uv_coord[1]*surf.spansV.get())'''    
#selection_list = pm.ls(sl = True, dag = True, type = 'nurbsSurface')
#createSurfAttachPoint(selection_list[0], [0.5, 0.5])
#sphere1 = pm.ls(sl=True)
element = UI()  
element.uIGenerator()

        
