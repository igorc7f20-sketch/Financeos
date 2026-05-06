class BaseRepository:
    """
    Base repository class.
    All feature repositories extend this to share common query patterns.
    """

    model = None

    @classmethod
    def get_by_id(cls, pk: int):
        return cls.model.objects.filter(pk=pk).first()

    @classmethod
    def get_all(cls):
        return cls.model.objects.all()

    @classmethod
    def create(cls, **kwargs):
        return cls.model.objects.create(**kwargs)

    @classmethod
    def delete(cls, pk: int) -> bool:
        obj = cls.get_by_id(pk)
        if obj:
            obj.delete()
            return True
        return False
