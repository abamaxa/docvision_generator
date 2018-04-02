import json
import os
import logging
import random

from question_templates import Question

class ConstructedQuestionFactory :
    def __init__(self) :
        self.templates = {}
        self.live_templates = {}
        self.template_dir = os.path.dirname(os.path.realpath(__file__))
        self.template_dir = os.path.dirname(self.template_dir)
        self.template_dir = os.path.join(self.template_dir, "templates")
        self.load_templates()
        
    def load_templates(self) :
        for file in os.listdir(self.template_dir) :
            if not file.endswith(".json") :
                continue
            
            self.load_template(file)

    def load_template(self, file) :
        try :
            with open(os.path.join(self.template_dir,file), "r") as json_file :
                template = json.load(json_file)
                
            name = template['name']
            msg = "Loaded template {} from file {}".format(name, file)
            logging.info(msg)
        
            if template['name'] in self.templates.keys() :
                msg = "File '{}' replaces existing template '{}'".format(file, name)
                logging.warn(msg)
                
            self.templates[name] = template
            if not template.get("test") :
                self.live_templates[name] = template
            
        except json.JSONDecodeError as decode_error :
            logging.error("Corrupt template " + file)
            logging.error(decode_error)
            
    def create_question_from_random_template(self) :
        template = self.live_templates[random.choice(list(self.live_templates.keys()))]
        return Question(template) 
            
    def create_question_from_template(self, name) :
        template = self.templates[name]
        return Question(template)                


    
    