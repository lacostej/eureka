import os
from fileset import *

def pdf_combine(paths):
  y = [ ("\includepdf[pages=-]{" + p + "}\n") for p in paths ]
  x = "".join(y)
  return '''
\documentclass[portrait]{article}
\usepackage{pdfpages}

\\begin{document}

''' + x + '''
\end{document}
'''

def pdf_combine_to_file(f, paths):
  with open(f, "w") as combinedPdf:
    combinedPdf.write(pdf_combine(paths))
  os.system("pdflatex " + f + " 2>&1 > combined.out")

def pdf_all_combine_to_file(f, dir, include_pattern, exclude_pattern):
  l = FileSet(dir, include_pattern, exclude_pattern).find_paths()
  l.sort()
  pdf_combine_to_file(f, l)

if __name__ == '__main__':
  import sys
  pdf_all_combine_to_file("combined.latex", "gen/pdfs/", "**.pdf", "**_result.pdf")
  pdf_all_combine_to_file("results_combined.latex", "gen/pdfs/", "**_result.pdf", None)
