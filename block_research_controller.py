from controller import Robot

# Initialize the Robot instance
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Enable Motor devices for differential steering
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

# Enable Distance Sensors
ds = []
ds_names = ['ps0', 'ps1', 'ps2', 'ps3', 'ps4', 'ps5', 'ps6', 'ps7']
for name in ds_names:
    sensor = robot.getDevice(name)
    sensor.enable(timestep)
    ds.append(sensor)

# Enable Camera device
camera = robot.getDevice('camera')
camera.enable(timestep)

print("Starting e-puck camera and navigation controller...")

image_saved = False
max_speed = 6.28

# Main Simulation Loop
while robot.step(timestep) != -1:
    # Read distance sensors for obstacle avoidance
    left_obstacle = ds[5].getValue() > 80.0 or ds[6].getValue() > 80.0
    right_obstacle = ds[1].getValue() > 80.0 or ds[2].getValue() > 80.0

    if left_obstacle:
        left_motor.setVelocity(max_speed)
        right_motor.setVelocity(-max_speed)
    elif right_obstacle:
        left_motor.setVelocity(-max_speed)
        right_motor.setVelocity(max_speed)
    else:
        left_motor.setVelocity(max_speed)
        right_motor.setVelocity(max_speed)

    # Capture a snapshot image from the camera
    if not image_saved:
        camera.saveImage("dog_cat_capture.png", quality=100)
        print("Saved camera capture as dog_cat_capture.png")
        image_saved = True
