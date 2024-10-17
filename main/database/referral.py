from datetime import datetime

import pymongo

import config

myclient = pymongo.MongoClient(config.db_url)
mydb = myclient[config.db_name]

mycol = mydb.referral


class Referral:
    user_id: int
    invited: int
    updated_at: int

    def __init__(self, user_id: int, invited: int, updated_at: int):
        self.user_id = user_id
        self.invited = invited
        self.updated_at = updated_at

    def get_updated_at(self) -> datetime:
        return datetime.fromtimestamp(self.updated_at)


def reset_referrals():
    mycol.update_many({}, {"$set": {"invited": 0, "updated_at": datetime.now().timestamp()}})


class ReferralDB:

    def __init__(self, user_id: int):
        self.user_id = user_id

    async def referral(self):
        # add new data if not exist by user_id
        if not await self.get_referral():
            await self.add_referral(0)
        return f"INV{self.user_id}"

    async def get_referral(self) -> Referral | None:
        data = mycol.find_one({"user_id": self.user_id})
        if data:
            return Referral(data["user_id"], data["invited"], data["updated_at"])
        else:
            return None

    async def add_referral(self, invited: int):
        data = await self.get_referral()
        try:
            if data:
                mycol.update_one({"user_id": self.user_id}, {"$set": {"invited": data.invited + invited}})
            else:
                mycol.insert_one({"user_id": self.user_id, "invited": invited, "updated_at": datetime.now().timestamp()})
            return True
        except Exception as e:
            return False


    async def update_referral(self, invited: int):
        data = await self.get_referral()
        if data:
            mycol.update_one({"user_id": self.user_id},
                             {"$set": {"invited": invited, "updated_at": datetime.now().timestamp()}})
        else:
            mycol.insert_one({"user_id": self.user_id, "invited": invited, "updated_at": datetime.now().timestamp()})

    async def reset_referral(self):
        data = await self.get_referral()
        if data:
            mycol.update_one({"user_id": self.user_id},
                             {"$set": {"invited": 0, "updated_at": datetime.now().timestamp()}})
        else:
            mycol.insert_one({"user_id": self.user_id, "invited": 0, "updated_at": datetime.now().timestamp()})
            