from random import seed
from random import random
import colorsys
import argparse
import os
import numpy as np
from PIL import Image
from PIL import ImageColor
from abc import ABC, abstractmethod

# Must set environment variable IMG_URL before running script
URL = ""
try:
    URL = os.environ["IMG_URL"]
except Exception:
    print("Must run: export IMG_URL=\"my_img_server_url>/\"")


def rgb2hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(int(r * 255 + .5), int(g * 255 + .5),
                                        int(b * 255 + .5))


class Symbol(ABC):
    @abstractmethod
    def js(self, color):
        pass

    @abstractmethod
    def default(self):
        pass


class SimpleFill(Symbol):
    def js(self, color):
        return "{{type: \"simple-fill\", color: \"{}\"}}".format(color)

    def default(self):
        return "{ type: \"simple-fill\" }"


class PictureFill(Symbol):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def js(self, color):
        return "{{type: \"picture-fill\", url: \"{}{}.png\", outline: {{style: \"solid\"}}, width: 5, height: 5}}".format(
            self.url, color)

    def default(self):
        return "{{type: \"picture-fill\", url: \"{}blank.png\", width: 5, height: 5}}".format(
            self.url)


class UVRenderer(ABC):
    '''
    Abstract base class for diffrernt types of Unique Value Renderer objects.
    '''

    template = "{{value: \"{}\", symbol: {}}},\n"

    @abstractmethod
    def unique_value_js(self, value, color):
        pass

    def header(self, var_name, fields, default_symbol):
        head = "var {} = {{\ntype: \"unique-value\",\n".format(var_name)

        field_str = ""
        for i, field in enumerate(fields):
            if i == 0:
                field_str += "field: \"{}\",\n".format(field)
            else:
                field_str += "field{}: \"{}\",\n".format(i + 1, field)

        tail = "fieldDelimiter: \", \",\ndefaultSymbol: {},\nuniqueValueInfos: [\n".format(
            default_symbol)

        return head + field_str + tail

    def footer(self, var_name):
        return "]}};\n export {{ {} }};".format(var_name)


class DomainCrossHatchRenderer(UVRenderer):
    """
    Returns a set of 3 unique value info objects to make hatching work. For example
    if the input to unique_value_js is 麻田藩 and #ec6666, the output will be:

        {value: "Regular, 麻田藩", symbol: {type: "simple-fill", color: "#ec6666"}},
        {value: "Newcomer, 麻田藩", symbol: {type: "picture-fill", url: "http://localhost:3000/nec6666.png", outline: {style: "solid"}, width: 5, height: 5}},
        {value: "Incumbent, 麻田藩", symbol: {type: "picture-fill", url: "http://localhost:3000/iec6666.png", outline: {style: "solid"}, width: 5, height: 5}},
    """
    def __init__(self, cs_name):
        super().__init__()
        self.picture_fill = PictureFill(URL + cs_name + '/')
        self.simple_fill = SimpleFill()

    def unique_value_js(self, value, color):
        entry = ""

        # Regular gets simple fill
        val = "Regular, {}".format(value)
        symbol = self.simple_fill.js(color)
        regular = self.template.format(val, symbol)
        entry += regular

        # Newcomer and Incumbent get picture fill
        NI = ["Newcomer", "Incumbent"]
        for situation in NI:
            val = "{}, {}".format(situation, value)

            # Go from #ec6666 to nec6666 or iec6666
            color_path = situation[0].lower() + color[1:]

            symbol = self.picture_fill.js(color_path)

            entry += self.template.format(val, symbol)

        return entry


class SimpleFillRenderer(UVRenderer):

    simple_fill = SimpleFill()

    def unique_value_js(self, value, color):
        return self.template.format(value, self.simple_fill.js(color))

    def default(self):
        return self.simple_fill.default()


class ImageGenerator:
    def __init__(self, img_path, color_scheme):
        self.path = img_path
        self.cs = color_scheme

        if not os.path.exists(self.path + self.cs):
            os.mkdir(self.path + self.cs)

    def gen_image(self, color, cs_name):

        # produce inc and newc images:
        rgbval = ImageColor.getcolor(color, "RGB")

        im = Image.open('newcomer.png')
        data = np.array(im)
        red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]
        mask = (red == 255) & (green == 255) & (blue == 255)
        data[:, :, :3][mask] = [rgbval[0], rgbval[1], rgbval[2]]

        im = Image.fromarray(data)
        im.save('{}{}/n{}.png'.format(self.path, cs_name, color.strip("#")))

        incumbentim = im.transpose(Image.FLIP_LEFT_RIGHT)
        incumbentim.save('{}{}/i{}.png'.format(self.path, cs_name,
                                               color.strip("#")))


