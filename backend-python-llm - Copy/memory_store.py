# backend-python-llm/memory_store.py

memory_store = {}

def update_memory(user_id, key, value):
    memory_store.setdefault(user_id, {})[key] = value

def get_memory(user_id, key=None):
    user_data = memory_store.get(user_id, {})
    return user_data if key is None else user_data.get(key)
