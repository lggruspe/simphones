# simphones

Phone similarity based on PHOIBLE allophone data.

## Interpretation

Each row in `simphones.csv` contains a pair of phones and a similarity score.
To save space, not every pair of phones has an entry in the dataset.

- `0 <= similarity (A, B) <= 1` (higher score means more similar)
- `similarity(A, B) = similarity(B, A)`
- `similarity(A, A) = 1`
- If neither `(A, B)` nor `(B, A)` appear in the dataset, then `similarity(A, B) = 0`.

Here's a small sample of the data.

```csv
fː,ʊa,1.6201569349461534e-11
fː,ʊə̯,5.932486442509328e-10
fː,ʊɛ,1.654628359093944e-11
fː,ʊi,5.7253518261578165e-12
fː,ʊɨ,4.755354402743387e-10
fː,ʊu,3.046657464491683e-09
fː,vː,3.866146283376924e-06
fː,vˑ,1.195342842330567e-06
fː,v̥,0.0001350560482600279
fː,v̩,0.0001378993334865548
fː,v̼,0.00014011162225906638
fː,v,0.0003932677951267566
fː,v͈,2.458656160009343e-05
fː,ṽ,3.019403441365072e-06
fː,v̠,3.0454327813768398e-06
```

## Generating the data

```bash
# Clone the repo.
git clone https://github.com/lggruspe/simphones

# Install some requirements.
python -m venv env
. env/bin/activate
pip install networkx

# Generate the data (this can take a while).
python -m simphones <output file>
```

## Licenses

Copyright 2023 Levi Gruspe

The scripts in this repository are licensed under [GPLv3 or later](./LICENSES/GNU_GPLv3.txt).

`simphones.csv`, which is a derivative work of [PHOIBLE 2.0](https://phoible.org/), is released under a [Creative Commons Attribution-ShareAlike 3.0 Unported License](./LICENSES/CC_BY-SA_3.0.txt).

PHOIBLE 2.0 by Steven Moran and Daniel McCloy is licensed under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/).
