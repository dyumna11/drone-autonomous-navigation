from dronekit import connect, VehicleMode, Vehicle, LocationGlobalRelative
from time import sleep

class Drone:
    def __init__(self, connection_string = "/dev/ttyACM0") -> None:
        self.connection_string = connection_string
        print(f"\nAttempting to connect on {connection_string}...")
        self.vehicle = connect(self.connection_string, wait_ready=True)
        print("Connection successful!")
    def get_gps_coords(self) -> tuple:
         return (self.vehicle.location.global_relative_frame.lat,self.vehicle.location.global_relative_frame.lon,self.vehicle.location.global_relative_frame.alt)
    
    def channel_5_listener(self,value):
        if value>1500:
            print(f"Channel 5 activated (value-{value}). Fetching GPS telemetry...")
            gps_value=self.get_gps_coords()
            with open("gps_locations.txt", "a") as file:
                file.write(f"{gps_value}\n")

        
    def monitor(self):
        print("Monitoring RC Channel 5...")
        while True:
            value=self.vehicle.channels['5']
            self.channel_5_listener(value)
            sleep(1)
if __name__ == "__main__":
    drone = Drone()
    drone.monitor()
    
    

   
