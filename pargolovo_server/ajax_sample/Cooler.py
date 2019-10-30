
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
    def __init__(self, num):
        self.num = num
        name = "CKT" + str(num)
        self.pv = Parameter(name)
        self.TagControl = 'OPC.' + name + '.Control'
        self.TagSP = 'OPC.' + name + '.SP'
        pass
    
    def YOn(self):
        print('YOn')
        pass
    def YOff(self):
        print('YOff')
        pass
    def SetSP(self, nsp):
        self.sp = nsp
        print('SetSP')
        pass
    def GetPV(self):
        print('GetPV')
        return self.pv.Value
        

#def main():
#    CKT1 = Cooler('1')
#    print(CKT1.PV.Value)

#main()
