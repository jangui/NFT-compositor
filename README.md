# NFT Compositor

A tool for randomly generating images. Images are created by superimposing different asset classes based on their rarities.

## Settings
To edit settings, edit the settings.json file. The current settings are meant for demonstration purposes.

Your assets should be organized in the following structure:

- assets

  - asset class a
    - rarity category a
        - asset1.png
        - asset2.png
    - rarity category b
        - asset3.png

  - asset class b
    - asset subclass a
        - rarity category a
            - asset4.png
            - asset5.png
        - rarity category b
            - asset6.png
            - asset7.png
        - rarity category c
            - asset8.png
            - asset9.png

### Asset Classes
The order the layers get superimposed is the order they are defined in "asset_classes"
Asset classes can also have subclasses and subclasses can have subsubclasses, etc ad infinitum.

### Asset Subclasses
Subclass rarities must be defined in "subclass_rarities". Subsubclasses are also defined here. An example can be seen in settings.json.
**Rarities must add up to 100 and ordered from largest to smallest probability**

### Default Rarities
The default rarities can be defined, but these will only work for classes and subclasses that have the **exact** rarity classes mentioned in the default rarities.
**Rarities must add up to 100 and ordered from largest to smallest probability**

### Custom Rarities
If an asset class does not have the **exact** rarity classes as the default rarities a custom rarity **must** be defined. Examples can be found in settings.json.
**Rarities must add up to 100 and ordered from largest to smallest probability**

### Incompatibility
Incompatible assets can be defined. However, assets can only be incompatible with layers before them. In essecence, nothing in layer 1 can be incompatible with any asset; however, assets in layers above can be incompatible with assets in layer 1.
**Incompatibility only works if each asset has a unique name.**
To define incompatibility, the asset name is a key in the "incompatible" section and the incompatible assets are specified as a list. 
**Asset names must be specified without their file extensions**

## Running

### Installing dependencies
```
cd <NFT Compositor folder location>
python3 -m pip install -r requirements.txt
```

### Generate
```
cd <NFT Compositor folder location>
python3 generate.py
```
