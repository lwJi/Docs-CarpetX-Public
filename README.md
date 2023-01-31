# Docs-CarpetX

## Grid indexes

Suppose we have 2 ghost points:

The grid index of the box generated with`box_all` should be
```
  face index   0   1   2   3   4   5   6
               | x | x | x | x | x | x | ...
  center index   0   1   2   3   4   5
```
but for the grid index generated with `box_int`, should it be
```
  face index           2   3   4   5   6
                       | x | x | x | x | ...
  center index           2   3   4   5
```
or
```
  face index           0   1   2   3   4
                       | x | x | x | x | ...
  center index           0   1   2   3
```
