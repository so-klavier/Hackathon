import json
from pathlib import Path

#jsonへのアクセスを行うための関数を定義するファイル
# ユーザーごとにclassのインスタンスを生成 -> 全てのユーザーのインスタンスをuidをキーとする辞書型に保存

USER_DATA_PATH = Path(__file__).resolve().parents[3] / "backend" / "data" / "users"

class Relationship_Manager:
    def load_user_data(self, user_id: str)-> dict:
        file_path = USER_DATA_PATH / f"{user_id}.json"
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def save_user_data(self, user_id: str, data: dict)-> None:
        file_path = USER_DATA_PATH / f"{user_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def get_relationship_data(self, user_id: str, heroine_id: str)->dict:
        data = self.load_user_data(user_id)
        return data["relationship"][heroine_id]
    
    def get_value(self, user_id: str, heroine_id: str, key: str, default: None):
        relationship = self.get_relationship_data(user_id, heroine_id)
        return relationship.get(key, default)
    
    def set_value(self, user_id: str, heroine_id: str, key: str, value)->None:
        data = self.load_user_data(user_id)
        data["relationship"][heroine_id][key] = value
        self.save_user_data(user_id, data)
    
    def update_value(self, user_id: str, heroine_id: str, key: str, delta)->None:
        current = self.get_value(user_id, heroine_id, key, 0)
        self.set_value(user_id, heroine_id, key, current + delta)
    
    def has_flag(self, user_id: str, heroine_id: str, flag_name: str)->bool:
        relationship = self.get_relationship_data(user_id, heroine_id)
        return flag_name in relationship["flags"]
    
    def add_flag(self, user_id: str, heroine_id: str, flag_name: str)->None:
        data = self.load_user_data(user_id)
        flags = data["relationship"][heroine_id]["flags"]
        if flag_name not in flags:
            flags.append(flag_name)
        self.save_user_data(user_id, data)
    
    def get_relationship(self, user_id: str, heroine_id: str)->str:
        affection = self.get_value(user_id, heroine_id, "affection", 0)
        if affection < 0:
            return "ユーザーを嫌っている。"
        elif affection < 20:
            return "まだ少し警戒している。"
        elif affection < 50:
            return "友達として接している"
        elif affection < 80:
            return "好意を持っている"
        else:
            return "かなり好意を持っている"


class RelationshipManager:
    def __init__(self, uid: str):
        self.uid = uid

    def load_user_data(self) -> dict:
        file_path = USER_DATA_PATH / f"{self.uid}.json"
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
        return None

    def save_user_data(self, data: dict) -> None:
        file_path = USER_DATA_PATH / f"{self.uid}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_relationship_data(self, heroine_id: str) -> dict:
        data = self.load_user_data()
        return data["relationship"][heroine_id]

    def get_value(self,heroine_id: str, key: str, default: None):
        relationship = self.get_relationship_data(heroine_id)
        return relationship.get(key, default)

    def set_value(self, heroine_id: str, key: str, value) -> None:
        data = self.load_user_data()
        data["relationship"][heroine_id][key] = value
        self.save_user_data(data)

    def update_value(self, heroine_id: str, key: str, delta) -> None:
        current = self.get_value(heroine_id, key, 0)
        self.set_value(heroine_id, key, current + delta)

    def has_flag(self, heroine_id: str, flag_name: str) -> bool:
        relationship = self.get_relationship_data( heroine_id)
        return flag_name in relationship["flags"]

    def add_flag(self, user_id: str, heroine_id: str, flag_name: str) -> None:
        data = self.load_user_data()
        flags = data["relationship"][heroine_id]["flags"]
        if flag_name not in flags:
            flags.append(flag_name)
        self.save_user_data(data)

    def get_relationship(self, heroine_id: str) -> str:
        affection = self.get_value(heroine_id, "affection", 0)
        if affection < 0:
            return "ユーザーを嫌っている。"
        elif affection < 20:
            return "まだ少し警戒している。"
        elif affection < 50:
            return "友達として接している"
        elif affection < 80:
            return "好意を持っている"
        else:
            return "かなり好意を持っている"