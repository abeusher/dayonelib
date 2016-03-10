# DayOneLib

A [Python](http://python.org) library for creating [DayOne](http://dayoneapp.com/) entries.

## Installation
``
pip install dayonelib
``
### Dependencies
* tzlocal
* pyobjc-framework-CoreLocation
* plistlib
* uuid
* arrow

## About
There are numerous tools to interact with DayOne. I have used [jrnl](https://maebert.github.io/jrnl/) and the DayOne CLI extensively in the past. However, they were both missing a few features. I also found that I had to write a lot of redundant code to use these tools.

This lib was created to offload some of the common chores of creating entries for DayOne, to provide a fuller set of features, and to make scripts interacting with DayOne cleaner.


Each DayOneEntry is only required to have the `text` property populated to create the journal entry.

dayonelib features:
* Location
  * Will use Location Services to find current location
* Tags
* Entry Text
* Date
* Starring
* UUID

Most of these will be automatically populated by DayOneLib but can be overloaded with custom values. The location serivce will require you to allow python access to location in the MacOS Privacy settings.
	
## Hello World
```python
import dayonelib
journal_location = '<path to journal>'
	
dayone = dayonelib.DayOne(journal_location)
	
entry = dayonelib.DayOneEntry()
entry.text = "I tried out dayonelib today!"
dayone.save(entry)
```

Additional examples can be found in `examples/`
*Heads up they are pretty dirty*

## Many Thanks
* [Kevin Landreth](https://github.com/crackerjackmack)
* [Kevin McDonald](https://github.com/sudorandom)
