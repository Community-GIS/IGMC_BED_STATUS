from import_export import resources
from .models import bulk_reg

class bulkResource(resources.ModelResource):
    class meta:
        model = bulk_reg