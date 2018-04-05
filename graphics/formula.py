"""
This module relies on Latex. To install on mac osx

1. Download BasicTeX, the basic version of MacTex,
(http://tug.org/mactex/) and install the pkg file.

2. Install “dvipng” by executing the following commands

$ sudo tlmgr update --self
$ sudo tlmgr install dvipng

And on Ubuntu, execute the following commands

$ sudo apt install texlive-latex-base dvipng
"""
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
    def __init__(self, text_size) :
        self.working_dir = None
        self._image = None
        self.latex_stdout = None
        self.dvipng_stdout = None
        self.text_size = str(text_size * 80)
        self.__calculate_random_value_dict()
        
    @property
    def image(self) :
        return self._image
    
    def generate_quadratic(self) :
        a = random.choice(('','2','3'))
        op1 = random.choice(('-','+'))
        b = random.choice(('','2','3','4','5'))
        op2 = random.choice(('-','+'))
        c = random.choice(('1','2','3','4','5','10','11'))
        eq = random.choice(('f(x)','y'))
        
        if random.random() > 0.35 :
            formula = "{eq} = {a}x^2 {op1} {b}x {op2} {c}".format_map(self.values)
        else :
            formula = "{a}x^2 {op1} {b}x {op2} {c} = 0".format_map(self.values)
            
        self.__render_formula(formula)
        
    def generate_intergral(self) :
        formula = "\int "
        
        styles = [
            "x{trig} {a}x dx",
            "{b}x{trig}^{a}x dx",
            "\\frac{{x^{pow}}}{{y^{pow2}}} dx",
            "\\frac{{x^{pow}}}{{ {a}{trig}^{pow2}x {op1} {b}{trig2} {c}y }} dx",
            "{a}x^2 {op1} {b}x {op2} dx"
            "\\sqrt{{x{trig} {a}x}} dx",
            "\\sqrt{{{b}x{trig}^{a}x}} dx",
            "\\sqrt{{\\frac{{x^{pow}}}{{y^{pow2}}}}} dx",
            "\\sqrt{{\\frac{{x^{pow}}}{{ {a}{trig}^{pow2}x {op1} {b}{trig2} {c}y }}}} dx",
            "\\sqrt{{{a}x^2 {op1} {b}x {op2}}} dx"            
        ]
        
        formula += random.choice(styles).format_map(self.values)
        self.__render_formula(formula)
        
    def generate_inequalities(self) :
        styles = [
            "{a}x^2 {op1} {b}x",
            "\\sqrt{{{a}x^2 {op1} {b}x}}"
        ]
        
        lhs = random.choice(styles).format_map(self.values)
        rhs = random.choice(styles).format_map(self.values)
        
        formula = " ".join([lhs,self.values['iq'], rhs])
        
        self.__render_formula(formula)  
        
    def generate_surds(self) :
        # include some fractions
        styles = [
            "{a}x^2 {op1} {b}x",
            "\\sqrt{{{a}x^2 {op1} {b}x}}"
        ]
        
        formula = random.choice(styles).format_map(self.values)
        
        self.__render_formula(formula)          
        
    def generate_trig(self) :
        # include some fractions
        styles = [
            "{trig} {A} {op1} {trig2} {B}",
            "{trig} {A} {trig2} {A}",
            "({a} {op1}{trig} {B})({b} {op1} {trig2} {A})",
            "\\frac{{ {a} {op1}{trig} {B}}}{{{b} {op1} {trig2} {A}}}",
            "\\sqrt{{{trig} {A} {op1} {trig2} {A}}}",
            "\\sqrt{{{trig} {A}{trig2} {B}}}",            
        ]
        
        formula = random.choice(styles).format_map(self.values)
        formula = styles[0].format_map(self.values)
        
        self.__render_formula(formula)         
     
        
    def generate_factorizations(self) :
        styles = [
            "{a}x^{pow} {op1} {b}x^{pow2}",
            "(1 {op1} x)^{pow} {op2} {c}",
            "(y {op1} x)^{pow} {op2} {b}y",
            "{a}x^2 {op1} {b}x",
        ]

        formula = random.choice(styles).format_map(self.values)
        
        self.__render_formula(formula)     
        
    def generate_angle_ranges(self) :
        formula = "{}^\circ \leq \\theta \leq {}^\circ".format(random.randint(20,50), random.randint(50,80))
        
        self.__render_formula(formula)     
        
    def __calculate_random_value_dict(self) :
        self. values = {
            "a" : random.choice(('','2','3')),
            "b" : random.choice(('','2','3','4','5')),
            "c" : random.choice(('1','2','3','4','5','10','11')),
            "op1": random.choice(('-','+')),
            "op2" : random.choice(('-','+')),
            "eq" : random.choice(('f(x)','y', None)),
            "pow" : random.randint(2,6),
            "pow2" : random.randint(2,6),
            "trig" :random.choice(("\\sin", "\\cos", "\\tan")),
            "trig2" :random.choice(("\\sin", "\\cos", "\\tan")),
            "A" : random.choice(("A", "B", "\\theta")),
            "B" : random.choice(("A", "B", "\\theta")),
            "iq" : random.choice(("\\leq", "\\geq" "\\neq", ">", "<"))
        }
            
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
        cmd = ["latex", "-halt-on-error", self.__get_tex_filepath()]
        result = subprocess.run(cmd, cwd=self.working_dir, check=True, stdout=subprocess.PIPE)
        self.latex_stdout = result.stdout
        
    def __convert_dvi_to_image(self) :
        # dvipng is not available in brew or the light version of mactex, although
        # it is readily available on linux/docker.
        cmd = ["dvipng", "-q", "-x", self.text_size, "-p", "1", "--height", "--depth"]
        cmd.extend(["-T", "tight", "-bg", "transparent", "--png", "-z", "0", "-o"])
        cmd.append(self.__get_image_filepath())
        cmd.append(self.__get_dvi_filepath())
        result = subprocess.run(cmd, cwd=self.working_dir, check=True, stdout=subprocess.PIPE)
        self.dvipng_stdout = result.stdout
        
    def __get_tex_filepath(self) :
        return os.path.join(self.working_dir, "content.tex")

    def __get_dvi_filepath(self) :
        return os.path.join(self.working_dir, "content.dvi")
    
    def __get_image_filepath(self) :
        return os.path.join(self.working_dir, "content.png")        
    
    def __read_image(self) :
        self._image = Image.open(self.__get_image_filepath())
            
