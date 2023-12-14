from process import steps


def parse_steps(step_definitions: list[dict]):
    step_list = []
    for step_definition in step_definitions:
        try:
            step = getattr(steps, step_definition["run"])
        except KeyError:
            raise RuntimeError("Step definition file missing run attribute")
        except AttributeError:
            raise RuntimeError("Step does not exists")

        parameter = step_definition.get("parameters", [])
        step_list.append(
            step(
                *parameter,
                name=step_definition["name"],
                dependancy=step_definition.get("dependancy", []),
            )
        )

    return step_list
