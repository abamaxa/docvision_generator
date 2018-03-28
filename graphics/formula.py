# ./tex2png -T -s 2000 -c "$\sum_{i=0}^\infty x_i$" -o test.png
import random
import os
import shutil
import tempfile
import subprocess

from PIL import Image

LATEX_TEMPLATE = r"""\documentclass{article}
\usepackage[paperwidth=\maxdimen,paperheight=\maxdimen]{geometry}
\pagestyle{empty}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage{amsmath}
\begin{document}
\begin{samepage}
"""

LATEX_TEMPLATE_END = r"""
\end{samepage}
\end{document}        
"""

class Formula :
    def __init__(self) :
        self.working_dir = None
        self._image = None
        
    @property
    def image(self) :
        return self._image
    
    def quadratic(self) :
        # y/0 x2 + 3y - 3
        # '$f(n) = n^2 + 4n + 2 $'
        a = random.choice((' ','2','3'))
        op1 = random.choice(('-','+'))
        b = random.choice((' ','2','3','4','5'))
        op2 = random.choice(('-','+'))
        c = random.choice(('1','2','3','4','5','10','11'))
        eq = random.choice(('f(x)','y',' '))
        
        if eq :
            formula = "{} = {}x^2 {} {}x {} {}".format(eq,a,op1,b,op2,c)
        else :
            formula = "{}x^2 {} {}x {} {} = 0".format(a,op1,b,op2,c)
            
        self.__render_formula(formula)
            
    def __render_formula(self, formula) :
        try :
            self.__make_working_dir()
            self.__write_tex_document(formula)
            self.__convert_tex_to_dvi()
            self.__convert_dvi_to_image()
            self.__read_image()
            
        finally :
            self.__remove_working_dir()

    def __make_working_dir(self) :
        self.working_dir = tempfile.mkdtemp()
        
    def __remove_working_dir(self) :
        if self.working_dir and os.path.exists(self.working_dir) : 
            shutil.rmtree(self.working_dir)
    
    def __write_tex_document(self, formula) :
        tex_doc = "".join([LATEX_TEMPLATE,'$',formula,'$',LATEX_TEMPLATE_END])
        with open(self.__get_tex_filepath(), "w") as tex_file :
            tex_file.write(tex_doc)
                    
    def __convert_tex_to_dvi(self) :
        # latex -halt-on-error content.tex
        cmd = ["latex", "-halt-on-error", self.__get_tex_filepath()]
        subprocess.run(cmd, cwd=self.working_dir, check=True)
    
    def __convert_dvi_to_image(self) :
        # dvipng -q -x "1400" -p "1" --height --depth -T tight -bg "transparent" --png -z 0 -o - content.dvi
        cmd = ["dvipng", "-q", "-x", "1400", "-p", "1", "--height", "--depth"]
        cmd.extend(["-T", "tight", "-bg", "transparent", "--png", "-z", "0", "-o"])
        cmd.append(self.__get_image_filepath())
        cmd.append(self.__get_dvi_filepath())
        subprocess.run(cmd, cwd=self.working_dir, check=True)
        
    def __get_tex_filepath(self) :
        return os.path.join(self.working_dir, "content.tex")

    def __get_dvi_filepath(self) :
        return os.path.join(self.working_dir, "content.dvi")
    
    def __get_image_filepath(self) :
        return os.path.join(self.working_dir, "content.png")        
    
    def __read_image(self) :
        self._image = Image.open(self.__get_image_filepath())
            
