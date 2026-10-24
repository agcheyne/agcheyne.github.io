"""Generate static/detector-data.json for the HRPPD page.

    python3 make_data.py

The readout map is mapping.c from the hpDIRC_sigma_hits rcdaq analysis (Glasgow NHP):
COLUMN_MAP[row][col] = (slot, channel) for ONE readout column of 8 x 32 pixels, "as you look
at the back readout". The full tile is 4 such columns side by side (32 x 32 = 1024 pixels,
4 x 8 digitiser slots of 32 channels), each with the same table.

The page shows the detector FACE (laser side), like the Photek and Photonis pages, so the
back-view columns are mirrored: x_face = 31 - (8 * block + col). Row 0 is at the top.
Block 0..3 is the order of the readout columns as seen from the back (assumed).
"""
import json
import os

# (slot, channel) for each [row][col] of one readout column, back view - from mapping.c
COLUMN_MAP = [
    [(6, 24), (6, 17), (6, 18), (6, 19), (7,  3), (7, 23), (7,  9), (7,  2)],
    [(6, 10), (6, 26), (6, 31), (6, 11), (7, 11), (7, 15), (7,  6), (7, 10)],
    [(6, 23), (6, 30), (6, 20), (6, 21), (7, 13), (7, 12), (7, 14), (7,  0)],
    [(6,  8), (6, 12), (6, 25), (7,  5), (6, 27), (7, 20), (7,  1), (7,  8)],
    [(6, 22), (6,  9), (6, 28), (6, 29), (7, 21), (7,  7), (7, 17), (7, 22)],
    [(6,  0), (6, 16), (6,  2), (6,  3), (7, 29), (7, 28), (7, 16), (7, 30)],
    [(6, 14), (6,  6), (6,  7), (7, 19), (6, 13), (7, 25), (7, 24), (7,  4)],
    [(6,  4), (6,  1), (6, 15), (6,  5), (7, 27), (7, 18), (7, 31), (7, 26)],
    [(4, 24), (4, 17), (4, 18), (4, 19), (5,  3), (5, 23), (5,  9), (5,  2)],
    [(4, 10), (4, 26), (4, 31), (4, 11), (5, 11), (5, 15), (5,  6), (5, 10)],
    [(4, 23), (4, 30), (4, 20), (4, 21), (5, 13), (5, 12), (5, 14), (5,  0)],
    [(4,  8), (4, 12), (4, 25), (5,  5), (4, 27), (5, 20), (5,  1), (5,  8)],
    [(4, 22), (4,  9), (4, 28), (4, 29), (5, 21), (5,  7), (5, 17), (5, 22)],
    [(4,  0), (4, 16), (4,  2), (4,  3), (5, 29), (5, 28), (5, 16), (5, 30)],
    [(4, 14), (4,  6), (4,  7), (5, 19), (4, 13), (5, 25), (5, 24), (5,  4)],
    [(4,  4), (4,  1), (4, 15), (4,  5), (5, 27), (5, 18), (5, 31), (5, 26)],
    [(2, 30), (2, 31), (2, 26), (2, 27), (3,  5), (3, 15), (3,  1), (3,  4)],
    [(2,  4), (2, 24), (2, 25), (3, 13), (2, 19), (3,  7), (3,  6), (3, 14)],
    [(2, 18), (2, 16), (2, 28), (2, 29), (3,  3), (3,  2), (3, 16), (3,  0)],
    [(2, 22), (2, 17), (2,  7), (2, 21), (3, 29), (3, 28), (3,  9), (3,  8)],
    [(2,  8), (2,  1), (2, 20), (3, 27), (2,  5), (3, 25), (3, 12), (3, 22)],
    [(2,  0), (2, 14), (2, 12), (2, 13), (3, 21), (3, 20), (3, 30), (3, 24)],
    [(2, 10), (2,  6), (2, 15), (2, 11), (3, 11), (3, 31), (3, 26), (3, 10)],
    [(2,  2), (2,  9), (2, 23), (2,  3), (3, 19), (3, 23), (3, 17), (3, 18)],
    [(0, 30), (0, 31), (0, 26), (0, 27), (1,  5), (1, 15), (1,  1), (1,  4)],
    [(0,  4), (0, 24), (0, 25), (1, 13), (0, 19), (1,  7), (1,  6), (1, 14)],
    [(0, 18), (0, 16), (0, 28), (0, 29), (1,  3), (1,  2), (1, 16), (1,  0)],
    [(0, 22), (0, 17), (0,  7), (0, 21), (1, 29), (1, 28), (1,  9), (1,  8)],
    [(0,  8), (0,  1), (0, 20), (1, 27), (0,  5), (1, 25), (1, 12), (1, 22)],
    [(0,  0), (0, 14), (0, 12), (0, 13), (1, 21), (1, 20), (1, 30), (1, 24)],
    [(0, 10), (0,  6), (0, 15), (0, 11), (1, 11), (1, 31), (1, 26), (1, 10)],
    [(0,  2), (0,  9), (0, 23), (0,  3), (1, 19), (1, 23), (1, 17), (1, 18)],
]

# Not measured yet: placeholders, shown as such on the page (the offset boxes stay editable)
SPECS = {
    "pixel_pitch_mm": 3.25,
    "offset_x_mm": 0.0,      # laser position of the centre of pixel (0,0)
    "offset_y_mm": 0.0,
    "placeholder": True,
}


def hrppd_channels():
    channels = {}
    for block in range(4):
        for row, cols in enumerate(COLUMN_MAP):
            for col, (slot, ch) in enumerate(cols):
                x = 31 - (8 * block + col)
                readout = 8 * block + slot
                channels[f"C{block}S{slot}_Ch{ch}"] = {
                    "x": x, "y": row, "readout": readout, "block": block, "slot": slot, "channel": ch}
    return channels


if __name__ == "__main__":
    ch = hrppd_channels()
    assert len(COLUMN_MAP) == 32 and all(len(r) == 8 for r in COLUMN_MAP)
    assert len(ch) == 1024
    assert len({(c["x"], c["y"]) for c in ch.values()}) == 1024
    assert len({(c["readout"], c["channel"]) for c in ch.values()}) == 1024
    os.makedirs("static", exist_ok=True)
    with open("static/detector-data.json", "w") as f:
        json.dump({"channels": ch, "specs": SPECS}, f, indent=2)
    print("wrote static/detector-data.json:", len(ch), "pixels")
