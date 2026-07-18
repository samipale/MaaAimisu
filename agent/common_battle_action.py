import numpy as np
from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context
from maa.define import Rect


@AgentServer.custom_action("adjust_settings_action")
class AdjustSettingsAction(CustomAction):

    def run(
        self,
        context: Context,
        argv: CustomAction.RunArg,
    ) -> bool:
        attachment = self._get_attachment(context, argv.node_name)

        # 从attachment中获得参数
        skip_mode = attachment.get("skip_mode", "multiply")
        max_skip_times = attachment.get("max_skip_times", 9)

        # 点击对应模式
        if skip_mode == "skip":
            context.run_task("CommonBattle_ChooseSkipMode")
        elif skip_mode == "raid":
            pass
        elif skip_mode == "multiply":
            context.run_task("CommonBattle_ChooseMultiplyMode")
        else:
            print(f"skip_mode {skip_mode} not supported")
            return False

        # 从屏幕识别中获得基础数据
        image = context.tasker.controller.post_screencap().wait().get()
        if not self._get_base_roi(context, image):
            return False
        cached_skip_count = self._get_cached_skip_count(context, image)
        current_bp = self._get_current_bp(context, image, skip_mode)
        cached_total_bp_cost = self._get_cached_total_bp_cost(context, image, skip_mode)
        if cached_skip_count == 0 or cached_total_bp_cost == 0 or current_bp == 0:
            return False

        if skip_mode == "skip": # 如果是用扫荡券，还要检查扫荡券是否足够
            current_skip_pass = self._get_current_skip_pass(context, image)
            if current_skip_pass == 0:
                return False
            max_skip_times = min(max_skip_times, current_skip_pass)

        # 根据数据获得最大可以扫荡的次数
        bp_cost_per_battle = cached_total_bp_cost // cached_skip_count
        max_skip_by_bp = current_bp // bp_cost_per_battle
        if max_skip_by_bp == 0:
            return False

        final_max_skip_count = min(max_skip_by_bp, max_skip_times)

        # 获得需要调整的数字，然后边点击边判断是否触发上限导致变成1
        adjust_count = final_max_skip_count - cached_skip_count
        pipeline_override = self._get_adjust_template(skip_mode)
        while adjust_count != 0:
            if adjust_count > 0:
                context.run_task("CommonBattle_Increase", pipeline_override)
                if skip_mode != "raid" and self._is_one_time(context, skip_mode):
                    adjust_count = -1 # 点增加1次结果回到1次，所以需要减少1次然后直接跳出循环
                else:
                    adjust_count -= 1
            elif adjust_count < 0:
                context.run_task("CommonBattle_Reduce", pipeline_override)
                adjust_count += 1

        return True

    @staticmethod
    def _get_attachment(context: Context, node_name: str) -> dict:
        node_data = context.get_node_data(node_name)
        return node_data.get("attach", {})

    @staticmethod
    def _get_base_roi(context: Context, image: np.ndarray) -> Rect | None:
        reco_result = context.run_recognition("CommonBattle_SkipQuest_GetBasePosition", image)
        if reco_result:
            return reco_result.best_result.box
        return None

    @staticmethod
    def _get_cached_skip_count(context: Context, image: np.ndarray) -> int:
        reco_result = context.run_recognition("CommonBattle_SkipQuest_GetSkipCount", image)
        if reco_result:
            return int(reco_result.best_result.text)
        return 0

    @staticmethod
    def _get_cached_total_bp_cost(context: Context, image: np.ndarray, skip_mode: str) -> int:
        if skip_mode == "skip":
            reco_result = context.run_recognition("CommonBattle_SkipMode_GetTotalBPCost", image)
        elif skip_mode == "raid":
            reco_result = context.run_recognition("CommonBattle_RaidMode_GetTotalBPCost", image)
        else:
            reco_result = context.run_recognition("CommonBattle_MultiplyMode_GetTotalBPCost", image)
        if reco_result:
            return int(reco_result.best_result.text)
        return 0

    @staticmethod
    def _get_current_bp(context: Context, image: np.ndarray, skip_mode: str) -> int:
        if skip_mode == "skip":
            reco_result = context.run_recognition("CommonBattle_SkipMode_GetBP", image)
        elif skip_mode == "raid":
            reco_result = context.run_recognition("CommonBattle_RaidMode_GetBP", image)
        else:
            reco_result = context.run_recognition("CommonBattle_MultiplyMode_GetBP", image)
        if reco_result:
            return int(reco_result.best_result.text)
        return 0

    @staticmethod
    def _get_current_skip_pass(context: Context, image: np.ndarray) -> int:
        reco_result = context.run_recognition("CommonBattle_SkipMode_GetSkipPass", image)
        if reco_result:
            return int(reco_result.best_result.text)
        return 0

    @staticmethod
    def _is_one_time(context: Context, skip_mode: str) -> bool:
        image = context.tasker.controller.post_screencap().wait().get()
        if skip_mode == "raid":
            reco_result = context.run_recognition("CommonBattle_RaidQuest_IsOneTime", image)
        else:
            reco_result = context.run_recognition("CommonBattle_SkipQuest_IsOneTime", image)
        if reco_result.hit:
            return True
        return False

    @staticmethod
    def _get_adjust_template(skip_mode: str) -> dict:
        if skip_mode == "raid":
            increase_template = "raid/increase.png"
            reduce_template = "raid/reduce.png"
        else:
            increase_template = "quest/increase.png"
            reduce_template = "quest/reduce.png"
        pipeline_override = {
            "CommonBattle_Increase": {
                "recognition": {
                    "param": {
                        "template": increase_template
                    }
                }
            },
            "CommonBattle_Reduce": {
                "recognition": {
                    "param": {
                        "template": reduce_template
                    }
                }
            }
        }
        return pipeline_override