class ArcGISRenderFactory:
    def __init__(self, img_path, js_path, color_scheme):
        self.js_path = js_path

        self.color_scheme = open(color_scheme, "r").readlines()
        self.cs_name = color_scheme.split("/")[-1].split(".")[0]

        # Generate images if specified
        self.images = False
        if img_path:
            self.img_generator = ImageGenerator(img_path, self.cs_name)
            self.images = True

        # Get the values and colors
        self.values, self.colors = [], []
        for i, line in enumerate(self.color_scheme):
            value, color = line.split(',')

            # Generate a random color if one not provided in color_scheme
            if not color.strip():
                hue = i / len(color_scheme) * 360
                satr = .5 + random() / 2
                val = .5 + random() / 2
                rgbtpl = colorsys.hsv_to_rgb(hue, satr, val)
                color = rgb2hex(rgbtpl[0], rgbtpl[1], rgbtpl[2])

            self.values.append(value.strip())
            self.colors.append(color.strip())

    def create_renderer(self, layer_type):
        """
        Create a renderer based on layer type.
        """
        if layer_type == "kuni":
            self.create_simple_uv_renderer(layer_type, ["Dump_Gun_1"])
        elif layer_type == "gun":
            self.create_simple_uv_renderer(layer_type, ["Dump_Gun_1"])
        elif layer_type == "domain":
            self.domain_renderer()

    def domain_renderer(self):
        self.domain_hatch_renderer()
        self.domain_NI_renderers()

    def domain_NI_renderers(self):
        """
        Create and write both the incumbent and newcomer renderers to files.
        """
        simple = SimpleFillRenderer()
        default = PictureFill(URL).default()

        # Make a renderer for both newcomer and incumbent
        NI = ["Newcomer", "Incumbent"]
        for ni in NI:
            var_name = "{}_renderer".format(ni.lower())
            footer = simple.footer(var_name)
            header = simple.header(var_name, ["Dump_Dom13", "Dump_Dom_1"],
                                   default)

            unique_vals = ""
            for domain, color in zip(self.values, self.colors):
                reg = simple.unique_value_js("Regular, " + domain, color)
                other = simple.unique_value_js("{}, {}".format(ni, domain),
                                               color)

                unique_vals += reg + other

            renderer = header + unique_vals + footer
            filename = self.js_path + "{}-{}.js".format(self.cs_name, ni)

            # Write the renderer to the file
            out = open(filename, "w")
            out.write(renderer)
            out.close()

    def domain_hatch_renderer(self):
        """
        Create and write the hatch renderer to a file.
        """
        hatch = DomainCrossHatchRenderer(self.cs_name)
        simple = SimpleFillRenderer()

        var_name = "hatch_renderer"
        footer = hatch.footer(var_name)
        header = hatch.header(var_name, ["Dump_Dom13", "Dump_Dom_1"],
                              simple.default())

        unique_vals = ""
        for domain, color in zip(self.values, self.colors):
            unique_vals += hatch.unique_value_js(domain, color)

            if self.images:
                self.img_generator.gen_image(color, self.cs_name)

        renderer = header + unique_vals + footer
        filename = self.js_path + self.cs_name + "-Hatch" + ".js"

        # Write the renderer to the file
        out = open(filename, "w")
        out.write(renderer)
        out.close()

    def create_simple_uv_renderer(self, name, fields):
        """
        Create a simple renderer that only relies on one field as the key.
        """
        simple = SimpleFillRenderer()
        default = PictureFill(URL).default()

        var_name = "{}_renderer".format(name)
        footer = simple.footer(var_name)
        header = simple.header(var_name, fields, default)

        unique_vals = ""
        for value, color in zip(self.values, self.colors):
            unique_vals += simple.unique_value_js("{}".format(value), color)

        renderer = header + unique_vals + footer
        filename = self.js_path + "{}-{}.js".format(self.cs_name, name)

        # Write the renderer to the file
        out = open(filename, "w")
        out.write(renderer)
        out.close()
