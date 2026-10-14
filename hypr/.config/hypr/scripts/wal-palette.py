#!/usr/bin/env python3
"""Extract wallpaper colors; let pywal export and apply the resulting theme."""
import colorsys
import json
from pathlib import Path
import subprocess
import sys

from PIL import Image, ImageOps


def luminance(rgb):
    linear = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in rgb]
    return sum(v * weight for v, weight in zip(linear, (0.2126, 0.7152, 0.0722)))


def readable(rgb, background, target=4.5):
    # Adjust only lightness, retaining the source hue and saturation.
    hue, lightness, saturation = colorsys.rgb_to_hls(*rgb)
    for step in range(101):
        candidate = colorsys.hls_to_rgb(hue, lightness + (1 - lightness) * step / 100, saturation)
        candidate = tuple(round(v * 255) / 255 for v in candidate)
        if (luminance(candidate) + 0.05) / (luminance(background) + 0.05) >= target:
            return candidate
    return (1.0, 1.0, 1.0)


def hex_color(rgb):
    return '#' + ''.join(f'{round(v * 255):02x}' for v in rgb)


def generate(wallpaper):
    with Image.open(wallpaper) as source:
        image = ImageOps.exif_transpose(source).convert('RGBA')
        canvas = Image.new('RGBA', image.size, (0, 0, 0, 255))
        image = Image.alpha_composite(canvas, image).convert('RGB')
        image.thumbnail((256, 256), Image.Resampling.LANCZOS)

    pixels = list(image.getdata())
    spreads = [max(pixel) - min(pixel) for pixel in pixels]
    monochrome = sum(spreads) / len(spreads) <= 3 and sum(v > 15 for v in spreads) / len(spreads) <= 0.01
    quantized = image.quantize(colors=32, method=Image.Quantize.MEDIANCUT)
    table = quantized.getpalette()
    samples = []
    for count, index in sorted(quantized.getcolors(), reverse=True):
        rgb = tuple(v / 255 for v in table[index * 3:index * 3 + 3])
        if count / len(pixels) >= 0.002:
            samples.append((count, rgb))

    # Prefer visible chromatic regions over compression noise and near-black pixels.
    ranked = sorted(samples, key=lambda item: item[0] ** 0.5 * (max(item[1]) - min(item[1])), reverse=True)
    accents = [rgb for _, rgb in ranked if max(rgb) - min(rgb) >= 0.04 and max(rgb) >= 0.15]
    dominant = accents[0] if accents else samples[0][1]
    hue, _, saturation = colorsys.rgb_to_hls(*dominant)
    if monochrome:
        saturation = 0
    background = tuple(round(v * 255) / 255 for v in colorsys.hls_to_rgb(hue, 0.035, min(saturation, 0.15)))
    foreground = colorsys.hls_to_rgb(hue, 0.83, min(saturation, 0.06))

    if monochrome:
        chosen = [(level,) * 3 for level in (0.65, 0.72, 0.78, 0.68, 0.75, 0.81)]
    else:
        chosen = []
        for rgb in accents or [rgb for _, rgb in samples]:
            candidate = readable(rgb, background)
            if all(sum((a - b) ** 2 for a, b in zip(candidate, previous)) > 0.012 for previous in chosen):
                chosen.append(candidate)
            if len(chosen) == 6:
                break
        # Few-color images should keep their hues rather than inventing new ones.
        base = chosen[:]
        while len(chosen) < 6:
            chosen.append(base[len(chosen) % len(base)])
        # color4 is the desktop accent; keep it aligned with the dominant color.
        chosen[0], chosen[3] = chosen[3], chosen[0]

    bright = [readable(rgb, background, 7) for rgb in chosen]
    muted = readable(colorsys.hls_to_rgb(hue, 0.40, min(saturation, 0.10)), background, 3)
    values = [background, *chosen, foreground, muted, *bright, (0.94,) * 3]
    return {
        'wallpaper': str(wallpaper),
        'alpha': '100',
        'special': {'background': hex_color(background), 'foreground': hex_color(foreground), 'cursor': hex_color(foreground)},
        'colors': {f'color{i}': hex_color(rgb) for i, rgb in enumerate(values)},
    }


def main():
    wallpaper = Path(sys.argv[1]).expanduser().resolve(strict=True)
    palette = generate(wallpaper)
    cache = Path.home() / '.cache/wal'
    cache.mkdir(parents=True, exist_ok=True)
    theme = cache / 'wallpaper-palette.json'
    theme.write_text(json.dumps(palette, indent=4) + '\n')
    subprocess.run(['wal', '--theme', str(theme), '-n', '-q', '-t', '-e'], check=True)


if __name__ == '__main__':
    main()
