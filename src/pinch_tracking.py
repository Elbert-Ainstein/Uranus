import time
import leap
from leap import datatypes as dt

def sub_vectors(v1: dt.Vector, v2: dt.Vector) -> list:
    return map(float.__sub__, v1, v2)

## Returns the location of the distal phalanges of a finger
def loc_end_of_finger(hand: dt.Hand, digit_index: int) -> dt.Vector:
    dig = hand.digits[digit_index]
    return dig.distal.next_joint

def fingers_pinching(thumb: dt.Vector, index: dt.Vector):
    diff = list(map(abs, sub_vectors(thumb, index)))
    if diff[0] < 20 and diff[1] < 20 and diff[2] < 20:
        return True, diff
    else:
        return False, diff
    
class PinchingListener(leap.Listener):
    def on_tracking_event(self, event):
        if event.tracking_frame_id % 50 == 0:
            for hand in event.hands:
                hand_type = "Left" if str(hand.type) == "HandType.Left" else "Right"

                thumb = loc_end_of_finger(hand, 0)
                index = loc_end_of_finger(hand, 1)

                pinching, array = fingers_pinching(thumb, index)
                pinching_str = "not pinching" if not pinching else "" + str("pinching")
                
                print(
                    f"{hand_type} hand thumb and index {pinching_str} with position diff ({array[0]}, {array[1]}, {array[2]})."
                )

def main():
    listener = PinchingListener()

    connection = leap.Connection()
    connection.add_listener(listener)

    with connection.open():
        while True:
            time.sleep(1)

if __name__ == "__main__":
    main()