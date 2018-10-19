import cProfile
from auklet.stats import AukletProfilerStats, Function


class AukletViewProfiler(object):
    profiler = None

    def process_view(self, request, view_func, view_args, view_kwargs):
        self.profiler = cProfile.Profile()
        args = (request,) + view_args
        return self.profiler.runcall(view_func, *args, **view_kwargs)

    def add_func(self, func, cumulative=0.1):
        for subfunc in func.subfuncs():
            if subfunc.stats[3] >= cumulative:
                func.callees.append(subfunc)
                self.add_func(subfunc, cumulative)

    def create_stack(self, request, response):
        if not hasattr(self, 'profiler'):
            return None
        # Could be delayed until the panel content is requested (perf. optim.)
        self.profiler.create_stats()
        self.stats = AukletProfilerStats(self.profiler)
        self.stats.calc_callees()

        root_func = self.stats.get_root_func()
        # Ensure root function exists before continuing with function call analysis
        if root_func:
            root = Function(self.stats, root_func, depth=0)
            self.add_func(root,
                          root.stats[3] / 8)
            return root
