from pydantic import BaseModel


class HumanMessageModel(BaseModel):
    human_msg: str | None


class AIMessageModel(BaseModel):
    ai_msg: str | None
