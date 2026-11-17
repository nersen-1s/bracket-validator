# bracket-validator-lab

Перевіряє, чи правильно закриті дужки `()`, `[]`, `{}`, `<>` у рядку.

## Встановлення

```
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ bracket-validator-lab
```

## Використання

```python
from bracket_validator import validate

validate("{[(<>)]}")                      # все гаразд, нічого не повертає
validate("<div><p>{ test }}</p</div>")    # ValueError: Дужки незбалансовані на позиціях [16, 17]
```

Із командного рядка:

```
python -m bracket_validator
bracket-validator
```

```
Введіть строку: <div><p>{ test }}</p</div>
<div><p>{ test }}</p</div>
                ^^
ValueError: Дужки незбалансовані на позиціях [16, 17]
```

Позиції рахуються з нуля.
