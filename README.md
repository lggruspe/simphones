# simphones

Phone similarity based on PHOIBLE allophone data.

## Interpretation

Each row in `simphones.csv` contains a pair of phones and a similarity score.
To save space, not every pair of phones is assigned a score.

- `0 <= similarity (A, B) <= 1` (higher score means more similar)
- `similarity(A, B) = similarity(B, A)`
- `similarity(A, A) = 1`
- If neither `(A, B)` nor `(B, A)` appear in the dataset, then `similarity(A, B) = 0`.

Here's a small sample of the data.

```csv
ë,ɛ,0.0020325203252032522
aɪ,ɛ,0.0020304568527918783
eɪ,ɛ,0.0020304568527918783
e̝,ɛ,0.002028397565922921
i̯,ɛ,0.0020161290322580645
ej,ɛ,0.002034587995930824
b,p,0.0650887573964497
b,β,0.04939063502245029
b,mb,0.026472534745201854
b,bʷ,0.026804123711340205
b,bʲ,0.02269601100412655
b,b̚,0.015829318651066758
b,p̚,0.01430517711171662
b,pʰ,0.012385919165580182
b,m,0.007673860911270983
b,w,0.007411067193675889
b,ɓ,0.009433962264150943
b,v,0.008547008547008548
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
