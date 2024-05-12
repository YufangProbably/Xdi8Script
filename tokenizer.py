(
    re := __import__("re"),
    ti2 := __import__("ti2"),
    
    xdi8_regex := (
        rf"⇧\^~{ti2.xdi8_alphabet}"
        rf"\uE001-\uE00F\uE020-\uE0AD"
        rf"{chr(0xF1B00)}-{chr(0xF1C1F)}"
    ),
    number_regex := (
        r"(?:0|[1-9]\d*)(?:\.\d+)?(?:[Ee\uE081\uE091"
        rf"{chr(0xF1B21)}{chr(0xF1B81)}][+-]?\d+)?"
    ),
    token_regexs := dict(
        comment = r"\\.+(?:\\|$)",
        string  = r'"(?:\\"|\\n|\\|\\/|[^"])*"',
        end     = r";|$",   skip    = r"\s+",
        number  = number_regex,
        xdi8num = rf"·[,._{xdi8_regex}]+·",
        symbol  = rf"(?P<ta>[◇♢])[_{xdi8_regex}]+(?P=ta)",
        iden    = rf"[$#_{xdi8_regex}]+",
        ldbk    = r"[\u27E6\u301A]|\[\[",
        rdbk    = r"[\u27E7\u301B]|\]\]",
        lpar = r"\(", rpar = r"\)",
        lbck = r"\[", rbck = r"\]",
        lbce = r"\{", rbce = r"\}",
        comma   = r",",     period  = r"\.",
        ques    = r"\?",    colon   = r":",
        op      = r"[%^]|(?P<tb>[*/&|])(?P=tb)?",
        dop     = r"[+\-]",
        fop     = r"[~!]",
        compare = r"[><]=?|=",
        error   = r".+?",
    ),
    keywords := [
        "^roH", "^pia^roH", "^pia",
        "^H6", "^z3gie",
        "^x6", "^goz", "^HT",
        "^wTH", "wE", 
    ],
    op_keywords := [
        "sE", "HY", "de", "yu6H",
        "ja", "jYE", "c3", "tA1", "cmo", "f8",
        "jaNiT", "jYENiT", "c3NiT", "tA1NiT", "cmoNiT", "f8NiT",
        "FY2", "da", "xL", "NiVH", "Fia1", "B6",
        "FY2yA", "dayA", "xLyA", "NiVHyA", "Fia1yA", "B6yA",
        "qeH", "hio", "bA",
    ],
    
    tokenize := lambda code, throws = True: (
        regex := r"|".join(rf"(?P<{n}>{v})" for n,v in token_regexs.items()),
        get := list(filter(lambda x: x, ((
            name := re.sub(r"\d+$", "", token.lastgroup),
            value := token.group(),
            (
                (_ for _ in ()).throw(SyntaxError(
                    f"Unexpected {repr(value)}"
                )) if throws else None
            ) if name == "error" else dict(
                type = "keyword",
                value = ti2.ti2ify(value),
            ) if value in keywords else dict(
                type = "op_keyword",
                value = ti2.ti2ify(value),
            ) if value in op_keywords else dict(
                type = "iden",
                value = ti2.ti2ify(value),
            ) if name == "iden" else dict(
                type = "int",
                value = value,
            ) if name == "number" and re.match("^0|[1-9]\d*$", value) else (
                None
            ) if name in ("skip",) else dict(
                type = name,
                value = value,
            )
        )[-1] for token in re.finditer(regex, code)))),
        print("\n".join((
            f"{i['type'].title()}"
            f"({repr(i['value'])})"
        )for i in get)),
        None
    )[-1],
)
