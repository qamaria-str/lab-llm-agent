from robot import LiquidHandler

robot = LiquidHandler()
print(robot.pick_up_tip())
print(robot.aspirate("plate_1", "A1", 50))
print(robot.dispense("plate_2", "B1", 50))
print(robot.drop_tip())
print(robot.wells)

try:
    robot.aspirate("plate_1", "A1", 50)
except ValueError as e:
    print("Erreur attendue :", e)