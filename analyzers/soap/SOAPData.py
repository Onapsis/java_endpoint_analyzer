class SOAPData:
    def __init__(self, filename, app_name, context_root, entrypoint, auth_methods):
        self.filename = filename
        self.app_name = app_name
        self.context_root = context_root
        if self.context_root:
            self.entrypoint = self._normalize_url(context_root,entrypoint)
        else:
            self.entrypoint = self._normalize_url(app_name,entrypoint)
        self.auth_methods = list(auth_methods)
    
    def _normalize_url(self, name, url):
        """	
            If something is X/X/Y, returns X/Y
        """		
        full_path = "{}{}".format(name, url)
        splitted_path = full_path.split('/')
        if len(splitted_path) >= 3 and splitted_path[0] == splitted_path[1]:
            return "{}/{}".format(splitted_path[0],splitted_path[2])
        else:
            return full_path

    def filename(self):
        return self.filename
    
    def app_name(self):
        return self.app_name

    def context_root(self):
        return self.context_root
        
    def entrypoint(self):
        return self.entrypoint
        
    def auth_methods(self):
        return self.auth_methods

    def is_authenticated(self):
        return "none" not in ",".join(self.auth_methods).lower()

    def __str__(self):
        output = "Name: {}\nContext Root: {}\nEntrypoint: {}\nAuth Methods:\n".format(
                                self.app_name,
                                self.context_root,
                                self.entrypoint
        )
        for auth_method in self.auth_methods:
            output += '\t- {}\n'.format(auth_method)
        
        return output + "\n"