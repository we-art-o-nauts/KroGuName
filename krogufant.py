from random import shuffle
from syllalib import get_name_arrays

file_path = "01_04_prenom.parquet"

krogufant = r"""

            _ ___                _______________
           _@)@) \            ,,/ '` ~ `'~~ ', `\.
_/o\_ _ _ _/~`.`...'~\        ./~~..,T`,'',.,' '  \
/ `,'.~,~.~  . K , . , ~|,   ,/ .,'N, ,. .. ,,.      \_
( ' _' _ '_` _  ' R.    , `\_/ .'A..' '  `  `   `.    |_
~V~ V~ V~ V~ ~\ `   'O .G' U  F ' .,.,''`.,.''`.,.`   '\_
_/\ /\ /\ /\_/, . ' ,   `_/~\_ .' .,. ,|         |   / \\
&lt; ~ ~ '~`'~'`, .,  .   `_: ::: \_ ' |    `_/  |__    **
\ ' `_  '`_    _    ',/ _::_::_ \ _    | _::_::_ \
`'~~ `'~~ `'~~ `'~~  \(_)(_)(_)/  `~~' \(_)(_)(_)/

"""

if __name__ == "__main__":
    print(krogufant)
    names, prefixes, suffixes = get_name_arrays(file_path)

    ratio = round(100*(len(prefixes)/len(suffixes)))

    print(f"Loaded {len(names)} names ({ratio}%)")

    if prefixes is None or suffixes is None:
        print("No prefixes or suffixes found")
        exit()

    print("Start typing letters and press ENTER to see more combinations")
    print("Type Q to quit")
    print("--- READY ---")

    old_input = None
    while True:
        user_input = input("> ")
        if old_input is not None and user_input is None:
            user_input = old_input
        if user_input.lower() == 'q':
            break
        old_input = user_input

        # Randomize the order
        shuffle(prefixes)
        shuffle(suffixes)

        # Process user input
        new_names = []
        for p in prefixes:
            if user_input.lower() in p.lower():
                for j in suffixes[:10]:
                    if p + j not in new_names:
                        new_names.append(p + j)
                break

        # Go backwards
        for s in suffixes:
            if user_input.lower() in s.lower():
                for j in prefixes[:10]:
                    if j + s not in new_names:
                        new_names.append(j + s)
                break

        if len(new_names) == 0:
            for n in names:
                if user_input.lower() in n.lower() and n not in new_names:
                    new_names.append(n)

        shuffle(new_names)
        print(" ".join(new_names[:10]))
