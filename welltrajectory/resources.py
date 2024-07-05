from import_export import resources
from .models import WellTrajectory

class WellTrajectoryResource(resources.ModelResource):
    class Meta:
        model = WellTrajectory