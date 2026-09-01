import numpy as np
from maa.agent.agent_server import AgentServer
from maa.custom_recognition import CustomRecognition
from maa.context import Context
from maa.define import Rect



@AgentServer.custom_recognition("event_difficulty_recognition")
class EventDifficultyRecognition(CustomRecognition):

    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        """寻找符合条件的活动关卡"""
        # 从attachment中获得参数
        attachment = self._get_attachment(context, argv.node_name)
        quest_type = attachment.get("quest_type", "")
        quest_cleared = attachment.get("quest_cleared", None)
        quest_name = attachment.get("quest_name", "")
        if quest_type not in ("story", "challenge", "bonus"):
            print(f"quest_type {quest_type} is not valid")
            return CustomRecognition.AnalyzeResult(box=None, detail={})

        if isinstance(quest_type, str):
            quest_type = [quest_type]

        # 从关卡类型获得基础ROI
        base_rois = self._get_quest_base_rois(context, argv.image, quest_type)
        if not base_rois:
            print("base_rois is empty")
            return CustomRecognition.AnalyzeResult(box=None, detail={})
        quest_rois = {
            i: {
                "base_roi": base_rois[i],
                "quest_roi": self._get_quest_roi(base_rois[i]),
                "quest_name_roi": self._get_quest_name_roi(base_rois[i]),
            }
            for i in range(len(base_rois))
        }

        # 对是否通关进行筛选
        quest_rois = self._filter_quest_rois_by_clear_status(context, argv.image, quest_rois, quest_cleared)

        # 对关卡名字进行筛选
        quest_rois = self._filter_quest_rois_by_name(context, argv.image, quest_rois, quest_name)

        if not quest_rois:
            print("quest_rois is empty")
            return CustomRecognition.AnalyzeResult(box=None, detail={})

        first_key = next(iter(quest_rois))
        return CustomRecognition.AnalyzeResult(
            box=quest_rois[first_key]["quest_name_roi"], detail={}
        )

    @staticmethod
    def _get_attachment(context: Context, node_name: str) -> dict:
        node_data = context.get_node_data(node_name)
        return node_data.get("attach", {})

    @staticmethod
    def _get_quest_base_rois(context: Context, image: np.ndarray, quest_type: list[str]) -> list[Rect] | None:
        template = []
        if "story" in quest_type:
            template.append("quest/event/story_quest.png")
        if "challenge" in quest_type:
            template.append("quest/event/challenge_quest.png")
        if "bonus" in quest_type:
            template.append("quest/event/bonus_quest.png")
        if not template:
            print("quest_type is empty")
            return None

        node_name = "__CommonEvent_EventDifficultyRecognition_QuestBaseROI"
        pipeline_override = {node_name: {"recognition": {"param": {"template": template}}}}
        reco_result = context.run_recognition(node_name, image, pipeline_override)
        if reco_result and reco_result.hit:
            return [r.box for r in reco_result.filtered_results]
        return None

    @staticmethod
    def _filter_quest_rois_by_clear_status(
            context: Context, image: np.ndarray, quest_rois: dict, quest_cleared: bool | None
    ) -> dict:
        if quest_cleared is None:
            return quest_rois
        node_name = "__CommonEvent_EventDifficultyRecognition_ClearedQuest"
        result_rois = {}
        for i in quest_rois:
            quest_roi = quest_rois[i]["quest_roi"]
            pipeline_override = {node_name: {"recognition": {"param": {"roi": quest_roi}}}}
            reco_result = context.run_recognition(node_name, image, pipeline_override)
            if reco_result and (reco_result.hit == quest_cleared):
                result_rois[i] = quest_rois[i]
        return result_rois

    @staticmethod
    def _filter_quest_rois_by_name(
            context: Context, image: np.ndarray, quest_rois: dict, quest_name: str | None
    ) -> dict:
        if not quest_name:
            return quest_rois
        node_name = "__CommonEvent_EventDifficultyRecognition_QuestName"
        result_rois = {}
        for i in quest_rois:
            quest_name_roi = quest_rois[i]["quest_name_roi"]
            pipeline_override = {node_name: {"recognition": {"param": {
                "roi": quest_name_roi,
                "expected": quest_name,
            }}}}
            reco_result = context.run_recognition(node_name, image, pipeline_override)
            if reco_result and reco_result.hit:
                result_rois[i] = quest_rois[i]
        return result_rois

    @staticmethod
    def _get_quest_roi(roi: Rect | list[int]) -> list[int]:
        offset = [-309, -29, 317, 54]
        return [r + o for r, o in zip(roi, offset)]

    @staticmethod
    def _get_quest_name_roi(roi: Rect | list[int]) -> list[int]:
        offset = [-309, 0, 250, 0]
        return [r + o for r, o in zip(roi, offset)]
