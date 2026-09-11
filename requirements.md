Okay, I think that I need to do a better job of explaining setup to you.  I think that they would best be saved as a json inset a text area.

Let me write a crude example of a setup file.

Rods:
{
    "id": 3,
}
Reels:
{
    "id": 14,
}
Flyline:
{
    "id": 25,
}
Knot:
{
    "id": 4,
}
Leader:
{
    "id": 4,
    "length": "5Ft"
}
Knot:
{
    "id": 1,
}
Hardware:{
    "id": 19,
}
Knot:
{
    "id": 1,
}
Leader:
{
    "id": 4,
    "length": "2Ft"
}
Knot:
{
    "id": 4,
}
tippet:{
    "id": 19,
    "length": "5Ft"
}


This then allows the user to build up their setups completly freely.  They can simply start a the rod and record every part of the setup down to the fly.

This is why I wanted a sort order.  

I hae been thinking and what I want is to have a drop down that offers all the catagories, then a drop down of all the items in the locker of that catagory.  From there if length is needed, then a space for length to be added.  This goes on until the user clicks finnished at the end.   This then causes the setup to be saved as a json inset a text area.  

Lets start with this.
