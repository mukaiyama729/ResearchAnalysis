
class ArrangeData:

    def __init__(self, data):
        self.data = data
        self.averaged_data = None
        self.length = len(data)

    def sorted_points_of_high_volume(self, percent):
        return self.extract_from_top(self.sort_volume(self.data), percent)
        #return self.data.sort_values('volume', ascending=False).head(int(self.length * percent))

    def averaged_trajectory_data(self):
        return self.data.groupby(['trial', 'cycle', 'reprica'], as_index=False).mean()

    def sort_volume(self, data):
        return data.sort_values('volume', ascending=False)

    def extract_from_top(self, data, percent):
        return data.head(int(len(data) * percent * 0.01))
