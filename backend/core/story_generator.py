# from sqlalchemy.orm import Session
# from core.config import settings

# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import PydanticOutputParser

# from core.prompts import STORY_PROMPT
# from models.story import Story, StoryNode
# from core.models import StoryLLMResponse, StoryNodeLLM
# from dotenv import load_dotenv
# import os

# load_dotenv()

# class StoryGenerator:

#     # @classmethod
#     # def _get_llm(cls):
#     #     openai_api_key = os.getenv("CHOREO_OPENAI_CONNECTION_OPENAI_API_KEY")
#     #     serviceurl = os.getenv("CHOREO_OPENAI_CONNECTION_SERVICEURL")

#     #     if openai_api_key and serviceurl:
#     #         return ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key, base_url=serviceurl)

#     #     return ChatOpenAI(model="gpt-4o-mini")

#     @classmethod
#     def _get_llm(cls):
#         if not settings.USE_OPENAI:
#             return None  # 👈 MOCK MODE

#         if not settings.OPENAI_API_KEY:
#             raise RuntimeError("OPENAI_API_KEY not set")

#         return ChatOpenAI(
#             model="gpt-4o-mini",
#             api_key=settings.OPENAI_API_KEY
#         )

#     def generate_mock_story(theme: str):
#         return {
#             "title": f"Mock Adventure: {theme}",
#             "description": (
#                 f"This is a mock story for '{theme}'. "
#                 "OpenAI usage is disabled."
#             ),
#             "nodes": [
#                 {
#                     "id": "start",
#                     "content": f"You enter a {theme}. The adventure begins!",
#                     "choices": [
#                         {"text": "Go left", "next_node": "left"},
#                         {"text": "Go right", "next_node": "right"}
#                     ]
#                 }
#             ]
#         }

#     @classmethod
#     def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy")-> Story:
#         llm = cls._get_llm()
#         story_parser = PydanticOutputParser(pydantic_object=StoryLLMResponse)

#         prompt = ChatPromptTemplate.from_messages([
#             (
#                 "system",
#                 STORY_PROMPT
#             ),
#             (
#                 "human",
#                 f"Create the story with this theme: {theme}"
#             )
#         ]).partial(format_instructions=story_parser.get_format_instructions())

#         raw_response = llm.invoke(prompt.invoke({}))

#         response_text = raw_response
#         if hasattr(raw_response, "content"):
#             response_text = raw_response.content

#         story_structure = story_parser.parse(response_text)

#         story_db = Story(title=story_structure.title, session_id=session_id)
#         db.add(story_db)
#         db.flush()

#         root_node_data = story_structure.rootNode
#         if isinstance(root_node_data, dict):
#             root_node_data = StoryNodeLLM.model_validate(root_node_data)

#         cls._process_story_node(db, story_db.id, root_node_data, is_root=True)

#         db.commit()
#         return story_db

#     @classmethod
#     def _process_story_node(cls, db: Session, story_id: int, node_data: StoryNodeLLM, is_root: bool = False) -> StoryNode:
#         node = StoryNode(
#             story_id=story_id,
#             content=node_data.content if hasattr(node_data, "content") else node_data["content"],
#             is_root=is_root,
#             is_ending=node_data.isEnding if hasattr(node_data, "isEnding") else node_data["isEnding"],
#             is_winning_ending=node_data.isWinningEnding if hasattr(node_data, "isWinningEnding") else node_data["isWinningEnding"],
#             options=[]
#         )
#         db.add(node)
#         db.flush()

#         if not node.is_ending and (hasattr(node_data, "options") and node_data.options):
#             options_list = []
#             for option_data in node_data.options:
#                 next_node = option_data.nextNode

#                 if isinstance(next_node, dict):
#                     next_node = StoryNodeLLM.model_validate(next_node)

#                 child_node = cls._process_story_node(db, story_id, next_node, False)

#                 options_list.append({
#                     "text": option_data.text,
#                     "node_id": child_node.id
#                 })

#             node.options = options_list

#         db.flush()
#         return node
    

from sqlalchemy.orm import Session
from core.config import settings

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.prompts import STORY_PROMPT
from models.story import Story, StoryNode
from core.models import StoryLLMResponse, StoryNodeLLM

from dotenv import load_dotenv
import os

load_dotenv()


