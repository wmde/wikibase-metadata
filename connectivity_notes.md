### Initial Data

We query the endpoint for links between items, which returns non-unique directional links such as:

```
a -> b
a -> b
b -> c
```

### Computations

We compute the distance matrix (actually, we compute a subset for performance reasons):


| from \ to | a | b | c |
| - |---|---|---|
| a | 0 | 1 | 2 |
| b |   | 0 | 1 |
| c |   |   | 0 |

#### average distance:

average of non-zero distances in the grid above

```
4 / 3
```

#### connectivity:

number of populated non-zero distances in the grid above (`k`) divided by the number of possible non-zero distances between two items (`n (n-1)`),

```
k / (n (n - 1))
```

* `k` is number of non-zero, populated connections
* `n` is number of items
3 / 6 = 0.5

#### item relationship counts:

* `a` links to `{b, c}` (including indirect connections) -> `a` has 2 links
* `b` links to `{c}` -> `b` has 1 link
* `c` links to `{}` -> `c` has 0 links

We summarize as:

* 1 item has 0 links
* 1 item has 1 link
* 1 item has 2 links

#### object relationship counts:
* `a` is linked to by `{}` -> `a` has 0 links
* `b` is linked to by `{a}` -> `b` has 1 link
* `c` is linked to by `{a, b}` (including indirect connections) -> `c` has 2 links

We summarize as:

* 1 object has 0 links
* 1 object has 1 link
* 1 object has 2 links
