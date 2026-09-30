from pydantic import BaseModel, Field

class SessionCreate(BaseModel):
    title: str = Field(..., min_length=3)
    trainer: str = Field(..., min_length=2)
    food_menu: str = Field(..., min_length=2)
    participants_count: int = Field(..., gt=0)
    date: str

class SessionResponse(SessionCreate):
    id: int