class StoryGenerator:

    # =========================
    # LLM LOADER (FEATURE-FLAG)
    # =========================
    @classmethod
    def _get_llm(cls):
        if not settings.USE_OPENAI:
            return None  # MOCK MODE

        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY not set")

        return ChatOpenAI(
            model="gpt-4o-mini",
            api_key=settings.OPENAI_API_KEY
        )

    # =========================
    # MOCK STORY (NO OPENAI)
    # =========================
    # @staticmethod
    # def _generate_mock_story(theme: str) -> StoryLLMResponse:
    #     return StoryLLMResponse(
    #         title=f"Mock Adventure: {theme}",
    #         rootNode=StoryNodeLLM(
    #             content=f"You enter a {theme}. The adventure begins!",
    #             isEnding=False,
    #             isWinningEnding=False,
    #             options=[]
    #         )
    #     )
    @staticmethod
    def _generate_mock_story(theme: str) -> StoryLLMResponse:
        return StoryLLMResponse(
            title=f"Mock Adventure: {theme}",
            rootNode=StoryNodeLLM(
                content=f"You enter a {theme}. The adventure begins!",
                isEnding=False,
                isWinningEnding=False,
                options=[
                    {
                        "text": "Explore the area",
                        "nextNode": {
                            "content": f"You explore deeper into the {theme}.",
                            "isEnding": False,
                            "isWinningEnding": False,
                            "options": [
                                {
                                    "text": "Continue forward",
                                    "nextNode": {
                                        "content": "You discover a hidden path and win!",
                                        "isEnding": True,
                                        "isWinningEnding": True,
                                        "options": []
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "text": "Leave the area",
                        "nextNode": {
                            "content": "You decide to leave. The adventure ends.",
                            "isEnding": True,
                            "isWinningEnding": False,
                            "options": []
                        }
                    }
                ]
            )
        )


    # =========================
    # MAIN STORY GENERATOR
    # =========================
    @classmethod
    def generate_story(
        cls,
        db: Session,
        session_id: str,
        theme: str = "fantasy"
    ) -> Story:

        # ---------- MOCK MODE ----------
        if not settings.USE_OPENAI:
            story_structure = cls._generate_mock_story(theme)

        # ---------- REAL OPENAI MODE ----------
        else:
            llm = cls._get_llm()

            story_parser = PydanticOutputParser(
                pydantic_object=StoryLLMResponse
            )

            prompt = ChatPromptTemplate.from_messages([
                ("system", STORY_PROMPT),
                ("human", f"Create the story with this theme: {theme}")
            ]).partial(
                format_instructions=story_parser.get_format_instructions()
            )

            raw_response = llm.invoke(prompt.invoke({}))

            response_text = (
                raw_response.content
                if hasattr(raw_response, "content")
                else raw_response
            )

            story_structure = story_parser.parse(response_text)

        # =========================
        # SAVE STORY TO DATABASE
        # =========================
        story_db = Story(
            title=story_structure.title,
            session_id=session_id
        )
        db.add(story_db)
        db.flush()

        root_node_data = story_structure.rootNode
        if isinstance(root_node_data, dict):
            root_node_data = StoryNodeLLM.model_validate(root_node_data)

        cls._process_story_node(
            db=db,
            story_id=story_db.id,
            node_data=root_node_data,
            is_root=True
        )

        db.commit()
        return story_db

    # =========================
    # RECURSIVE NODE PROCESSOR
    # =========================
    @classmethod
    def _process_story_node(
        cls,
        db: Session,
        story_id: int,
        node_data: StoryNodeLLM,
        is_root: bool = False
    ) -> StoryNode:

        node = StoryNode(
            story_id=story_id,
            content=node_data.content,
            is_root=is_root,
            is_ending=node_data.isEnding,
            is_winning_ending=node_data.isWinningEnding,
            options=[]
        )
        db.add(node)
        db.flush()

        if not node.is_ending and node_data.options:
            options_list = []

            for option_data in node_data.options:
                next_node = option_data.nextNode

                if isinstance(next_node, dict):
                    next_node = StoryNodeLLM.model_validate(next_node)

                child_node = cls._process_story_node(
                    db=db,
                    story_id=story_id,
                    node_data=next_node,
                    is_root=False
                )

                options_list.append({
                    "text": option_data.text,
                    "node_id": child_node.id
                })

            node.options = options_list

        db.flush()
        return node
