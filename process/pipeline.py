import yaml
from utils.path_parser import resolve_path
from process.steps import parse_steps


class Pipeline:
    def __init__(self, process: list | str):
        self.__process = self.__initialize_process(process)
        self.results = {}

    def run(self, data):
        res = data
        for process in self.__process:
            if process.dependancy:
                params = []
                for dependancy in process.dependancy:
                    try:
                        if isinstance(self.results[dependancy], (list, tuple)):
                            params.extend(self.results[dependancy])
                        else:
                            params.append(self.results[dependancy])
                    except KeyError:
                        raise RuntimeError(
                            "Dependancy must be from previously executed process"
                        )
            else:
                params = res
            res = process(*params)
            self.results[process.name] = res
        return res[0]

    @property
    def process(self):
        return self.__process.copy()

    @process.setter
    def set_process(self, new_process):
        if not isinstance(new_process, (list, str)):
            raise ValueError("Process must be a list or pipeline definition file")

        self.__process = self.__initialize_process(new_process)

    def __initialize_process(self, process):
        if isinstance(process, str):
            process_definitions = None
            try:
                source_file = resolve_path(f"process/config/{process}.yaml")
                with open(source_file, "r") as f:
                    process_definitions = yaml.safe_load(f)
            except OSError:
                raise FileNotFoundError("Config file not count")

            return parse_steps(process_definitions)

        elif isinstance(process, list):
            return process
        else:
            raise ValueError("Process must be a list or pipeline definition file")
