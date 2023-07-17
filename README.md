# pylinq

- [pylinq](#pylinq)
  - [Features](#features)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Supported types](#supported-types)
  - [Supported methods](#supported-methods)
  - [Non Supported methods](#non-supported-methods)

## Features

- LINQ implementation in Python3
- Supports almost all LINQ methods in .NET
- All methods and types have complete type hints
- Some methods supports overloads

## Dependencies

- Python: >= 3.11
- Package: Nothing

## Installation

Execute shell commands below at your python workspace

```bash
git clone git@github.com:Funny-Silkie/pylinq.git
mv pylinq tmp
cp -r tmp/src/pylinq .
rm -rf tmp
```

## Usage

1. import `pylinq` package
1. `LinqSequence[T]` is LINQ object (think as `IEnumerable<T>` in .NET)
1. `from_iterable()` method creates a new `LinqSequence[T]` instance from an `Iterable[T]` instance
1. Method chain can be described from a instance of `LinqSequence[T]`

```py
from pylinq import LinqSequence

sequence: LinqSequence[int] = LinqSequence.from_iterable(range(10))\
    .where(lambda x: x % 2 == 0)\
    .select(lambda x: x * 10)
for current in sequence:
    print(current)
```

Output
```shell-session
0
20
40
60
80
```

`from_generator()` method creates a new `LinqSequence[T]` instance from a generator function and its arguments.
The instance generated from `from_generator()` supports many times iterations.

```py
from typing import Generator
from pylinq import LinqSequence


def generator(stop: str) -> Generator[str, None, None]:
    yield "A"
    yield "B"
    yield "C"
    yield stop


sequence: LinqSequence[str] = LinqSequence.from_generator(generator, "Finished")
for current in sequence:
    print(current)
for current in sequence:
    print(current)
```

Output

```shell-session
A
B
C
Finished
A
B
C
Finished
```

## Supported types

All types described below can be imported from `pylinq` module.

|       Type in `pylinq` |   Corresponding .NET Type   |
| ---------------------: | :-------------------------: |
|        LinqSequence[T] |      IEnumerable\<T\>       |
| OrderedLinqSequence[T] |   IOrderedEnumerable\<T\>   |
|      Grouping[TKey, T] | IGrouping\<TKey, TElement\> |
|   Lookup[TKey, TValue] |  ILookup\<TKey, TElement\>  |

## Supported methods

- Almost all .NET LINQ methods are supported
- `Except` method is implemented as except**ed** in this library because of collision with `except` keyword
- some methods have overloads and several return types

|       Category       |  Method in `pylinq`   |                                            Return                                            | Corresponding .NET method |
| :------------------: | :-------------------: | :------------------------------------------------------------------------------------------: | :-----------------------: |
|       Creating       |     from_iterable     |                                       LinqSequence[T]                                        |             -             |
|       Creating       |       from_dict       |                              LinqSequence[tuple[TKey, TValue]]                               |             -             |
|       Creating       |    from_generator     |                                       LinqSequence[T]                                        |             -             |
|       Creating       |         empty         |                                       LinqSequence[T]                                        |           Empty           |
|       Creating       |         range         |                                      LinqSequence[int]                                       |           Range           |
|       Creating       |        repeat         |                                       LinqSequence[T]                                        |          Repeat           |
|       Creating       |   default_if_empty    |                                       LinqSequence[T]                                        |      DefaultIfEmpty       |
|    Concatenation     |        concat         |                                       LinqSequence[T]                                        |          Concat           |
|    Concatenation     |        append         |                                       LinqSequence[T]                                        |          Append           |
|    Concatenation     |        prepend        |                                       LinqSequence[T]                                        |          Prepend          |
|       joining        |         join          |                                    LinqSequence[TResult]                                     |           Join            |
|       joining        |      group_join       |                                    LinqSequence[TResult]                                     |         GroupJoin         |
|  Comparing Sequence  |    sequence_equal     |                                             bool                                             |       SequenceEqual       |
| Quantifier Operation |          any          |                                             bool                                             |            Any            |
| Quantifier Operation |          all          |                                             bool                                             |            All            |
| Quantifier Operation |       contains        |                                             bool                                             |         Contains          |
|     Get Element      |      element_at       |                                              T                                               |         ElementAt         |
|     Get Element      | element_at_or_default |                                              T                                               |    ElementAtOrDefault     |
|     Get Element      |         first         |                                              T                                               |           First           |
|     Get Element      |   first_or_default    |                                              T                                               |      FirstOrDefault       |
|     Get Element      |         last          |                                              T                                               |           Last            |
|     Get Element      |    last_or_default    |                                              T                                               |       LastOrDefault       |
|     Get Element      |        single         |                                              T                                               |          Single           |
|     Get Element      |   single_or_default   |                                              T                                               |      SingleOrDefault      |
|      Filtering       |         where         |                                       LinqSequence[T]                                        |           Where           |
|      Filtering       |         where         |                                    LinqSequence[TResult]                                     |          OfType           |
|       Grouping       |      to_look_up       |                                     Lookup[TKey, TValue]                                     |         ToLookup          |
|       Grouping       |       group_by        | LinqSequence[Grouping[TKey, T]]<br>LinqSequence[Grouping[TKey, T2]]<br>LinqSequence[TResult] |          GroupBy          |
|       Ordering       |         order         |                                    OrderedLinqSequence[T]                                    |           Order           |
|       Ordering       |       order_by        |                                    OrderedLinqSequence[T]                                    |          OrderBy          |
|       Ordering       |   order_descending    |                                    OrderedLinqSequence[T]                                    |      OrderDescending      |
|       Ordering       |  order_by_descending  |                                    OrderedLinqSequence[T]                                    |     OrderByDescending     |
|       Ordering       |        then_by        |                                    OrderedLinqSequence[T]                                    |          ThenBy           |
|       Ordering       |  then_by_descending   |                                    OrderedLinqSequence[T]                                    |     ThenByDescending      |
|       Ordering       |        reverse        |                                       LinqSequence[T]                                        |          Reverse          |
|    Set Operation     |       distinct        |                                       LinqSequence[T]                                        |         Distinct          |
|    Set Operation     |      distinct_by      |                                       LinqSequence[T]                                        |        DistinctBy         |
|    Set Operation     |         union         |                                       LinqSequence[T]                                        |           Union           |
|    Set Operation     |       union_by        |                                       LinqSequence[T]                                        |          UnionBy          |
|    Set Operation     |     **excepted**      |                                       LinqSequence[T]                                        |          Except           |
|    Set Operation     |    **excepted_by**    |                                       LinqSequence[T]                                        |         ExceptBy          |
|    Set Operation     |       intersect       |                                       LinqSequence[T]                                        |         Intersect         |
|    Set Operation     |     intersect_by      |                                       LinqSequence[T]                                        |        IntersectBy        |
|     Partitioning     |         skip          |                                       LinqSequence[T]                                        |           Skip            |
|     Partitioning     |       skip_last       |                                       LinqSequence[T]                                        |         SkipLast          |
|     Partitioning     |      skip_while       |                                       LinqSequence[T]                                        |         SkipWhile         |
|     Partitioning     |         take          |                                       LinqSequence[T]                                        |           Take            |
|     Partitioning     |       take_last       |                                       LinqSequence[T]                                        |         TakeLast          |
|     Partitioning     |      take_while       |                                       LinqSequence[T]                                        |         TakeWhile         |
|     Partitioning     |         chunk         |                                    LinqSequence[list[T]]                                     |           Chunk           |
|      Projection      |        select         |                                    LinqSequence[TResult]                                     |          Select           |
|      Projection      |      select_many      |                          LinqSequence[T2]<br>LinqSequence[TResult]                           |        SelectMany         |
|      Projection      |          zip          |                     LinqSequence[tuple[T1, T2]]<br>LinqSequence[TResult]                     |            Zip            |
|      Conversion      |        to_list        |                                           list[T]                                            |          ToList           |
|      Conversion      |        to_dict        |                             dict[TKey, T]<br>dict[TKey, TValue]                              |       ToDictionary        |
|      Conversion      |        to_set         |                                            set[T]                                            |         ToHashSet         |
|      Statistics      |         count         |                                             int                                              |    Count<br>LongCount     |
|      Statistics      |        max_by         |                                              T                                               |           MaxBy           |
|      Statistics      |        min_by         |                                              T                                               |           MinBy           |
|      Statistics      |          sum          |                                            float                                             |            Sum            |
|      Statistics      |        average        |                                            float                                             |          Average          |
|      Statistics      |       aggregate       |                                    TAccumulate<br>TResult                                    |         Aggregate         |

## Non Supported methods

- `Max`, `Min`: Difficult to implement these methods only specific `T` type
- `Cast`: Python doesn't have type casting
