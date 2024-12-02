# MillenniumDB Driver
---

Here you can find the official Python driver for the [MillenniumDB server](https://github.com/MillenniumDB/MillenniumDB).

Check out the driver for different languages!

- [MillenniumDB driver in JavaScript](https://github.com/MillenniumDB/MillenniumDB-driver-javascript)

## Table of contents

1. [Directory structure](#1-directory-structure)
2. [Build instructions](#2-build-instructions)

## 1. Directory structure

```txt
📦millenniumdb_driver
├── 📂docs/ ---------------------------- Documentation generator (Sphinx)
├── 📂src/ ----------------------------- The Python implementation
├── 📜LICENSE
├── 📜README.md
├── 📜pyproject.toml
└── 📜setup.cfg
```

## 2. Build instructions

### Setup

Dependencies:

- Git
- Setuptools
- Wheel
- A running MillenniumDB server instance

### Installation

Install the driver and the dependecies.

```bash
pip install millenniumdb_driver
```

### Usage

After successfully installing the project, you can start using the library in your Python programs.

#### Creating a Driver instance

First you must create a `Driver` instance:

```python
import millenniumdb_driver

url = 'URL for the MillenniumDB server'
driver = millenniumdb_driver.driver(url)
```

When you are done with the driver, you should close it before exiting the application.

```python
driver.close()
```

#### Acquiring a Session

For sending queries to the MillenniumDB server, you must acquire a session instance:

```python
session = driver.session()
```

Then you can send queries through your session.

```python
query = 'MATCH (?from)-[:?type]->(?to) RETURN * LIMIT 10'
result = session.run(query)
```

#### Consuming results

The alternatives for consuming results must never be mixed because it would generate undefined behavior on your client and/or server. It is important to mention that the session must be closed when your operations are done.

```python
result.variables() -> Tuple[str]
```

Returns the list of variables in the result.

```python
result.records() -> List[Record]
```

Returns the list of `Records` in the result.

```python
result.values() -> List[object]
```

Returns the list of values in the result.

```python
result.data() -> List[Dict[str, object]]
```

Returns the list of records in the result as dictionaries.

```python
result.to_df() -> "DataFrame"
```

Returns the result as a Pandas DataFrame.

```python
result.summary() -> object
```

Returns the summary of the result.

```python
for record in result: -> Iterator[Record]
    print(record)
```

Iterates over each record in result.
