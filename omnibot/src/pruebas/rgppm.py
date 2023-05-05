#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import mathematica as ma
from wolframclient.language import evaluate

entrada1= """
lista = {};
listaNodos = {};
listaNodosResistencias = {};
CuadradosLado = 5;
NodosLado = CuadradosLado + 1;
NodoInicio = 3;
NodoFinal = 19;
(*NodoFinal=NodosLado^2+CuadradosLado^2;*)
(*NodoFinal=50;*)
NodosTotales = NodosLado^2 + CuadradosLado^2;
orden = NodosTotales + 2;
ValorDeFuenteInicio = 10;
ValorDeFuenteFinal = 0;
Timing[
 
 For[i = 1,
  i <= NodosLado^2 + CuadradosLado^2,
  AppendTo[listaNodos, {i}];
  AppendTo[listaNodosResistencias, {i}];
  i++
  ];
 
 
 
 For[j = 1,
  j <= NodosLado - 1,
  seguimiento = Length[lista];
  NodoInicial = 1 + ((j - 1)*(2*NodosLado - 1));
  For[i = NodoInicial,
   i <= NodoInicial + (NodosLado - 1),
   seguimiento = Length[lista];
   If[i == NodoInicial + (NodosLado - 1),
    Goto[salir],
    AppendTo[
     lista, {ToExpression[StringJoin["R", ToString[seguimiento + 1]]],
       i, i + 1, 1}];
    AppendTo[listaNodos[[i]], {i + 1, 1}];
    AppendTo[listaNodos[[i + 1]], {i, 1}];
    AppendTo[listaNodosResistencias[[i]], seguimiento + 1];
    AppendTo[listaNodosResistencias[[i + 1]], seguimiento + 1]
    ];
   Label[salir];
   i++ 
   ];
  For[i = NodoInicial,
   i <= NodoInicial + (NodosLado - 1),
   seguimiento = Length[lista];
   AppendTo[
    lista, {ToExpression[StringJoin["R", ToString[seguimiento + 1]]], 
     i, i + (2*NodosLado - 1), 1}];
   AppendTo[listaNodos[[i]], {i + (2*NodosLado - 1), 1}];
   AppendTo[listaNodos[[i + (2*NodosLado - 1)]], {i, 1}];
   AppendTo[listaNodosResistencias[[i]], seguimiento + 1];
   AppendTo[listaNodosResistencias[[i + (2*NodosLado - 1)]], 
    seguimiento + 1];
   i++ 
   ];
  For[i = NodoInicial,
   i <= NodoInicial + (NodosLado - 1),
   seguimiento = Length[lista];
   If[i == NodoInicial + (NodosLado - 1),
    Goto[salir],
    AppendTo[
     lista, {ToExpression[StringJoin["R", ToString[seguimiento + 1]]],
       i, i + NodosLado, 0.7}];
    AppendTo[listaNodos[[i]], {i + NodosLado, 0.7}];
    AppendTo[listaNodos[[i + NodosLado]], {i, 0.7}];
    AppendTo[listaNodosResistencias[[i]], seguimiento + 1];
    AppendTo[listaNodosResistencias[[i + NodosLado]], seguimiento + 1];
    seguimiento = Length[lista];
    AppendTo[
     lista, {ToExpression[StringJoin["R", ToString[seguimiento + 1]]],
       i + NodosLado, i + 2*NodosLado, 0.7}];
    AppendTo[listaNodos[[i + NodosLado]], {i + 2*NodosLado, 0.7}];
    AppendTo[listaNodos[[i + 2*NodosLado]], {i + NodosLado, 0.7}];
    AppendTo[listaNodosResistencias[[i + NodosLado]], seguimiento + 1];
    AppendTo[listaNodosResistencias[[i + 2*NodosLado]], 
     seguimiento + 1]
    ];
   Label[salir];
   i++ 
   ];
  For[i = NodoInicial,
   i <= NodoInicial + (NodosLado - 1),
   seguimiento = Length[lista];
   If[i == NodoInicial,
    Goto[salir],
    AppendTo[
     lista, {ToExpression[StringJoin["R", ToString[seguimiento + 1]]],
       i, i + (NodosLado - 1), 0.7}];
    AppendTo[listaNodos[[i]], {i + (NodosLado - 1), 0.7}];
    AppendTo[listaNodos[[i + (NodosLado - 1)]], {i, 0.7}];
    AppendTo[listaNodosResistencias[[i]], seguimiento + 1];
    AppendTo[listaNodosResistencias[[i + (NodosLado - 1)]], 
     seguimiento + 1];
    seguimiento = Length[lista];
    AppendTo[
     lista, {ToExpression[StringJoin["R", ToString[seguimiento + 1]]],
       i + (NodosLado - 1), i + (2*NodosLado - 2), 0.7}];
    AppendTo[
     listaNodos[[i + (NodosLado - 1)]], {i + (2*NodosLado - 2), 
      0.7}];
    AppendTo[
     listaNodos[[i + (2*NodosLado - 2)]], {i + (NodosLado - 1), 
      0.7}];
    AppendTo[listaNodosResistencias[[i + (NodosLado - 1)]], 
     seguimiento + 1];
    AppendTo[listaNodosResistencias[[i + (2*NodosLado - 2)]], 
     seguimiento + 1]
    ];
   Label[salir];
   i++ 
   ];
  j++ 
  ];
 For[i = NodoInicial + (2*NodosLado - 1),
   i <= NodoInicial + ((3*NodosLado) - 2),
   seguimiento = Length[lista];
   If[i == NodoInicial + ((3*NodosLado) - 2),
    Goto[salir],
    AppendTo[
     lista, {ToExpression[StringJoin["R", ToString[seguimiento + 1]]],
       i, i + 1, 1}];
    AppendTo[listaNodos[[i]], {i + 1, 1}];
    AppendTo[listaNodos[[i + 1]], {i, 1}];
    AppendTo[listaNodosResistencias[[i]], seguimiento + 1];
    AppendTo[listaNodosResistencias[[i + 1]], seguimiento + 1]
    ];
   Label[salir];
   i++ 
   ]
  
  AppendTo[
   lista, {ToExpression[StringJoin["V", ToString[1]]], NodoInicio, 
    ValorDeFuenteInicio}];
 AppendTo[
  lista, {ToExpression[StringJoin["V", ToString[2]]], NodoFinal, 
   ValorDeFuenteFinal}];
 ]
"""
entrada2= """

lista;

"""

