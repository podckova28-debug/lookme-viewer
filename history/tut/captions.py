# Overlays for the Tutankhamun episode, keyed by shot number (1-based, as in shots.S).
# CAP   - key-fact caption (Bebas Neue, white caps, red underline, no dot separators)
# YEAR  - year plate, bottom right (set at the first shot of a range, holds until changed; None hides it)
# AGE   - Tutankhamun's age, second line of the year plate (holds until changed; None hides it)
# INSET - round portrait + name when a person is introduced (no CAP on those shots)
CAP = {
 1: "VALLEY OF THE KINGS, EGYPT", 6: "LORD CARNARVON", 9: "3,000 YEARS", 11: "TUTANKHAMUN",
 12: "AKHETATEN (AMARNA)", 15: "PHARAOH AKHENATEN", 18: "ONE GOD: THE ATEN", 19: "TEMPLES CLOSED",
 22: "DNA STUDIES", 26: "THE CROOK AND THE FLAIL", 27: "ANKHESENPAATEN", 28: "QUEEN NEFERTITI",
 35: "EGYPT IS ANGRY", 38: "A NEW NAME", 39: "ATEN OUT, AMUN IN", 40: "ANKHESENAMUN", 41: "AMARNA ABANDONED",
 43: "KARNAK", 44: "THE RESTORATION STELA", 51: "THE PERFECT YOUNG GOD", 53: "A DAMAGED LEFT FOOT",
 55: "MALARIA", 56: "130 WALKING STICKS", 59: "TWO DAUGHTERS", 65: "AGE 19",
 67: "X-RAY, 1968", 68: "CT SCAN, 2005", 69: "A BROKEN LEFT LEG", 70: "A CHARIOT ACCIDENT?",
 73: "NO PHARAOH, NO HEIR", 76: "THE HITTITES", 77: "KING SUPPILULIUMA", 78: "\"I HAVE NO SON\"",
 85: "PRINCE ZANNANZA", 86: "KILLED ON THE WAY", 90: "PHARAOH AY",
 93: "ONLY FOUR ROOMS", 94: "AY AS PRIEST", 96: "THOUSANDS OF OBJECTS", 99: "ROBBED TWICE",
 103: "PHARAOH HOREMHEB", 104: "TEMPLES TORN DOWN", 107: "A KING NEVER LISTED", 108: "200 YEARS LATER",
 111: "FORGOTTEN", 113: "\"THE VALLEY IS EMPTY\"", 117: "FIVE SEASONS, NOTHING", 118: "THE LAST SEASON",
 119: "4 NOVEMBER 1922", 121: "16 STEPS", 122: "A TELEGRAM", 126: "TEN YEARS OF WORK",
 127: "5,000 OBJECTS", 128: "FOUR GOLDEN SHRINES", 130: "THREE COFFINS", 131: "110 KG OF GOLD",
 132: "THE GOLDEN MASK", 135: "EGYPTOMANIA", 138: "A MOSQUITO BITE", 140: "BLOOD POISONING",
 142: "\"THE CURSE OF THE PHARAOH\"", 143: "CAIRO GOES DARK?", 146: "CARTER LIVES ON", 147: "GRAND EGYPTIAN MUSEUM",
}
YEAR = {1: "1922", 9: None, 10: "TODAY", 11: "1341-1323 BC",
        12: "1341 BC", 22: "TODAY", 23: "1336 BC", 25: "1332 BC", 38: "1331 BC", 51: "1324 BC",
        54: "TODAY", 57: "1324 BC", 62: None, 64: "1324 BC", 65: "1323 BC", 67: "1968", 68: "2005", 70: "1323 BC",
        72: "TODAY", 73: "1323 BC", 102: "1319 BC", 108: "1150 BC", 113: "1910", 114: "1915", 116: "1914",
        117: "1917", 118: "1922", 119: "4 NOV 1922", 122: "1922", 123: "26 NOV 1922", 126: "1923",
        146: "1939", 147: "TODAY", 150: None}
AGE = {12: "NEWBORN", 20: "AGE 5", 22: None, 23: "AGE 5", 24: "AGE 6", 25: "AGE 9", 38: "AGE 10", 51: "AGE 18",
       54: None, 57: "AGE 18", 62: None, 64: "AGE 18", 65: "AGE 19", 67: None, 70: "AGE 19", 72: None, 73: None}
INSET = {4: ("carter", "HOWARD CARTER"), 25: ("tut9", "TUTANKHATEN"), 32: ("ay", "AY"), 33: ("horemheb", "HOREMHEB"), 58: ("ankh20", "ANKHESENAMUN"),
         114: ("carter", "HOWARD CARTER"), 116: ("carnarvon", "LORD CARNARVON")}
# animated clips (kling, checked frame-by-frame); shot -> file in frames/
CLIP = {5: "clip005.mp4", 8: "clip008.mp4", 124: "clip005.mp4", 125: "clip008.mp4",
        18: "clip018.mp4:2.0", 41: "clip041.mp4", 70: "clip070.mp4", 86: "clip086.mp4:2.0", 112: "clip112.mp4", 136: "clip136.mp4", 143: "clip143.mp4"}
# ":2.0" = use only the first 2 s (the rest drifts: priest face in 18, chariot shape in 86)

def held(d, k):
    v, last = None, None
    for kk in sorted(d):
        if kk <= k: v = d[kk]
    return v
