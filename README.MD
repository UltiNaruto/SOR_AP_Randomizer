# Streets of Rage Archipelago
An Archipelago implementation of Streets of Rage multiworld randomizer using [sor_patcher](https://github.com/UltiNaruto/sor_patcher/tree/b8b4d5a93d636677927add302912fbed39f9334e)

## Setup

To get started or for troubleshooting, see [the Setup Guide](./src/data/setup_en.md).

## Info
### What is randomized in this game?

Any destructibles that is not moving and stage accesses (including final boss access).

### Which items can be in another player's world?

So far only score items (+1000 points, +5000 points), healing items (Apple, Chicken), police and stage access keys.
Any weapon is not spawnable yet, it will change in the future.
Additionally, you can shuffle traps in the game, such as death traps or even game over traps.

### What versions of Streets of Rage are supported?
So far only (W) (REV00) of the MegaDrive release is supported.
There are no plans of supporting GameGear and Master System versions.

### Does the randomizer support /collect?
Yes, it does. It deletes the destructibles before you can even see them.