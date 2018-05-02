import json
import os
import logging
import random

from page_fragments import Question

class MissingTemplateException(Exception) :
    pass

class FragmentFactory :
    def __init__(self, page) :
        self.parameters = page.parameters
        self.templates = {}
        self.templates_by_path = {}
        self.live_templates = {}
        self.template_groups = {}
        self.template_dir = None
        
        self.__set_template_dir()
        self.__load_templates_in_directory()
        
    def __set_template_dir(self) :
        if self.parameters.get("fragment_templates_dir") :
            self.template_dir = self.parameters.fragment_templates_dir
        else :
            self.template_dir = os.path.dirname(os.path.realpath(__file__))
            self.template_dir = os.path.dirname(self.template_dir)
            self.template_dir = os.path.join(self.template_dir, "fragment_templates")            
                
    def __load_templates_in_directory(self) :
        for file in os.listdir(self.template_dir) :
            if not file.endswith(".json") :
                continue
            
            filepath = os.path.join(self.template_dir, file)
            self.__load_template(filepath)

    def __load_template(self, filepath) :
        try :
            with open(filepath, "r") as json_file :
                template = json.load(json_file)
                
            template["filepath"] = filepath
            self.__add_template(template)
            
        except json.JSONDecodeError as decode_error :
            logging.error("Corrupt template " + filepath)
            logging.error(decode_error)
            
    def __add_template(self, template) :
        self.__add_template_by_path(template)
        self.__add_template_by_name(template)
        self.__add_template_by_group(template)
        
    def __add_template_by_path(self, template) :
        self.templates_by_path[template['filepath']] = template
        
    def __add_template_by_name(self, template) :
        name = template['name']
        msg = "Loaded template {} from file {}".format(name, template['filepath'])
        logging.info(msg)
    
        if template['name'] in self.templates.keys() :
            msg = "File '{}' replaces existing template '{}'".format(template['filepath'], name)
            logging.warning(msg)
            
        self.templates[name] = template
        if not template.get("test") :
            self.live_templates[name] = template
          
    def __add_template_by_group(self, template) :  
        group =  template.get("group")
        if group :
            lst = self.template_groups.get(group,[])
            lst.append(template)
            self.template_groups[group] = lst   
   
    def create_fragment_from_random_template(self) :
        if self.parameters.fragments :
            name = random.choice(self.parameters.fragments)
        else :
            name = random.choice(list(self.live_templates.keys()))
            
        return self.create_fragment_from_template(name) 
    
    def create_fragment_from_group(self) :
        name = random.choice(list(self.template_groups.keys()))
        template = self.template_groups[name]
        return Question(template) 
            
    def create_fragment_from_template(self, name) :
        template = self.templates.get(name)
        if not template :
            template = self.templates_by_path.get(name)
            
        if not template :
            raise MissingTemplateException(name)
            
        return Question(template)          
    