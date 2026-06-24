from .orei_client import OreiHttpClient
from .models import MatrixInfo, MatrixInput, MatrixOutput

class OreiApi:
    def __init__(self, client: OreiHttpClient):
        self._client = client

    async def _command(
        self,
        command: str,
        **kwargs,
    ):
        payload = {
            "comhead": command,
            "language": 0,
            **kwargs,
        }

        return await self._client.post(payload)

    async def get_system_status(self) -> MatrixInfo:
        response = await self._command("get system status")
        return MatrixInfo(response)

    async def get_input_status(self):
        return await self._command("get input status")
    
    async def get_status(self) -> MatrixInfo:
        return await self._command("get status")
    
    async def get_inputs(self) -> list[MatrixInput]:
        response = await self._command("get input status")

        inputs: list[MatrixInput] = []

        for index, name in enumerate(response["inname"], start=1):
            inputs.append(
                MatrixInput(
                    id = index,
                    name = name,
                    active=response["inactive"][index-1] == 0,
                    edid_mode = response["edid"][index-1],
                )
            )
        
        return inputs
    
    async def get_outputs(self) -> list[MatrixOutput]:
        response = await self._command("get output status")

        outputs: list[MatrixOutput] = []

        for index, name in enumerate(response["name"], start=1):
            outputs.append(
                MatrixOutput(
                    id = index,
                    name = name,
                    current_input=response["allsource"][index-1],
                    hdbt_name = response["hdbtname"][index-1],
                    scaler = response["allscaler"][index-1] == 1,
                )
            )
        
        return outputs
    
    async def set_output_source(
        self,
        output_id: int,
        input_id: int,
    ):
        print(f'Setting Output {output_id} to source {input_id}')
        await self._command("video switch", source=[input_id, output_id])
