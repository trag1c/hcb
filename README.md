[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# hcb

hcb is a Python 3.10+ wrapper library for the [HCB] v3 API. It provides typed
access to organizations, transactions, cards, donations, and other financial
data with both synchronous and asynchronous support.

- [Installation](#installation)
- [Usage](#usage)
  - [Basic example](#basic-example)
  - [Expanding nested objects](#expanding-nested-objects)
  - [Asynchronous usage](#asynchronous-usage)
  - [API reference](#api-reference)
- [License](#license)

## Installation

`hcb` is available on PyPI and can be installed with any package manager:

```sh
pip install hcb
# or
poetry add hcb
# or
uv add hcb
```

You can also install it from source:

```sh
pip install git+https://github.com/trag1c/hcb.git
```

## Usage

### Basic example

```py
import hcb

for txn in hcb.get_organization_transactions("hq"):  # Hack Club HQ
    print(txn.memo, txn.amount_cents)

# or
hq = hcb.get_organization("hq")

for txn in hq.get_transactions():
    print(txn.memo, txn.amount_cents)
```

### Expanding nested objects

By default, related objects like donations, cards, and users are returned as
`None`. Use the `expand` parameter to fetch them:

```py
# Without expand, nested objects have very little data:
txn = hq.get_transactions()[0]
print(txn.card_charge.date)  # None

# With expand, a lot more donation data is included:
txn = hq.get_transactions(expand="card_charge")[0]
print(txn.card_charge.date)  # 2026-03-22 00:00:00


# Multiple objects can be expanded by separating them with commas:
txn = hq.get_transactions(expand="donation,user,organization")[0]
```

### Asynchronous usage

All functions have async equivalents prefixed with `async_`:

```py
import asyncio
import hcb


async def main() -> None:
    ghostty = await hcb.async_get_organization("ghostty")
    transactions = await ghostty.async_get_transactions(expand="donation")
    for txn in transactions:
        if donation := txn.donation:
            print(f"Donation: ${donation.amount_cents / 100:.2f}")


asyncio.run(main())
```

### API reference

See [core.py](src/hcb/core.py).

## License

`hcb` is licensed under the [MIT License]. © [trag1c], 2026

[HCB]: https://hcb.hackclub.com
[mit license]: https://opensource.org/license/mit
[trag1c]: https://github.com/trag1c
