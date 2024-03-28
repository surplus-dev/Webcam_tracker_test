from math import radians

from vmcp.osc import OSC
from vmcp.osc.typing import Message
from vmcp.osc.backend.osc4py3 import as_eventloop as backend

from time import time as get_time

'''
0 - nose
1 - left eye (inner)
2 - left eye
3 - left eye (outer)
4 - right eye (inner)
5 - right eye
6 - right eye (outer)
7 - left ear
8 - right ear
9 - mouth (left)
10 - mouth (right)

11 - left shoulder -> LEFT_SHOULDER
12 - right shoulder -> RIGHT_SHOULDER
13 - left elbow
14 - right elbow
15 - left wrist
16 - right wrist
17 - left pinky
18 - right pinky
19 - left index
20 - right index
21 - left thumb
22 - right thumb
23 - left hip
24 - right hip
25 - left knee
26 - right knee
27 - left ankle
28 - right ankle
29 - left heel
30 - right heel
31 - left foot index
32 - right foot index
'''

# VMC protocol layer
from vmcp.events import (
    Event,
    RootTransformEvent,
    BoneTransformEvent,
    BlendShapeEvent,
    BlendShapeApplyEvent,
    DeviceTransformEvent,
    StateEvent,
    RelativeTimeEvent
)
from vmcp.typing import (
    CoordinateVector,
    Quaternion,
    Bone,
    DeviceType,
    BlendShapeKey as AbstractBlendShapeKey,
    ModelState,
    Timestamp
)
from vmcp.protocol import (
    root_transform,
    bone_transform,
    device_transform,
    blendshape,
    blendshape_apply,
    state,
    time
)

LISTENING = True
try:
    osc = OSC(backend)
    with osc.open():
        # Sender
        osc.create_sender("192.168.56.1", 39539, "sender1")
        while 1:
            osc.get_sender("sender1").open().send(
                (
                    Message(*bone_transform(
                        Bone.LEFT_UPPER_LEG,
                        CoordinateVector.identity(),
                        Quaternion.from_euler(0, 0, radians(-45))
                    )),
                    Message(*bone_transform(
                        Bone.RIGHT_LOWER_ARM,
                        CoordinateVector.identity(),
                        Quaternion(0, 0, 0.3826834323650898, 0.9238795325112867)
                    )),
                    Message(*blendshape_apply()),
                    Message(*state(ModelState.LOADED)),
                    Message(*time(Timestamp(get_time())))
                )
            )

            print("test")
            osc.run()
except KeyboardInterrupt:
    print("Canceled.")
finally:
    osc.close()