import numpy as np
import re
from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context
from maa.define import Rect


@AgentServer.custom_action("choose_party_action")
class ChoosePartyAction(CustomAction):

    def run(
        self,
        context: Context,
        argv: CustomAction.RunArg,
    ) -> bool:
        attachment = self._get_attachment(context, argv.node_name)

        # 从attachment中获得参数
        party_name = attachment.get("party_name", "")
        party_name = re.sub(r"\W|ー|一", "", party_name) if isinstance(party_name, str) else ""
        if not party_name:
            print("party_name is empty")
            return False

        # 从屏幕识别中获得基础数据
        image = context.tasker.controller.post_screencap().wait().get()
        if not self._get_base_roi(context, image):
            print("get_base_roi failed")
            return False

        # 开始识别队伍
        recognize_party_names = []
        for _ in range(60):
            recognize_party_name = self._recognize_party_name(context, image)
            if party_name == recognize_party_name:
                return True
            elif recognize_party_name and recognize_party_name in recognize_party_names:
                print("party_name not found")
                return False
            else:
                recognize_party_names.append(recognize_party_name)
                context.run_task("ChooseParty_Next")
                image = context.tasker.controller.post_screencap().wait().get()

        print(f"party_name {party_name} not found after 60 times")
        return False

    @staticmethod
    def _get_attachment(context: Context, node_name: str) -> dict:
        node_data = context.get_node_data(node_name)
        return node_data.get("attach", {})

    @staticmethod
    def _get_base_roi(context: Context, image: np.ndarray) -> Rect | None:
        reco_result = context.run_recognition("ChooseParty_Base", image)
        if reco_result:
            return reco_result.best_result.box
        return None

    @staticmethod
    def _recognize_party_name(context: Context, image: np.ndarray) -> str | None:
        reco_result = context.run_recognition("ChooseParty_RecognizePartyName", image)
        if reco_result:
            return reco_result.best_result.text
        return None
