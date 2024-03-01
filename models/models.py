from pydantic import BaseModel, Field


class HumanMessageModel(BaseModel):
    human_msg: str | None


class AIMessageModel(BaseModel):
    ai_msg: str | None = Field(description="Response of the AI assistant")
    url: str | None = Field(None)
