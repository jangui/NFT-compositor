#!/usr/bin/env python3
from PIL import Image
import os
import json
import random
from tqdm import tqdm
from collections import OrderedDict

class Generator:
    def __init__(self, args):
        self.current_assets = set()

        # get random seed
        random.seed(os.urandom(10))

        # get args from file
        self.args = self.get_args(args)
        self.default_rarities = self.args["default_rarities"]
        self.custom_rarities = self.args["custom_rarities"]
        self.subclass_rarities = self.args["subclass_rarities"]
        self.asset_classes = self.args["asset_classes"]

        # make folder for generated assets
        if not os.path.isdir(self.args["save_location"]):
            os.mkdir(self.args["save_location"])

        # initialize asset cache
        self.asset_cache = {}

    def get_args(self, filepath):
        with open(filepath) as f:
            data = json.load(f, object_pairs_hook=OrderedDict)
            return data

    def run(self):
        # generate
        for i in tqdm(range(1, self.args["generate"]+1)):
            self.generate(i)

    def generate(self, current):
        # reset frog
        self.current_assets.clear()

        # create first layer
        assets_iterable = iter(self.asset_classes.items())
        first_asset, first_subclass = next(assets_iterable)
        img = self.add_asset(first_asset, first_subclass, None, superimpose=False)

        # super impose rest of layers
        for asset_class, subclass in assets_iterable:
            img = self.add_asset(asset_class, subclass, img)

        # save image
        path = os.path.join(self.args['save_location'], f"{current}.png")
        img.save(path)

    def get_rarity(self, asset):
        # set rarities
        rarities = self.default_rarities
        if asset in self.custom_rarities:
            rarities = self.custom_rarities[asset]

        # get rarity
        p = 0
        chance = random.random()
        for rarity, percentage in rarities.items():
            percentage = percentage / 100
            p += percentage
            if chance <= p:
                return rarity

    def get_subclass(self, asset):
        chance = random.random()
        r = 0
        for subclass, rarity in self.subclass_rarities[asset].items():
            rarity = rarity / 100
            r += rarity
            if chance <= r:
                return subclass

    def non_compatible(self, asset):
        # check if asset has no incompatibilities
        if asset not in self.args["incompatible"]:
            return False

        for incompatible_asset in self.args["incompatible"][asset]:
            if incompatible_asset in self.current_assets:
                return True

        return False

    def add_asset(self, asset_class,  subclass, img, superimpose=True):
        # handle subclasses
        if subclass:
            # randomly choose subclass
            asset_subclass = self.get_subclass(asset_class)
            # get subsubclass
            asset_subsubclass = self.asset_classes[asset_class][asset_subclass]
            # recurse
            asset = os.path.join(asset_class, asset_subclass)
            return self.add_asset(asset, asset_subsubclass, img)

        # get rarity
        rarity = self.get_rarity(asset_class)
        path = os.path.join(self.args["assets_location"], asset_class, rarity)

        if rarity == "none":
            return img

        # cache asset names
        if path in self.asset_cache:
            assets = self.asset_cache[path]
        else:
            assets = os.listdir(path)
            self.asset_cache[path] = assets

        # select random asset from rarity class
        asset = random.choice(assets)
        path = os.path.join(path, asset)

        # get asset name w/out file extension
        asset_basename = asset.split(".")[0]

        # if non compatible add another asset of same class
        if self.non_compatible(asset_basename):
            return self.add_asset(asset_class, subclass, img)

        # add the compatible asset to current_asset
        self.current_assets.add(asset_basename)

        if not superimpose:
            return Image.open(path)

        # superimpose asset to image
        asset_img = Image.open(path)
        img.paste(asset_img, (0,0), asset_img)
        return img

def main():
    generator = Generator("./settings.json")
    generator.run()

if __name__ == "__main__":
    main()
