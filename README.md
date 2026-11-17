# bracket-validator-lab

Перевіряє, чи правильно закриті дужки `()`, `[]`, `{}`, `<>` у рядку.

## Встановлення

```
python -m pip install --upgrade --no-cache-dir --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ batsur-bracket-validator
```

## Використання

```python
from src.bracket_validator import validate

validate("{[(<>)]}")  # все гаразд, нічого не повертає
validate("<div><p>{ test }}</p</div>")  # ValueError: Дужки незбалансовані на позиціях [16, 17]
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
