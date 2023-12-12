def pipeline_step(fn):
    def step(*args, name, dependancy, **kwargs):
        fn.name = name
        fn.dependancy = dependancy
        return fn
    return step