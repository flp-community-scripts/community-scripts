# NBP
no-bs pitch tools

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