class WDData:
    def __init__(self, filename, app_name, entrypoints):
        self.app_name = app_name    
        self.filename = filename
        self.entrypoints = list(entrypoints)
    
    def filename(self):
        return self.filename
    
    def app_name(self):
        return self.app_name

    def entrypoints(self):
        return self.entrypoints
    
    def __str__(self):
        output = "App name: {}\nFilename: {}\nEntrypoints:\n".format(
                                self.app_name,
                                self.filename
        )
        for entrypoint in self.entrypoints:
            output += '\t- {}\n'.format(entrypoint)
        
        return output + "\n"