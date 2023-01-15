(* ::Package:: *)

(* Stencils.wl *)
(* (c) Liwei Ji, 01/2023 *)


GetCoefficient[sample_, value_] := Module[{npts, conds},
    npts = Length[sample];
    conds = Table[Sum[ToExpression["c"<>ToString[i]] sample[[i]]^j, {i, 1, npts}] == value[[j+1]], {j, 0, npts-1}];
    Solve[conds, Table[ToExpression["c"<>ToString[i]], {i, 1, npts}]]
]
