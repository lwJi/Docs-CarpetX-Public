# Docs-CarpetX

## Grid indexes

Suppose we have 2 ghost points:

The grid index of the box generated with`box_all` should be
```
  face index   -2  -1  0   1   2   3   4
               | x | x | x | x | x | x | ...
  center index   -2  -1  0   1   2   3
```
for the grid index generated with `box_int`, should it be
```
  face index           0   1   2   3   4
                       | x | x | x | x | ...
  center index           0   1   2   3
```

for next tile, is it the following:
The grid index of the box generated with`box_all` should be
```
  face index   5   6   7   8   9   10  11
               | x | x | x | x | x | x | ...
  center index   5   6   7   8   9   10
```
for the grid index generated with `box_int`, should it be
```
  face index           7   8   9   10  11
                       | x | x | x | x | ...
  center index           7   8   9   10
```

