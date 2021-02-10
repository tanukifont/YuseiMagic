from fontmake import __main__
from fontTools.ttLib import TTFont, newTable
import shutil
import subprocess
from glyphsLib.cli import main
import ufoLib2
import ufo2ft #note, requires version 2.19.2
import os

print ("Converting to UFO")
main(("glyphs2ufo", "sources/YuseiMagic.glyphs"))

exportFont = ufoLib2.Font.open("sources/YuseiMagic-Regular.ufo")

exportFont.lib['com.github.googlei18n.ufo2ft.filters'] = [{
    "name": "flattenComponents",
    "pre": 1,
}]

print ("Compiling")
static_ttf = ufo2ft.compileTTF(exportFont, removeOverlaps=True)

static_ttf["DSIG"] = newTable("DSIG")
static_ttf["DSIG"].ulVersion = 1
static_ttf["DSIG"].usFlag = 0
static_ttf["DSIG"].usNumSigs = 0
static_ttf["DSIG"].signatureRecords = []
static_ttf["head"].flags |= 1 << 3        #sets flag to always round PPEM to integer

print ("[Yusei Magic] Saving")
static_ttf.save("fonts/ttf/YuseiMagic-Regular.ttf")

shutil.rmtree("sources/YuseiMagic-Regular.ufo")
os.remove("sources/YuseiMagic.designspace")

subprocess.check_call(
        [
            "ttfautohint",
            "--stem-width",
            "nsn",
            "fonts/ttf/YuseiMagic-Regular.ttf",
            "fonts/ttf/YuseiMagic-Regular-hinted.ttf",
        ]
    )
shutil.move("fonts/ttf/YuseiMagic-Regular-hinted.ttf", "fonts/ttf/YuseiMagic-Regular.ttf")