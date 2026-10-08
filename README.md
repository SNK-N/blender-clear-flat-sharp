# Clear Flat Sharp
A Blender add-on that automatically clears Sharp edges on edges that are considered nearly flat.

## Features
* Clear Sharp edges on selected geometry
* Clear Sharp edges across the entire mesh
* Adjustable angle threshold
* Supports Undo
* Works in Edit Mode

## Requirements
* Blender 4.0 or later

## Installation
1. Download `clear_flat_sharp.py` from this repository.
2. Open Blender.
3. Go to `Edit > Preferences > Add-ons`.
4. Click `Install...`.
5. Select `clear_flat_sharp.py`.
6. Enable the add-on.

## Usage
1. Enter Edit Mode.
2. Open the Sidebar with `N`.
3. Open the `Flat Sharp` tab.
4. Adjust the settings.
5. Click `Clear Flat Sharp`.

### Threshold
The add-on compares the angle between the normals of adjacent faces.
If the angle is below the specified threshold, the edge is considered nearly flat and its Sharp setting is cleared.

### Scope
* **Selected** — Process only selected edges.
* **All** — Process all applicable edges in the mesh.

## License

See the `LICENSE` file for license information.
