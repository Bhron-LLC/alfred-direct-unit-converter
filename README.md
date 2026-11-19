# Unit Converter — Direct Search for Alfred

Type unit conversions directly into Alfred's normal search, without a `conv` prefix.

- `37 c to f` → `98.6 °F`
- `98.6 f to c` → `37 °C`
- `-40 c to f` → `-40 °F`
- `10 km to miles` → `6.214 mi`

Press Return to copy the result, including its unit. Ordinary arithmetic such as `25*4` produces no results from this workflow and remains available to Alfred's calculator.

## Installation

1. Use Alfred 5.1 or later with Powerpack on macOS 13 or later.
2. Install the official [Unit Converter by the Alfred Team](https://alfred.app/workflows/alfredapp/unit-converter/).
3. Ensure `/usr/bin/python3` works on your Mac. Apple Command Line Tools can provide it; it is not guaranteed to be ready on a fresh macOS installation.
4. Download [Unit-Converter-Direct-Search.alfredworkflow](../../raw/refs/heads/main/Unit-Converter-Direct-Search.alfredworkflow) and open it to import into Alfred.
5. Open Alfred normally and type a conversion.

Keep both workflows installed in the same Alfred preferences library. The original `conv` command continues to work.

## How it works

A Script Filter uses digits and `-`, `+`, and `.` as prefix keywords, without requiring a space. The Python wrapper reconstructs the input, checks whether it looks like a unit query, and locates the original workflow by its bundle identifier (`com.alfredapp.vitor.unitconverter`). It invokes that workflow's `converter` executable and returns the results to Alfred.

The conversion engine is **not bundled or duplicated**. Updates to the original converter are used automatically. Decimal-place and other conversion settings are read from the original workflow's configuration. Return copies the result with its unit; the original workflow's copy-format setting is not applied.

This is an independent companion workflow, not an official Alfred release. It depends on the original workflow's current bundle identifier, executable name, and JSON output interface. Future changes to those interfaces may require an update.

## Files

- `workflow/direct.py`: query handling, original-engine discovery, and result formatting.
- `workflow/info.plist`: Alfred workflow configuration.
- `Unit-Converter-Direct-Search.alfredworkflow`: importable ZIP package containing those two files.

To rebuild the package, ZIP the contents of `workflow/` at the archive root and use the `.alfredworkflow` extension.

## Validation

The wrapper was tested against the installed Unit Converter 2025.1 for Celsius/Fahrenheit conversions in both directions, negative temperatures, kilometer-to-mile conversion, and exclusion of ordinary arithmetic. Live Alfred search interaction was not independently verified through UI automation.

## Credits

The conversion engine is provided by [Vítor Galvão / the Alfred Team](https://github.com/alfredapp/unit-converter-workflow). This repository contains only the companion wrapper and Alfred configuration; it does not redistribute their engine or artwork.
