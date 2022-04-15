# Dice-Roller
A command line dice roller written in Python.

```
format: xdy + z + dw... !flags #roll comment here
q to quit, f for flags and formatting, ![flags] to set default flags.
e for example inputs.

flags:                  game aliases:

(a)dvantage             shadowrun
(d)isadvantage          (shadowrun, !sr)
default dice (tN)ype    new world of darkness
(eN)xploding dice       (nwod, acc, !nw, new world of darkness)
(sN)uccess check
(rN)epeated rolls
(i)gnore default flags
(h)ide individual rolls

flags with N require a number following the flag.
!e6 would indicate rolls of 6 or greater explode.
use !ad to roll no advantage while advantage or disadvantage is default.

df + x #comment for fate/fudge dice.
