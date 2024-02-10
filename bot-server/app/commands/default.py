from .command import Command


class DefaultCommand(Command):
    async def async_execute(self):
        pass