from astrbot.api.all import Star, logger, Plain, At, AstrMessageEvent, filter


class 补回艾特自身(Star):

    def __init__(self, context):
        super().__init__(context)
        self.context = context

    @filter.on_waiting_llm_request()
    async def llm队列时(self, event: AstrMessageEvent, *_, **__):
        """进入llm请求队列时执行"""

        ystr = event.message_str
        mstr = event.message_str
        mxxl = event.get_messages()
        mid = event.get_self_id()

        ctp = []
        atp = []

        for i in mxxl:
            if isinstance(i, Plain):
                ctp.append(i.text)
                atp.append(i.text)

            elif isinstance(i, At):
                if str(i.qq) == mid:
                    atp.append(f" @{i.name}(myself) ")
                else:
                    ctp.append(f" @{i.name}({i.qq}) ")
                    atp.append(f" @{i.name}({i.qq}) ")

            # 其他类型跟随框架，忽略

        ctx = ''.join(ctp).strip()
        atx = ''.join(atp).strip()

        if ctx == atx:
            logger.debug(f"无艾特自身，跳过")
            return

        ctx, atx = next(
            (
                (ctx.removeprefix(p), atx.removeprefix(p))
                for p in self.context.get_config(umo=event.unified_msg_origin).get("wake_prefix", [])
                if ctx.startswith(p)
            ),
            (ctx, atx)
        )

        if ctx not in mstr:
            logger.info(f"重组后文本：|{ctx}|")
            logger.info(f"框架原文本：|{mstr}|")
            logger.warning("没有定位到，不做修改")
            return

        mstr = mstr.replace(ctx, atx, 1)

        event.message_str = mstr
        event.message_obj.message_str = mstr

        logger.debug(f"消息链：|{mxxl}|")
        logger.debug(f"原文本：|{ystr}|")
        logger.debug(f"概要喵：|{event.get_message_outline()}|")
        logger.debug(f"补全后：|{mstr}|")
        logger.info(f"已补全艾特自身信息：|{mstr}|")