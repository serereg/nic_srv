
class Parameter:
    Value = 0
    Fault = False
    TagName = "OPC.Item"
    def __init__(self, name):
        self.TagName = name
        #print(self.TagName)
    

class Cooler:
    """Управление охладителем"""
    num = 1 # cooler num
    name = "CKT" # cooler name
    sp = 0
    pv = Parameter('') # Parameter for control
    TagControl = ''
    TagSP = ''
    ControlString = ""
    StateOn = False
    def __init__(self, num):
        self.num = num
        name = "CKT" + str(num)
        self.pv = Parameter(name)
        self.TagControl = 'OPC.' + name + '.Control'
        self.TagSP = 'OPC.' + name + '.SP'
        pass
    
    def YOn(self):
        print('YOn')
        self.StateOn = True # imitation
        pass
    def YOff(self):
        print('YOff')
        self.StateOn = False # imitation
        pass
    def SetSP(self, nsp):
        self.sp = nsp
        print('SetSP')
        pass
    def GetPV(self):
        #print('GetPV')
        self.pv.Value = self.sp # imitation
        return self.pv.Value
    def isOn(self):
        return self.StateOn

#def main():
#    CKT1 = Cooler('1')
#    print(CKT1.PV.Value)

#main()
