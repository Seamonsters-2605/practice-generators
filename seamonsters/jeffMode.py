__author__ = 'jacobvanthoog'
import wpilib

# based off code in HolonomicDrive
class JeffMode:

    def __init__(self, talon):
        self.Talon = talon

        if not (self.Talon.getControlMode() == wpilib.CANTalon.ControlMode.Position):
            self.Talon.changeControlMode(wpilib.CANTalon.ControlMode.Position)
        self.encoderTarget = self.Talon.getPosition() #zero encoder targets
        self.invert = 1 # can be 1 or -1


    def set(self, magnitude): #Increments position to mock speed mode
        if not abs(self.Talon.getPosition() - self.encoderTarget) > 2*magnitude:
            self.encoderTarget += magnitude * self.invert
        self.Talon.set(self.encoderTarget)
    
    def invert(self, enabled=True):
        self.invert = -1 if enabled else 1