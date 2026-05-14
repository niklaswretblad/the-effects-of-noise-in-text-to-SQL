class BaseModel:
    def generate_query(self, *args, **kwargs):
        raise NotImplementedError("generate_query() not implemented")
