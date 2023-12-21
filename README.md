# Modules

The unit of the QR code. Don't have any specific size. Size of a module should be consistent across the whole QR code.

They have two varieties *light* and *dark*

You can have various QR code sizes which are called: versions. The larger the version, the more data that can be
contained inside of it.

Look up person who stored a book in QR code.

[Gradient QR Codes](https://www.qrcode-monkey.com/)

# Modes

Numeric, Alphanumeric, Byte and Kanji. These are the 4 most basic.

You can also mix QR codes

# Error Correction Level

This level determines how max percentage of data that can be recovered in a partial QR code reading.

There are four correction levels: L, M, Q, H

L: 7%, M: 15%, Q: 25%, H: 30%

# Versions

40 possible versions from 1-40. Each version results in a QR code that is **4 modules wider and taller than the previous
version**.

21 x 21 modules = Version 1

177 x 177 modules = Version 40 *(39 * 4 == 156)*

4 * (version — 1) + 21

