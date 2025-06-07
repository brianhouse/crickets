# NOW


zones

 8    4  
 2   10  
 9    3  
 5    7

 then upstairs use two of 1, 6, 11 that are the least used in the building


## current

the issue now is that if you trigger a bunch, the groups are too small

so the GROUP command has to work even if you're already grouped

that's fine, actually. but it results in orphans

the orphans will keep going just fine, except I want them to stop if there's too few

they could know this if they received reject messages, which is fine

...but then there would be a reject message EVERY TIME we got a ping

we don't even have peers anymore

I guess we could send reject messages at the moment of group switching

