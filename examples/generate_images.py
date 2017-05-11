from subprocess import run


# Compile examples and export them as images
#
# Dependencies:
# * LaTeX distribution (MiKTeX or TeXLive)
# * ImageMagick
#
# Known issue: ImageMagick's "convert" clashes with Windows' "convert"
# Please make a symlink to convert:
# mklink convert-im.exe <path to ImageMagick's convert.exe>


# Compile the LaTeX document with examples
num_runs = 2
for i in range(num_runs):
    run(["pdflatex", "--interaction=nonstopmode", "_examples.tex"])

# Convert pdf to png
#
# Optional: If you do not want a transparent background, add
#
# "-background", "white",
# "-alpha", "remove",
#
# to the call arguments
page_exists = True
page_num = 0
while page_exists:
    print("Processing page {:d}".format(page_num + 1))
    ret_val = run([
        "convert-im",
        "-density", "1600",
        "-trim",
        "-resize", "12.5%",
        "-quality", "100",
        "_examples.pdf[{:02d}]".format(page_num),
        "_examples-{:02d}.png".format(page_num),
        ]).returncode
    page_num += 1
    page_exists = ret_val == 0
