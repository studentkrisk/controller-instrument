import hid, mido
gamepad = hid.device()
gamepad.open(0x054c, 0x0268)
gamepad.set_nonblocking(True)

notes = {
    "LEFT": 64,
    "DOWN": 62,
    "RIGHT": 65,
    "UP": 60,
    "Y": 71,
    "B": 67,
    "A": 69,
    "X": 72,
}

with mido.open_output('Controller MIDI Controller', virtual=True) as out:
    last_state = {
        "LEFT": 0,
        "DOWN": 0,
        "RIGHT": 0,
        "UP": 0,
        "Y": 0,
        "B": 0,
        "A": 0,
        "X": 0,
        "LB": 0,
        "RB": 0,
        "LT": 0,
        "RT": 0,
        "RS": 0,
        "LS": 0,
        "SEL": 0
    }
    trans = 0
    while True:
        report = gamepad.read(64)
        if not report:
            continue
        state = {
            "LEFT": (report[2] & 2**7) >> 7,
            "DOWN": (report[2] & 2**6) >> 6,
            "RIGHT": (report[2] & 2**5) >> 5,
            "UP": (report[2] & 2**4) >> 4,
            "Y": (report[3] & 2**7) >> 7,
            "B": (report[3] & 2**6) >> 6,
            "A": (report[3] & 2**5) >> 5,
            "X": (report[3] & 2**4) >> 4,
            "RB": (report[3] & 2**3) >> 3,
            "LB": (report[3] & 2**2) >> 2,
            "RT": (report[3] & 2**1) >> 1,
            "LT": report[3] & 2**0,
            "RS": (report[2] & 2**2) >> 2,
            "LS": (report[2] & 2**1) >> 1,
            "SEL": report[2] & 2**0
        }
        print(state)
        for btn in notes.keys():
            if state[btn] and not last_state[btn]:
                out.send(mido.Message("note_on", note=notes[btn] - 12*state["LB"] + 12*state["RB"] - state["LT"] + state["RT"] + trans))
            if not state[btn] and last_state[btn]:
                out.send(mido.Message("note_off", note=trans + notes[btn] - 12 - 1))
                out.send(mido.Message("note_off", note=trans + notes[btn] + 12 - 1))
                out.send(mido.Message("note_off", note=trans + notes[btn]      - 1))
                out.send(mido.Message("note_off", note=trans + notes[btn] - 12    ))
                out.send(mido.Message("note_off", note=trans + notes[btn]         ))
                out.send(mido.Message("note_off", note=trans + notes[btn] + 12    ))
                out.send(mido.Message("note_off", note=trans + notes[btn] - 12 + 1))
                out.send(mido.Message("note_off", note=trans + notes[btn]      + 1))
                out.send(mido.Message("note_off", note=trans + notes[btn] + 12 + 1))
        if state["LS"] and not last_state["LS"]:
            trans -= 1
        if state["RS"] and not last_state["RS"]:
            trans += 1
        if state["SEL"]:
            for i in range(60 - 12 - 1, 60 + 12 + 1 + 1):
                out.send(mido.Message("note_off", note=i))
            trans = 0

        last_state = state



# 2 =   1   2   3   4   5   6   7   8
#       ←   ↓   →   ↑
# 3 =   1   2   3   4   5   6   7   8
#       y   b   a   x   lb  rb  lt  rt