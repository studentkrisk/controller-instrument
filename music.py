import hid
gamepad = hid.device()
gamepad.open(0x054c, 0x0268)
gamepad.set_nonblocking(True)