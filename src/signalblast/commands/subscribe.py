from signalbot import Command
from signalbot import Context as ChatContext

from signalblast.broadcastbot import BroadcasBot
from signalblast.commands_strings import CommandRegex
from signalblast.utils import triggered


class Subscribe(Command):
    def __init__(self, bot: BroadcasBot) -> None:
        super().__init__()
        self.broadcastbot = bot

    async def subscribe(self, ctx: ChatContext, verbose: bool = False) -> None:
        try:
            subscriber_uuid = ctx.message.source_uuid
            if subscriber_uuid in self.broadcastbot.subscribers:
                if verbose:
                    await self.broadcastbot.reply_with_warn_on_failure(ctx, "Already subscribed!")
                    self.broadcastbot.logger.info("Already subscribed!")
                return

            if subscriber_uuid in self.broadcastbot.banned_users:
                if verbose:
                    await self.broadcastbot.reply_with_warn_on_failure(ctx, "This number is not allowed to subscribe")
                    self.broadcastbot.logger.info(f"{subscriber_uuid} was not allowed to subscribe")
                return

            await self.broadcastbot.subscribers.add(subscriber_uuid, ctx.message.source_number)
            await self.broadcastbot.reply_with_warn_on_failure(ctx, self.broadcastbot.welcome_message)
            # if self.broadcastbot.expiration_time is not None:
            #     await ctx.bot.set_expiration(subscriber_uuid, self.broadcastbot.expiration_time)
            self.broadcastbot.logger.info(f"{subscriber_uuid} subscribed")
        except Exception as e:
            self.broadcastbot.logger.error(e, exc_info=True)
            try:
                await self.broadcastbot.reply_with_warn_on_failure(ctx, "Could not subscribe!")
            except Exception as e:
                self.broadcastbot.logger.error(e, exc_info=True)

    @triggered(CommandRegex.subscribe)
    async def handle(self, ctx: ChatContext) -> None:
        await Subscribe.subscribe(self, ctx, verbose=True)
