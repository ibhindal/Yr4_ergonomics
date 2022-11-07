import slicer as sl
import numpy as np


# Setting up k-wire information

# User can input a k-wire thickness or type x which chooses the average value for them
kWireDiameterInput = input("Enter the diameter of your k-wire in mm. If none is decided, type x: ")


try:
    kWireDiameter = float(kWireDiameterInput) # Convert to float

    if kWireDiameter < 0.5:
        print("This value is too small")

    elif kWireDiameter > 3:
        print("This value is too big")

except(ValueError):
    if kWireDiameterInput == "x" or kWireDiameterInput == "X": # Code to choose value for user 
        kWireDiameter = 1.8 # Research needed on what diameter is best/most commonly used

except:
    print("This is not a valid number")


print("Your k-wire diameter is " + str(kWireDiameter))






# First k-wire



# Second k-wire




# Third k-wire
