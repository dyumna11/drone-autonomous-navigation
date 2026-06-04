LOG_FILE = '/home/bravo6/startup.txt'


with open(LOG_FILE, 'a') as f:
    f.write("ELLO from ze script...")


try:
    from datetime import datetime
    import json
    from time import sleep
    from DroneTerminal import Drone
    import os
    # from dronekit import connect

    with open(LOG_FILE, 'a') as f:
        f.write("Imports done...")

    try:
        drone = Drone()
        vehicle = drone.get_vehicle()
    except Exception as e:
        with open(LOG_FILE, 'a') as f:
            f.write("Error connecting to Drone...\n", e)


    with open(LOG_FILE, 'a') as f:
        f.write("Imports done...")

    ROUND = 0

    MASTER_CHANNEL = 7
    LOG_CHANNEL = 8
    AUTO_COMMENCE_CHANNEL = 6
    

    # vehicle = connect('/dev/ttyACM0', wait_ready=True)
    # vehicle = connect('127.0.0.1:14550')


    print("Make Sure PPM mode is selected...\nConnected!")

    @vehicle.on_message('RC_CHANNELS')
    def RC_CHANNEL_listener(vehicle, name, message):
        set_rc(1, message.chan1_raw)
        set_rc(2, message.chan2_raw)
        set_rc(3, message.chan3_raw)
        set_rc(4, message.chan4_raw)
        set_rc(5, message.chan5_raw)
        set_rc(6, message.chan6_raw)
        set_rc(7, message.chan7_raw)
        set_rc(8, message.chan8_raw)
        vehicle.notify_attribute_listeners('channels', vehicle.channels)


    def set_rc(channel_num, value):
        vehicle._channels._update_channel(str(channel_num), value)

    try:
        while True:
            try:
                # print(f"\r{vehicle.channels[5]:04d}   {vehicle.channels[6]:04d}   {vehicle.channels[7]:04d}   {vehicle.channels[8]:04d} ", end="", flush=True)
                
                
                master_val = vehicle.channels[MASTER_CHANNEL]
                if master_val < 1100:
                    ROUND = 0
                elif master_val < 1700:
                    ROUND = 1
                    # print("Activating Logger...")
                else:
                    ROUND = 2

                print(f"\r{ROUND}", end="", flush=True)

                '''If ROUND == 1 then Activate Logger, if ROUND == 2 then run the round 2 script'''


                if ROUND == 1:
                    vehicle.play_tune(b'B')
                    log_flag = vehicle.channels[LOG_CHANNEL]
                    try:
                        if log_flag < 1500:
                            clicked = False
                        else: # Click
                            if not clicked:
                                clicked = True
                                d = {}
                                try:
                                    with open('coord_log.json', 'r') as f:
                                        d = json.load(f)
                                except Exception as e:
                                    print(e)
                                d[str(datetime.now())] = drone.get_gps_coords()
                                # print(d)
                                with open('coord_log.json', 'w') as f:
                                    json.dump(d, f)
                    except TypeError:
                        pass

                elif ROUND == 2:
                    # break
                    auto_val = vehicle.channels[AUTO_COMMENCE_CHANNEL]
                    if auto_val > 1500:
                        break
                else: # ROUND 0
                    vehicle.play_tune(b'A')

                    # Rename the file 'coord_log.json' to 'OLDcoord_log.json' if it exists
                    v = vehicle.channels[AUTO_COMMENCE_CHANNEL]
                    if v > 1500:
                        if os.path.exists('coord_log.json'):
                            os.rename('coord_log.json', f'OLDcoord_log-{datetime.now()}.json')
                            vehicle.play_tune(b'D')

            except TypeError:
                pass
    except KeyboardInterrupt:
        pass


    print("\n\n\nStarting ROUND 2 Sequence...")

    vehicle.play_tune(b'AA')
    vehicle.play_tune(b'BBB')
    vehicle.play_tune(b'A')
    vehicle.play_tune(b'C')


    TOLERANCE = 12

    coord_sequence = [] # Lat and Lons
    try:
        print("Fetching coords from 'coord_log.json'...")
        with open('coord_log.json', 'r') as f:
            d = json.load(f)
            for timestamp in d:
                coord = d[timestamp]
                coord_sequence.append(tuple(coord))

        print(f'{len(coord_sequence)} coords found!')
        print(coord_sequence)
    except FileNotFoundError as e:
        print(e)
        while True:
            vehicle.play_tune(b'G')
            sleep(1)
            vehicle.play_tune(b'H')
            sleep(1)



    quit()


    drone.arm_and_takeoff(5)
    sleep(1)


    print(f"Starting journey... {len(coord_sequence)} spots to cover.")
    i = 0
    try:
        for coord in coord_sequence:
            i+=1
        
            drone.goto_gps(coord)

            try:
                while True:
                    x, y = drone.get_gps_coords()
                    errorx = abs(round((coord[0] - x) * 10 ** 6, 3))
                    errory = abs(round((coord[1] - y) * 10 ** 6, 3))

                    # print(f"\r{coord}  | {(x, y)}  | {(errorx, errory)}", end="", flush=True)

                    if errorx + errory < 12:
                        print("Lock acquired! Sleeping for 5...")
                        sleep(5)
                        raise KeyboardInterrupt
            except KeyboardInterrupt:
                print(f"\nMoved to point {i}...")


    except KeyboardInterrupt:
        pass


    print("Sending RTL!")
    drone.rtl()

    drone.close_vehicle()

except Exception as e:
    with open(LOG_FILE, 'a') as f:
        f.write(f"\nMEGA ERROR: {e}")