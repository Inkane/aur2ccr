class PackageTracker(object):
    """This will track all packages.
    Future versions will have better dependency tracking"""

    def __init__(self):
        self.yet_to_install = []
        self.already_installed = set()
        self.errorneous_package = []

    def track_package(self, package):
        """tracks a package, but only if it is not converted yet."""
        if package not in self.already_installed:
            if package in self.yet_to_install:
                self.yet_to_install.remove(package)
            self.yet_to_install.append(package)
        else:
            # move package up
            pass
