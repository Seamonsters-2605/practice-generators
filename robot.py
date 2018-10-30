import wpilib
import ctre
import seamonsters as sea

class MyRobot(sea.GeneratorBot):

    def robotInit(self):
        self.frontLeft = ctre.WPI_TalonSRX(2)
        self.frontRight = ctre.WPI_TalonSRX(1)
        self.backLeft = ctre.WPI_TalonSRX(0)
        self.backRight = ctre.WPI_TalonSRX(3)
    
    def autonomous(self):
        yield

if __name__ == "__main__":
    wpilib.run(MyRobot, physics_enabled=True)
