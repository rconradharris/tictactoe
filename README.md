Let's imagine a world where Tic-Tac-Toe isn't a trivially solved
game.

Great players like TGM Alice Kasparov (elo 2950) compete against
hungry upstarts like TIM Bob Carlsen (elo 2675) for the prestigous
Tic-Tac-Toe World Championship.

This projects builds out a Tic-Tac-Toe engine to explore this
imgainary world.

Of course great games should be shared, so a standard file format for
describing a game would be useful. In this world, we have AT3 to do just that.
Inspired by PGN, AT3, or algebraic Tic-Tac-Toe Notation, lets players capture
their masterpiece in a simple plain text file so it can live on for
all time.

But wait, Wikipedia tells us that Tic-Tac-Toe is a specialization of
[m,n,k games](https://en.wikipedia.org/wiki/M,n,k-game)
, so let's support those too! 4x5 Tic-Tac-Toe where it takes 2 in a row to
win? Not sure why you'd want to, but we can do it!

Oh, Connect Four is eerily similar, just slight restrictions on where pieces
can be placed (got to be as low as they can go). So let's support that as well.
Why not?

3D Tic-Tac-Toe? 4D? 60D? Sure! But not right now...

If you want to understand how this all works, I'd start at the test cases and
work backwards.

Also try `make play` to run the game in interactive mode; though the headless,
automated tests are really more of the actual point...
