import yaml
from process.parser import parse_steps
from utils.path_parser import resolve_path


class Pipeline:
    def __init__(self, process: list | str):
        self._process = self.__initialize_process(process)
        self.results = {}

    def run(self, data):
        res = data
        for step in self._process:
            params = []
            if step.dependancy:
                for dependancy in step.dependancy:
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
                params.append(res)
            res = step(*params)
            self.results[step.name] = res
        return res

    @property
    def process(self):
        return self._process.copy()

    @process.setter
    def process(self, process):
        if not isinstance(process, (list, str)):
            raise ValueError("Process must be a list or pipeline definition file")

        self._process = self.__initialize_process(process)

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
