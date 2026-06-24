from dataclasses import dataclass

@dataclass
class MatrixInput:
    id: int
    name: str
    active: bool
    edid_mode: int

@dataclass
class MatrixOutput:
    id: int
    name: str
    current_input: int
    hdbt_name: str
    scaler: bool

@dataclass
class MatrixInfo:
    model: str
    firmware: str
    inputs: int
    outputs: int

@dataclass
class MatrixState:
    inputs: list[MatrixInput]
    outputs: list[MatrixOutput]