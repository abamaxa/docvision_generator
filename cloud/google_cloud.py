from pprint import pprint
import time
import logging

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

from cloud.base_cloud_provider import AbstractCloudProvider

class GoogleCloud(AbstractCloudProvider) :
    def __init__(self, options) :
        self.zone = options.get("zone")
        self.project = options.get("project")
        self.name = options.get("instance")
        self.service = None
        
        self.__connect()
                
    def __connect(self) :
        credentials = GoogleCredentials.get_application_default()  
        self.service = discovery.build('compute', 'v1', credentials=credentials)         

    def __instance_request(self, name, kwargs = {}) :
        foo = getattr(self.service.instances(), name)
        return foo(project=self.project, zone=self.zone, **kwargs)
    
    def list_instances(self):
        request = self.service.instances().list(project=self.project, zone=self.zone)
        while request is not None:
            response = request.execute()
        
            for instance in response['items']:
                # TODO: Change code below to process each `accelerator_type` resource:
                pprint(instance.get("name"))
        
            request = self.service.instances().list_next(previous_request=request, previous_response=response) 
    
    def start_instance(self) :
        logging.warn("Starting Google compute instance %s for project %s in zone %s", self.name,
                     self.project, self.zone)
        request = self.__instance_request("start", {"instance" : self.name})
        response = request.execute()     
        status = response.get("status") 
        logging.warn("Start request for instance %s has status %s", self.name, status)        
        return status
    
    def wait_until_running(self, max_wait_seconds = 30) :
        seconds = 0
        status, ip_list = self.get_instance_ip()
        
        while seconds < max_wait_seconds and status != "RUNNING" :
            seconds += 1
            time.sleep(1)
            status, ip_list = self.get_instance_ip()
            logging.warn("Instance %s has status: %s ips: %s", self.name, status, ip_list)
            
        return status, ip_list
    
    def get_instance_ip(self) :
        request = self.__instance_request("get", {"instance" : self.name})
        response = request.execute()   
        status = response.get("status") 
        return status, self.__find_ips_in_response(response)
    
    def __find_ips_in_response(self, response) :
        ip_list = []
        for item in response.get("networkInterfaces", []) :
            for config in item.get("accessConfigs", []) :
                ip = config.get("natIP")
                if not ip :
                    continue
                
                ip_list.append(ip)
                
        return ip_list    

    def stop_instance(self) :
        logging.warn("Stopping Google compute instance %s for project %s in zone %s", self.name,
                     self.project, self.zone)        
        request = self.__instance_request("stop", {"instance" : self.name})
        response = request.execute()  
        status = response.get("status") 
        logging.warn("Stop request for instance %s has status %s", self.name, status)        
        return status
        
if __name__ == "__main__" :	
    options = {
        "zone" : "europe-west2-b", 
        "project" : "docvision-200508", 
        "instance" : "docvision-data-2-0-4b-london" }
    
    options_light = {
        "zone" : "europe-west4-b", 
        "project" : "docvision-200508", 
        "instance" : "docvision-data" }    
    
    cloud = GoogleCloud(options_light)
    print(cloud.list_instances())
    print(cloud.start_instance())
    print(cloud.wait_until_running())
    print(cloud.stop_instance())
