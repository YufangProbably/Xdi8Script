(
    xdi8_alphabet := (
        "XbpmwjqxynzDsrH"
        "Nldtgkh45vF7Bcfu"
        "aoeEAYL62T83V1i"
    ),
    xdi8_symbols := {
        0x5E:   "^",
        0x21E7: "~",
        0x7E:   "~",
    },
    ti2ify := lambda string, func = lambda x: "".join(x): func((
        (
            char := char - 0xE020,
            Xsymbol := char % 0x30 >> 4,
            Xorder := (char // 0x30 << 4) + (char & 0xF),
            ("^", "", "~")[Xsymbol] + xdi8_alphabet[Xorder]
        )[-1] if 0xE020 <= (char := ord(i)) < 0xE0B0 else (
            char := char - 0xF1B00,
            Xsymbol := char // 0x60,
            Xorder := char % 0x60,
            ("^", "", "~")[Xsymbol] + xdi8_alphabet[Xorder]     
        )[-1] if 0xF1B00 <= char < 0xF1C20 else (
            i,
        )[-1] if (
            0x40 < char < 0x5B
            or 0x60 < char < 0x7B
            or 0x30 <= char < 0x3A
            or i == "_"
        ) else (
            xdi8_symbols[char],
        )[-1] if char in xdi8_symbols else (
            "/" + hex(char)[2:],
        )[-1]
    ) for i in string),
)
