import hid
gamepad = hid.device()
gamepad.open(0x054c, 0x0268)
gamepad.set_nonblocking(True)
while True:
    report = gamepad.read(64)
    if report:
        print("{:08b}".format(report[2]), "{:08b}".format(report[3]))

# 2 =   1   2   3   4   5   6   7   8
#       ←   ↓   →   ↑
# 3 =   1   2   3   4   5   6   7   8
#       y   b   a   x   lb  rb  lt  rt