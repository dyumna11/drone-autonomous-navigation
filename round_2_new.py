from dronekit import connect, VehicleMode, Vehicle, LocationGlobalRelative
from time import sleep
import math

class Drone:
    def __init__(self, connection_string = "/dev/ttyACM0") -> None:
        self.connection_string = connection_string
        print(f"\nAttempting to connect on {connection_string}...")
        self.vehicle = connect(self.connection_string, wait_ready=True)
        print("Connection successful!")
    
    def goto_gps(self, coords : tuple):
        self.vehicle.simple_goto(LocationGlobalRelative(
            coords[0],
            coords[1],
            coords[2],))
        while self.calculate_dist(coords)<=5:
            print("reached")
            sleep(5)
        sleep(1)

    def calculate_dist(self,target_coords):
        curr_loc=self.get_current_location()
        calc_dist=math.sqrt(((curr_loc[0]-target_coords[0])**2+(curr_loc[1]-target_coords[1])**2))
        return calc_dist

    def get_current_location(self):
        return (self.vehicle.location.global_relative_frame.lat,
            self.vehicle.location.global_relative_frame.lon,
            self.vehicle.location.global_relative_frame.alt)
    
    def read_waypoints(self, file_path): #insert file path
        with open(file_path, "r") as file:
            return [tuple(map(float, line.strip().split(','))) for line in file]

if __name__ == "__main__":
    drone=Drone()
    try:
        waypoints=drone.read_waypoints("gps_locations.txt")
        for waypoint in waypoints:
            drone.goto_gps(waypoint)
    except KeyboardInterrupt:
        print("mission interrupted")

