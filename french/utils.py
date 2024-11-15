from typing import TypedDict, Any


class T_DICT(TypedDict):
    Mot: str
    Définitions: list[str]


def loolike(text: Any, target: str):
    len_text = len(text)
    ecart = len(target) - len_text
    denominator = len(target)
    same: float = 0

    if len_text > len(target):
        # text = text[0 : len_text + ecart]
        target += abs(ecart) * "-"
    else:
        text += ecart * "-"

    denominator = len(target) + abs(ecart)

    for i, letter in enumerate(text):
        if letter in target:
            # same += 1
            if letter != target[i]:
                same += 0.25
            else:
                same += 1
    return same / denominator


def loolike2(text: Any, target: str):
    len_text = len(text)
    ecart = len(target) - len_text
    denominator = 1
    same: float = 0

    target += abs(ecart) * "-"
    denominator = len(target)

    for i, letter in enumerate(text):
        if letter != target[i]:
            same += 0.25
        else:
            same += 1

    return same / denominator


def frange(a: float, b: float, step: float):
    while a < b:
        yield round(a, 2)
        a += step


class style:
    @classmethod
    def __contains__(cls, target, *chars):
        return any((i in target for i in chars))

    @classmethod
    def __style(cls, value: int, text: Any) -> str:
        text = str(text)
        colorize = lambda x: f"\033[{value}m{x}\033[0m"
        iter_tokens = ("[]", "()", "{}", "]", "{", "}", "(", ")")

        return (
            colorize(text)
            if cls.__contains__(text, *iter_tokens)
            else " ".join((colorize(i) for i in text.split(" ")))
        )

    @classmethod
    def cyan2(cls, text: Any):
        return cls.__style(96, text)

    @classmethod
    def purple2(cls, text: Any):
        return cls.__style(95, text)

    @classmethod
    def blue2(cls, text: Any):
        return cls.__style(94, text)

    @classmethod
    def yellow2(cls, text: Any):
        return cls.__style(93, text)

    @classmethod
    def green2(cls, text: Any):
        return cls.__style(92, text)

    @classmethod
    def red2(cls, text: Any):
        return cls.__style(91, text)

    @classmethod
    def grey2(cls, text: Any):
        return cls.__style(90, text)

    @classmethod
    def underline2(cls, text: Any):
        return cls.__style(52, text)

    @classmethod
    def bgwhite2(cls, text: Any):
        return cls.__style(47, text)

    @classmethod
    def bgcyan(cls, text: Any):
        return cls.__style(46, text)

    @classmethod
    def bgpurple(cls, text: Any):
        return cls.__style(45, text)

    @classmethod
    def bgblue(cls, text: Any):
        return cls.__style(44, text)

    @classmethod
    def bgyellow(cls, text: Any):
        return cls.__style(43, text)

    @classmethod
    def bggreen(cls, text: Any):
        return cls.__style(42, text)

    @classmethod
    def bgred(cls, text: Any):
        return cls.__style(41, text)

    @classmethod
    def bggrey(cls, text: Any):
        return cls.__style(40, text)

    @classmethod
    def bold2(cls, text: Any):
        return cls.__style(37, text)

    @classmethod
    def cyan(cls, text: Any):
        return cls.__style(36, text)

    @classmethod
    def purple(cls, text: Any):
        return cls.__style(35, text)

    @classmethod
    def blue(cls, text: Any):
        return cls.__style(34, text)

    @classmethod
    def yellow(cls, text: Any):
        return cls.__style(33, text)

    @classmethod
    def green(cls, text: Any):
        return cls.__style(32, text)

    @classmethod
    def red(cls, text: Any):
        return cls.__style(31, text)

    @classmethod
    def grey(cls, text: Any):
        return cls.__style(30, text)

    @classmethod
    def dunderline(cls, text: Any):
        return cls.__style(21, text)

    @classmethod
    def crossline(cls, text: Any):
        return cls.__style(9, text)

    @classmethod
    def invisible(cls, text: Any):
        return cls.__style(8, text)

    @classmethod
    def bgwhite(cls, text: Any):
        return cls.__style(7, text)

    @classmethod
    def blink2(cls, text: Any):
        return cls.__style(6, text)

    @classmethod
    def blink(cls, text: Any):
        return cls.__style(5, text)

    @classmethod
    def underline(cls, text: Any):
        return cls.__style(4, text)

    @classmethod
    def italic(cls, text: Any):
        return cls.__style(3, text)

    @classmethod
    def lite(cls, text: Any):
        return cls.__style(2, text)

    @classmethod
    def bold(cls, text: Any):
        return cls.__style(1, text)
