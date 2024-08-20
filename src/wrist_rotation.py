import time
import leap
from leap.events import TrackingEvent
from leap.event_listener import LatestEventListener
from leap.datatypes import FrameData
from components.wait_until import wait_until
from leap import datatypes as dt
import math

def vector_to_deg(quat: dt.Quaternion):
    theta: float = math.acos(quat.w)*2
    angle_x = quat.x / math.sin(math.acos(theta))
    angle_y = quat.y / math.sin(math.acos(theta)) 
    angle_z = quat.z / math.sin(math.acos(theta))
    print(f"angle x: {angle_x}, angle y: {angle_y}, angle z: {angle_z}")

def wrist_rotation():
    ## Add Tracking event
    listening = LatestEventListener(leap.EventType.Tracking)

    connection = leap.Connection()
    connection.add_listener(listening)

    with connection.open() as open_connection:
        ## uses the wait_until() to make sure sensor is working
        wait_until(lambda: listening.event is not None)

        ## ctrl c to exit
        while True:
            event = listening.event
            if event is None:
                continue
            
            target_frame_size = leap.ffi.new("uint64_t*")
            frame_time = leap.ffi.new("int64_t*")
            frame_time[0] = event.timestamp

            ## a delay of 0.3 seconds
            time.sleep(0.3)

            try:
                # we need to query the storage required for our interpolation
                # request, the size will depend on the number visible hands in
                # this frame
                leap.get_frame_size(open_connection, frame_time, target_frame_size)
            except Exception as e:
                print("get_frame_size() failed with: ", e)
                continue

            frame_data = FrameData(target_frame_size[0])
            try:
                # actually interpolate and get frame data from the Leap API
                # this is the time of the frame plus the 20ms artificial
                # delay and an estimated 10ms processing time which should
                # get close to real time hand tracking with interpolation
                leap.interpolate_frame(
                    open_connection,
                    event.timestamp + 30000,
                    frame_data.frame_ptr(),
                    target_frame_size[0],
                )
            except Exception as e:
                print("interpolate_frame() failed with: ", e)
                continue
            
            print(
                "Frame ",
                event.tracking_frame_id,
                " with ",
                len(event.hands),
                "hands with a delay of ",
                leap.get_now() - event.timestamp,
            )

            for hand in event.hands:
                hand_type = "left" if str(hand.type) == "HandType.Left" else "right"
                # print(
                #     f"{hand.arm.rotation.x}, {hand.arm.rotation.y}, {hand.arm.rotation.z}, {hand.arm.rotation.w}"
                # )
                vector_to_deg(hand.arm.rotation)
             
def main():
    wrist_rotation()

if __name__ == "__main__":
    main()



 