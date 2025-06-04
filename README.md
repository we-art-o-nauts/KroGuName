Krogufant
---

This is a small project made at Code Dojo Bern on June 4, 2025.

![Screenshot](screenshot.png)

Inspired by Krogufant by Sara Ball, a book for small children where you can shuffle the names and pictures of animals together into an imaginary animal:

![](https://www.beltz.de/fileadmin/_processed_/e/a/csm_9783407773050_d03ed479a7.jpg)

_Image source: [beltz.de](https://www.beltz.de/kinderbuch_jugendbuch/produkte/details/6323-krogufant.html)_

# Data source

"Vornamen, ab 1987" (Open use) from the Statistics and Data Service Fribourg is included in Parquet format. It can be freely downloaded from here:
https://opendata.swiss/en/dataset/vornamen-ab-1987

The free version of Claude 3.7 Sonnet and Zed were used to develop the `syllalib.py` library, which splits the names into complementary arrays by syllables.

# How to use

To run the script, install [uv - Astral](https://docs.astral.sh/uv/) and then run:

`uv run syllalib.py`

You will be asked to enter some letters. If they match any of the prefixes or suffixes, then random combinations of new names will be generated. If no match is found, the program will try to just find matching names in the database.

# License

CC0 1.0 Public Domain
