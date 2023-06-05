# simphones

Phone similarity based on PHOIBLE allophone data.

## Interpretation

Each row in `simphones.csv` contains a pair of phones and a similarity score.
To save space, not every pair of phones has an entry in the dataset.

- `0 <= similarity (A, B) <= 1` (higher score means more similar)
- `similarity(A, B) = similarity(B, A)`
- `similarity(A, A) = 1`
- If neither `(A, B)` nor `(B, A)` appear in the dataset, and if `A != B`, then `similarity(A, B) = 0`.

Here's a small sample of the data.

```csv
n̪,ʊɛ,0.43121545775887227
n̪,ʊa,0.43111336275832324
n̪,ʁ̥ʷː,0.38899594774891666
n̪,ʁʷː,0.38899594774891666
n̪,sʼː,0.3427814506713922
t,t̪,0.8946818014216882
t,tʰ,0.8915659055270435
t,t̚,0.8900445610114259
t,tʲ,0.8871978153386992
t,tʷ,0.8860247688311866
t,tː,0.8859568472356656
t,ɾ,0.8858339230223978
t,t̠ʃ,0.885766574261883
t,ts,0.8856616994842816
t,ð,0.8854152257900325
```

## Generating the data

```bash
# Clone the repo.
git clone https://github.com/lggruspe/simphones
cd simphones

# Install some requirements.
python -m venv env
. env/bin/activate
pip install -r requirements.txt

# Generate the data (this can take a while).
python -m simphones <path to output CSV file>
```

## Licenses

Copyright 2023 Levi Gruspe

The scripts in the repository are licensed under [GPLv3 or later](./LICENSES/GNU_GPLv3.txt).

`simphones.csv`, which is a derivative work of [PHOIBLE 2.0](https://phoible.org/), is released under a [Creative Commons Attribution-ShareAlike 3.0 Unported License](./LICENSES/CC_BY-SA_3.0.txt).

PHOIBLE 2.0 by Steven Moran and Daniel McCloy is licensed under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/).
