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

```
> 2d20 + 5

rolls 2 20-sided dice and adds 5 to the total.

> !ae6t6

sets advantage, rolls of 6+ explode, and default die is 6 as default flags

> shadowrun

sets flags for shadowrun rolls to default.

> 10d10 - 5 !hir4 #to hit

rolls 10d10 - 5 four seperate times. (to hit) is noted next to the result.
default flags are ignored, and the indidual rolls are hidden.

> df - 1 #lockpicking check

rolls 4 fate/fudge dice (-0+), subtracts one, and echoes comment 'lockpicking check.'