entrada3="""
listaNodos;"""
entrada4="""

listaNodosResistencias; """

entrada5="""

Timing[
 A = Table[0, {i, orden}, {j, orden}];
 B = Table[0, {i, orden}, {j, 1}];
 For[i = 1,
  i <= Length[lista] - 2,
  A[[lista[[i, 2]], lista[[i, 2]]]] = 
   A[[lista[[i, 2]], lista[[i, 2]]]] + 1/lista[[i, 4]];
  A[[lista[[i, 3]], lista[[i, 3]]]] = 
   A[[lista[[i, 3]], lista[[i, 3]]]] + 1/lista[[i, 4]];
  A[[lista[[i, 2]], lista[[i, 3]]]] = 
   A[[lista[[i, 2]], lista[[i, 3]]]] - 1/lista[[i, 4]];
  A[[lista[[i, 3]], lista[[i, 2]]]] = 
   A[[lista[[i, 3]], lista[[i, 2]]]] - 1/lista[[i, 4]];
  i++
  ];
 A[[NodoInicio, NodosTotales + 1]] = 
  A[[NodoInicio, NodosTotales + 1]] + 1;
 A[[NodosTotales + 1, NodoInicio ]] = 
  A[[NodosTotales + 1, NodoInicio ]] + 1;
 A[[NodoFinal, NodosTotales + 2]] = 
  A[[NodoFinal, NodosTotales + 2]] + 1;
 A[[NodosTotales + 2, NodoFinal ]] = 
  A[[NodosTotales + 2, NodoFinal ]] + 1;
 B[[NodosTotales + 1, 1]] = 
  B[[NodosTotales + 1, 1 ]] + ValorDeFuenteInicio;
 B[[NodosTotales + 2, 1]] = 
  B[[NodosTotales + 2, 1 ]] + ValorDeFuenteFinal;
 
 ]"""


entrada6="""

MatrixForm[A];
"""
entrada7= """

MatrixForm[B];
"""
entrada8="""

Timing[
 Voltajes = LinearSolve[N[A], N[B], Method -> "Multifrontal"];
 ]"""

entrada9="""

Voltajes"""

entrada10="""

voltajes = Flatten[Voltajes]"""


entrada11="""

LongitudTotal = {};
NodoFlotante = NodoInicio;
LongitudResistencias = Length[lista];
NodosReferencia = {0};
While[NodoFlotante != NodoFinal,
  (*Print[NodoFlotante];*)
  ResistenciasDinamicas = {};
  NodosDinamicos = {};
  CorrientesParaMax = {};
  
  For[i = 2,
   i <= Length[listaNodos[[NodoFlotante]]],
   AppendTo[NodosDinamicos, listaNodos[[NodoFlotante, i, 1]]];
   AppendTo[ResistenciasDinamicas, listaNodos[[NodoFlotante, i, 2]]];
   i++
   ];
  
  (*Print[NodosDinamicos];*)
  (*Print[ResistenciasDinamicas];*)
  
  AppendTo[NodosReferencia, NodoFlotante];
  
  For[i = 1,
   i <= Length[ResistenciasDinamicas],
   Corriente = (
    voltajes[[NodoFlotante]] - voltajes[[NodosDinamicos[[i]]]])/
    ResistenciasDinamicas[[i]];
   AppendTo[CorrientesParaMax, Corriente];
   i++
   ];
  
  (*Print[CorrientesParaMax];*)
  
  MaximaCorriente = Max[CorrientesParaMax];
  
  AppendTo[LongitudTotal, 
   ResistenciasDinamicas[[
    Position[CorrientesParaMax, MaximaCorriente][[1, 1]]]]];
  
  (*Print[MaximaCorriente];*)
  
  NodoFlotante = 
   NodosDinamicos[[
    Position[CorrientesParaMax, MaximaCorriente][[1, 1]]]]
  
  ];

AppendTo[NodosReferencia, NodoFinal]; """

entrada12="""

NodosReferencia"""



res1 = evaluate(entrada1)


