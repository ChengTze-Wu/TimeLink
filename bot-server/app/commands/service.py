from .command import Command


class ServiceCommand(Command):
    async def async_execute(self):
        print("服務 0 0")