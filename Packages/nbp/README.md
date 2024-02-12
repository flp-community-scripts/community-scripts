# NBP
no-bs pitch dependent tools

**What do I mean by "pitch dependent?"**: Simply that all operations are confined within each pitch/note. (i.e. each set over operations run for each pitch separately, C4, F3, D5...).

**Why tools?**: By tools I'm implying that these are utility functions intended to save time rather than 'enhance your creative output', well technically by saving time you do, but these tools are intended to streamline some annoying operations that are mostly manual otherwise. So you can treat these almost like macros :)

**What's the point**?: Say I want a legato but I want a legato for each pitch separately at once, technically there isn't such a thing but I find myself often needing something like that. What if what I want is not a legato say, what if I want to join notes across pitch? Or what if I want to normalize a chord that was generated from a guitar audio sample? You could say quantize but what if quantize behaves in a very annoying way?

Since there is a set of these problems that somehow can all fit by into this framework of treating each pitch as its own thing there is a few such tools that kind of achieve this intended result faster than any fl pianoroll speedrun kiddie can do, well okay ofc if you've got everything in your head and you are just transcribing your thoughts maybe there are diminishing returns but if you often freestyle or like to experiment in real time this is package has a bunch of useful time saving tools. 

## Contents

> Currently all tools operate on pitch basis, meaning operations are applied for each pitch separately

`nbplink` - stretches notes to fill in the gaps in between

---

`nbpspacearound` - out of selection will take a note of the earliest note and the latest note and stretch out the first and last notes to make like a chord block, however without changing anything in the middle should there be multiple notes for one pitch

---

`nbpstretch` - out of selection will take a note of the earliest note and the latest note and stretch out all notes by filing the gaps (will ignore overlaps)

---

`nbpweld` - merges notes into one, from the earliest note selected for the pitch to the latest

---


`nbpweldwrap` - merges all notes into one and also makes notes for each pitch same length based on the earliest and latest note. So essentially like a chord normalizes flattening tool type thing. Useful for quickly normalizing let say melodyne generated midis.



## Authors

- @fruitybagel