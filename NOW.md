# NOW

new mode is simplest

interference is the issue

different channels should help
dont use the ones with other stuff on it
1 6 11 don't overlap, but theyre probably kind of full

zones
1 2
3 4
5 6
7 8


 8    4  
 2   10  
 9    3  
 5    7

 then upstairs use two of 1, 6, 11 that are the least used in the building


 ///


 ok. so good plan. do channels, and then use the hardcoded location information for proximity.

- start it up and run diagnostics to see the channel use
- upload new code on a few bays (util, config, topo) and try it; verify with the scanner

 and if it doesn't work?

basically I've lost the timing of communication

==> only send flash messages if you're the leader
would reduce the message volume by an order of magnitude
kind of violates the spirit of it, doesn't it?
but whatever, if it works, it works

if I do this, raise the bump amount to 25
could even make it a config option
