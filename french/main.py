#! /usr/bin/python3
import readline
import json
from utils import loolike2 as loolike, style as _, T_DICT, frange
from pathlib import Path
import argparse
import os
from string import ascii_lowercase as letters

accentueds = "aáàâä", "eéèêë", "iíìîï", "oóòôöœ", "uúùûü"
voyelles = {k: v for k, v in zip(accentueds, "aeiou")}
all_letters = letters + "".join(voyelles)

parser = argparse.ArgumentParser(
    description="Dictionaire de la langue française via le terminal"
)
parser.add_argument("-w", "--word", default=None)
parser.add_argument("-d", "--deep", default="false", choices=["true", "false"])
parser.add_argument(
    "-p",
    "--precision",
    type=int,
    default=6,
    choices=range(1, 11),
)

class Dicterm:
    def __init__(self) -> None:
        self.parsed = parser.parse_args()
        self.precisions_map = {i + 1: v for i, v in enumerate(frange(0.5, 1, 0.05))}
        self.inverted_precisions_map = {v: k for k, v in self.precisions_map.items()}

        self.precision = self.precisions_map.get(self.parsed.precision)
        most_like: int = 6 if self.parsed.precision < 6 else self.parsed.precision + 1
        most_like = most_like if most_like < 11 else 10
        self.next_precision: float | None = self.precisions_map.get(most_like)

        self.deep: str = self.parsed.deep

    def get_results(self, w: str):
        do_print = lambda f: lambda: self.get_definitions(w, f)
        {
            "true": do_print(self.search_far),
            "false": do_print(self.search_near),
        }[self.deep]()

    def help_(self):
        help_text = _.bggrey(
            _.bold2(_.green2(_.underline("   Aide d'utilisation:   ")))
        )
        print("\t\t\t", help_text, "\n\n\n")

        italipurple = lambda x: _.italic(_.bgpurple(_.bold2(x)))
        colored_list = italipurple(list(range(1, 11)))
        
        d_info = f"La valeur doit être soit {italipurple('true')} soit {italipurple('false')}. Ex:{italipurple('-d true')} ou {italipurple('-d=true')}"
        d_info = _.italic(d_info)
        p_info = f"Le nombre doit être compris dans l'intervalle {colored_list}. Ex: {italipurple('-p 7')}, ou {italipurple('-p=7')}"
        
        commands = {
            f"-p {_.green2('{nombre}')}": f"Modifier la précison de recherche. {p_info}",
            "-p": "Afficher la précison de recherche",
            f"-d {_.cyan('{booléen}')}": f"Activer ou désactiver l'option de recherche en profondeur. {d_info}",
            "-d": "Afficher l'état de l'option de recherche en profondeur",
            "-c": "Nettoyer la console",
            "-k": "Quitter l'application",
            "? | -h": "Obtenir de l'aide",
        }

        for k, v in commands.items():
            print(_.bold(_.blue(k)), "---->", v, "\n")

    def get_voyelle(self, letter: str):
        filtered = tuple(filter(lambda k: letter in k, voyelles.keys()))
        key = filtered and filtered[0]
        return voyelles.get(str(key), letter)

    def file_path(self, letter: str):
        return Path(__file__).parent / f"dico_utils/jsons/{letter}.json"

    def data(self, letter: str):
        letter = self.get_voyelle(letter)
        with open(self.file_path(letter), "r") as f:
            words: list[T_DICT] = json.loads(f.read())
            return words

    def search_near(self, word: str, first_letter: str = ""):
        first_letter = first_letter or word[0].lower()
        word = word.strip().capitalize()
        word_list = self.data(first_letter)

        yield from filter(
            lambda w: loolike(w["Mot"], word) >= self.precision, word_list
        )

    def search_far(self, word: str):
        for found in map(lambda l: self.search_near(word, l), letters):
            yield from found

    def get_definitions(self, word: str, searcher):
        word = word.strip().capitalize()
        for w in searcher(word):
            percent = loolike(w["Mot"], word)
            dumped = json.dumps(w, indent=3, ensure_ascii=False)

            colored = (
                _.bggrey(_.bold(_.purple2(dumped)))
                if percent >= self.next_precision
                else _.italic(dumped)
            )
            print(colored)
            print("\n")

    def __strip(self, char: str, to_get: str):
        return char.replace(to_get, "").replace("=", "").strip()

    def get_precision(self, inputed: str):
        p = int(self.__strip(inputed, "-p"))
        self.precision = self.precisions_map[p]
        return p

    @property
    def inverted_precision(self):
        return self.inverted_precisions_map[self.precision]

    def run(self):
        if word := self.parsed.word:
            self.get_results(word)
        else:
            while True:
                inputed = input(_.bold2(_.purple2(">>> ")))
                inputed = inputed.strip() if inputed else "test"
                if inputed.startswith("-p") and len(inputed) > 2:
                    print(
                        _.green(_.italic(_.bold("Précision modifiée:"))),
                        _.bold(_.yellow(_.blink2(self.get_precision(inputed)))),
                    )
                elif inputed.startswith("-d") and len(inputed) > 2:
                    tampo_deep = self.__strip(inputed, '-d')
                    if tampo_deep in ("true", "false"):
                        self.deep = tampo_deep
                        etat = "activée" if self.deep == "true" else "désactivée"
                        msg = f"Option recherche en profondeur {etat}"
                        colored = _.green(_.italic(_.bold(msg)))
                        print(colored)

                    else:
                        err_msg = _.cyan(f"Paramètre {_.purple(tampo_deep)} invalide")
                        print(err_msg)

                else:
                    case_p = lambda: print(
                        _.cyan2(_.italic("La valeur de la précision est")),
                        _.bold(_.purple2(self.inverted_precision)),
                    )
                    case_d = lambda: print(
                        _.cyan2(_.italic("L'option de recherche en profondeur est")),
                        _.bold(
                            _.purple2("active" if self.deep == "true" else "innactive")
                        ),
                    )
                    case_any = (
                        lambda: self.get_results(inputed)
                        if inputed[0] in all_letters
                        else print(_.bold("Caractères inconnus:"), _.red(inputed))
                    )
                    {
                        "-c": lambda: os.system("clear"),
                        "-d": case_d,
                        "-p": case_p,
                        "-h": self.help_,
                        "?": self.help_,
                    }.get(inputed, case_any)()


if __name__ == "__main__":
    Dicterm().run()
