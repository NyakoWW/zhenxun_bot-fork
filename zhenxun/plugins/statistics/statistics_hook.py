from datetime import datetime

from nonebot.adapters import Bot
from nonebot.matcher import Matcher
from nonebot.message import run_postprocessor
from nonebot.plugin import PluginMetadata
from nonebot_plugin_session import EventSession

from zhenxun.configs.utils import PluginExtraData
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.models.statistics import Statistics
from zhenxun.utils.enum import PluginType

__plugin_meta__ = PluginMetadata(
    name="功能调用统计",
    description="功能调用统计",
    usage="""""".strip(),
    extra=PluginExtraData(
        author="HibiKier", version="0.1", plugin_type=PluginType.HIDDEN
    ).dict(),
)


@run_postprocessor
async def _(
    matcher: Matcher, exception: Exception | None, bot: Bot, session: EventSession
):
    plugin = await PluginInfo.get_or_none(module=matcher.plugin_name)
    plugin_type = plugin.plugin_type if plugin else None
    if (
        plugin_type == PluginType.NORMAL
        and matcher.priority not in [1, 999]
        and matcher.plugin_name not in ["update_info", "statistics_handle"]
    ):
        await Statistics.create(
            user_id=session.id1,
            group_id=session.id3 or session.id2,
            plugin_name=matcher.plugin_name,
            create_time=datetime.now(),
        )