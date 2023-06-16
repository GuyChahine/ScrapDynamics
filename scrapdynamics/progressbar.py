from rich.progress import (
    Progress,
    BarColumn,
    MofNCompleteColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)


class ProgressBar(Progress):
    """Wrapper of Rich ProgressBar
    """        
    
    def __init__(self):
        
        super(ProgressBar, self).__init__(
            TextColumn("[progress.description]{task.description}"),
            MofNCompleteColumn(),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("•"),
            TimeRemainingColumn(),
        )
        
        self.progress = self.__enter__()
        
        # Set progress bars to 0 for the moment
        self.depth_task = self.progress.add_task("Depth", total=0)
        self.url_task = self.progress.add_task("Url", total=0)
        
    def update_task(self, depth_total: int = 0, url_total: int = 0):
        """Change the maximum of depth or total url

        Args:
            depth_total (int, optional): total depth. Defaults to 0.
            url_total (int, optional): total url. Defaults to 0.
        """
        
        if depth_total: self.progress.update(self.depth_task, total=depth_total)
        if url_total: self.progress.update(self.url_task, total=url_total)
        self.progress.refresh()
        
    def make_advance(self, depth: bool, url: bool):
        """Advance of 1 the progress bars

        Args:
            depth (bool): if True advance of 1 the depth bar
            url (bool): if True advance of 1 the url bar
        """
        
        if depth: self.progress.advance(self.depth_task)
        if url: self.progress.advance(self.url_task)
        self.progress.refresh()
        
    def make_reset(self, depth: bool, url: bool):
        """Reset the 0 the progress bars

        Args:
            depth (bool): if True reset depth bar
            url (bool): if True reset url bar
        """
        
        if depth: self.progress.reset(self.depth_task)
        if url: self.progress.reset(self.url_task)
        self.progress.refresh()
        
    def close(self):
        self.__exit__(None, None, None)