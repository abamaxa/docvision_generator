from .base_cloud_provider import AbstractCloudProvider

class GoogleCloud(AbstractCloudProvider) :
    def __init__(self, options) :
        self.compute = options.get("compute")
    
    def list_instances(compute, project, zone):
        result = compute.instances().list(project=project, zone=zone).execute()
        return result['items']    
    
if __name__ == "__main__" :
    options = {"compute" : 1}
    cloud = GoogleCloud(options)