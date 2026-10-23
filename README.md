# g.MOBIlab+ serial protocol notes

Independent documentation and minimal Python scripts for communicating with
a g.MOBIlab+ amplifier over Bluetooth serial (RFCOMM), written for
interoperability (e.g. use on Linux / Raspberry Pi / ARM where the vendor
library is not available).

Based on observing the traffic of a device my university legally owns.

- `protocol.tex`: observed command sequence (Spanish)
- `capture.py`: records raw data from the amplifier
- `plot.py`: plots a captured file

Not affiliated with g.tec. Not a medical device.
Test with a known signal before trusting the output.
