from pydantic import BaseModel


class UserSubscriptionsBase(BaseModel):
    user_id: str
    plan_id: int
    status: str


class CreateUserSubscriptionsSchema(UserSubscriptionsBase):
    pass


class ResponseUserSubscriptions(UserSubscriptionsBase):
    start_date: str
    end_date: str
    auto_renewal: bool


class UpdateUserSubscriptionsSchema(UserSubscriptionsBase):
    start_date: str
    end_date: str
    auto_renewal: bool
