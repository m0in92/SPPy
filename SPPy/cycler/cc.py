from SPPy.cycler.base import BaseCycler


class CC(BaseCycler):
    # class variables
    cycle_steps = ["rest", "charge", "rest", "discharge"]

    def __init__(self, num_cycles: int,
                 charge_current: float, discharge_current: float, rest_time: float,
                 V_max: float, V_min: float):
        super().__init__()
        self.num_cycles = num_cycles
        self.charge_current = charge_current
        self.discharge_current = -discharge_current
        self.rest_time = rest_time
        self.V_max = V_max
        self.V_min = V_min

    def get_current(self, step_name: str, t: float = 0.0) -> float:
        if step_name == "rest":
            return 0.0
        elif step_name == "charge":
            return self.charge_current
        elif step_name == "discharge":
            return self.discharge_current
        else:
            raise TypeError("Not a valid step name")

    def reset(self) -> None:
        self.time_elapsed = 0.0
        self.SOC_LIB = self.SOC_LIB_init


class CCNoFirstRest(BaseCycler):
    # class variables
    cycle_steps = ["charge", "rest", "discharge", "rest"]

    def __init__(self, num_cycles, charge_current, discharge_current, rest_time, V_max, V_min, SOC_min=0, SOC_max=1,
                 SOC_LIB=0):
        super().__init__()
        self.num_cycles = num_cycles
        self.charge_current = charge_current
        self.discharge_current = -discharge_current
        self.rest_time = rest_time
        self.V_max = V_max
        self.V_min = V_min
        self.SOC_min = SOC_min
        self.SOC_max = SOC_max
        self.SOC_LIB = SOC_LIB

    def get_current(self, step_name: str, t: float = 0.0) -> float:
        if step_name == "rest":
            return 0.0
        elif step_name == "charge":
            return self.charge_current
        elif step_name == "discharge":
            return self.discharge_current
        else:
            raise TypeError("Not a valid step name")

    def reset(self) -> None:
        self.time_elapsed = 0.0
        self.SOC_LIB = self.SOC_LIB_init


class CCCV(BaseCycler):
    # class variables
    cycle_steps = ["charge", "CV", "rest", "discharge", "rest"]

    def __init__(self, num_cycles, charge_current, discharge_current, rest_time, V_max, V_min, SOC_min=0, SOC_max=1,
                 SOC_LIB=0):
        super().__init__()
        self.num_cycles = num_cycles
        self.charge_current = charge_current
        self.discharge_current = -discharge_current
        self.rest_time = rest_time
        self.V_max = V_max
        self.V_min = V_min
        self.SOC_min = SOC_min
        self.SOC_max = SOC_max
        self.SOC_LIB = SOC_LIB

    def get_current(self, step_name: str, t: float = 0.0) -> float:
        if step_name == "rest":
            return 0.0
        elif step_name == "charge":
            return self.charge_current
        elif step_name == "discharge":
            return self.discharge_current
        else:
            raise TypeError("Not a valid step name")

    def reset(self) -> None:
        self.time_elapsed = 0.0
        self.SOC_LIB = self.SOC_LIB_init


class DischargeRestCharge(BaseCycler):
    def __init__(self, discharge_current: float, rest_time: float, charge_current: float,
                 V_max: float, V_min: float,
                 SOC_LIB: float=1, SOC_LIB_min=0, SOC_LIB_max=1):
        super().__init__(SOC_LIB=SOC_LIB, SOC_LIB_min=SOC_LIB_min, SOC_LIB_max=SOC_LIB_max)
        self.discharge_current = -discharge_current
        self.charge_current = charge_current
        self.V_max = V_max
        self.V_min = V_min
        self.SOC_LIB_init = SOC_LIB
        self.rest_time = rest_time
        self.cycle_steps = ['discharge', 'rest', 'charge']
        self.num_cycles = 1

    def get_current(self, step_name: str, t: float = 0.0) -> float:
        if step_name == "rest":
            return 0.0
        elif step_name == "charge":
            return self.charge_current
        elif step_name == "discharge":
            return self.discharge_current
        else:
            raise TypeError("Not a valid step name")

    def reset(self) -> None:
        self.time_elapsed = 0.0
        self.SOC_LIB = self.SOC_LIB_init


class DischargeRestChargeRest(BaseCycler):
    def __init__(self, num_cycles: float, discharge_current: float, rest_time: float, charge_current: float,
                 V_max: float, V_min: float,
                 SOC_LIB: float=1, SOC_LIB_min=0, SOC_LIB_max=1):
        super().__init__(SOC_LIB=SOC_LIB, SOC_LIB_min=SOC_LIB_min, SOC_LIB_max=SOC_LIB_max, num_cycles=num_cycles)
        self.discharge_current = -discharge_current
        self.charge_current = charge_current
        self.V_max = V_max
        self.V_min = V_min
        self.SOC_LIB_init = SOC_LIB
        self.rest_time = rest_time
        self.cycle_steps = ['discharge', 'rest', 'charge', 'rest']
        self.num_cycles = 1

    def get_current(self, step_name: str, t: float = 0.0) -> float:
        if step_name == "rest":
            return 0.0
        elif step_name == "charge":
            return self.charge_current
        elif step_name == "discharge":
            return self.discharge_current
        else:
            raise TypeError("Not a valid step name")

    def reset(self) -> None:
        self.time_elapsed = 0.0
        self.SOC_LIB = self.SOC_LIB_init