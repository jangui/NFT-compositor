#!/usr/bin/env python3
from PIL import Image
import os
import json
import random
from tqdm import tqdm

class Generator:
    def __init__(self, args):
        # get random seed
        random.seed(os.urandom(10))

        # get args from file
        self.args = self.get_args(args)
        self.default_rarities = self.args["default_rarities"]
        self.custom_rarities = self.args["custom_rarities"]
        self.subclass_rarities = self.args["subclass_rarities"]

        # make folder for generated assets
        if not os.path.isdir(self.args["save_location"]):
            os.mkdir(self.args["save_location"])

        # initialize asset cache
        self.asset_cache = {}

    def get_args(self, filepath):
        with open(filepath) as f:
            data = json.load(f)
            return data

    def run(self):
        # generate
        for i in tqdm(range(1, self.args["generate"]+1)):
            self.generate(i)

        # display the first generated image
        if self.args["display"]:
            import webbrowser
            webbrowser.open(f"{self.args['save_location']}/{1}.png")

    def generate(self, current):
        img = self.add_asset("background", None, superimpose=False)
        img = self.add_asset("frog", img, has_subclass=True)
        img = self.add_asset("mouth", img)
        img = self.add_asset("eyes", img)
        img = self.add_asset("hair", img)
        img = self.add_asset("torso", img)
        img = self.add_asset("bottom", img)
        img = self.add_asset("neck", img)
        img = self.add_asset("forehead", img)
        img = self.add_asset("mouth_accessory", img)
        img = self.add_asset("head_accessory", img)
        img = self.add_asset("sit-able", img)

        # save image
        img.save(f"{self.args['save_location']}/{current}.png")

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


    def add_asset(self, asset_class,  img, has_subclass=False, superimpose=True):
        # get rarity
        if has_subclass:
            asset_subclass = self.get_subclass(asset_class)
            rarity = self.get_rarity(f"{asset_class}.{asset_subclass}")
            path = f"./assets/{asset_class}/{asset_subclass}/{rarity}"
        else:
            rarity = self.get_rarity(asset_class)
            path = f"./assets/{asset_class}/{rarity}"

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
        path = f"{path}/{asset}"

        if not superimpose:
            return Image.open(path)

        # superimpose asset
        asset_img = Image.open(path)
        img.paste(asset_img, (0,0), asset_img)
        return img

def main():
    generator = Generator("./settings.json")
    generator.run()

if __name__ == "__main__":
    main()
