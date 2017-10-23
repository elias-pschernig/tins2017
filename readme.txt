 _____         ______    by Allefant   _   
|  __ \       |  ____|      & AKA     | |  
| |  | |_ __  | |__ ___  _ __ ___  ___| |_ 
| |  | | '__| |  __/ _ \| '__/ _ \/ __| __|
| |__| | |    | | | (_) | | |  __/\__ \ |_ 
|_____/|_|    |_|  \___/|_|  \___||___/\__|

_______________
TINS 2017 entry

The entry implements all 4 of the standard rules (no bonus rule was
used):


____________________________
Theme Rule: Doctors & Health

Well, the game is all about keeping a forest healthy.

________________________________________________________________________
Artistic Rule: The game shall have a pause mode where all the characters
dance to a funky tune

Press the pause button! (or finish a level)

_________________________________________________________
Artistic: The game must include a silly weapon or powerup

There is not only one but five different functions and they are quite
silly, one tosses trees up into the air, one creates a patch of bog to
swallow whole trees, one incinerates a tree, one plants an oak (often
infest by beetles) and one plants a pine (or something else, from time
to time).

______________________________________________________
Technical: Use a morphing effect somewhere in the game

When a tree dies it will do vector morphing into the model without
any leaves. If you play the game you should see it quite often!


___________
How to Play

Press or press-and-hold the left mouse button to activate any of the
5 functions. Note that the first level has only one of the five
available.

Place three bog patches to kill a beetle. But beware, place 5 of them
on a tree and it kills the tree. You can also toss or burn beetles.


_______________
How it was made

All code was written by me during the competition (you can see the
git commits and screenshots in the TINS logs). It uses my old Land
library, which in turn uses Allegro. All graphics are programmatically
created.

If you look at the git repository, I'm actually using my own programming
languages Scramble which looks somewhat like Python. I have a Scramble
to C trans-compiler and for the sake of everyone's sanity the C output
of that is included here, together with two Makefiles I used to create
the Linux and Windows binaries. The Windows binary is included and
should also work in Wine.

The funky pause music was made by AKA.

I added a TTF font since I ran out of time to do a programmatic font as
I had planned originally.

Also, my original idea was to synthesize sound effects and instruments
and do programmatic music. However due to time constraints I used some
samples from soundbible.com instead.

The second piece of music is my old Allefant theme which I just
re-created from scratch in LMMS (using various builtin samples). 
