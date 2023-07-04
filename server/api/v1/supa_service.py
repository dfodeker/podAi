from supabase import create_client, Client

class SupabaseService:
    def __init__(self, url: str, key: str):
        self.client: Client = create_client(url, key)

    def get_interactions(self):
        data, error = self.client.from_('interactions').select('user_id, user_input')
        if error:
            raise ValueError("Error fetching interactions: ", error)
        return data
