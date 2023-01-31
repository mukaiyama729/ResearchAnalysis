
class ArrangeData:

    def __init__(self, data):
        self.data = data
        self.averaged_data = None
        self.length = len(data)

    def sorted_points_of_h_volume(self, percent):
        return self.data.sort_values('volume', ascending=False).head(int(self.length * percent))

    def averaged_trajectory_data(self):
        return self.data.groupby(['trial', 'cycle', 'reprica']).mean()
