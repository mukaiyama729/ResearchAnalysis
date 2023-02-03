
class ArrangeData:

    def __init__(self, data):
        self.data = data
        self.averaged_data = None
        self.length = len(data)

    def sorted_points_of_large_volume(self, percent):
        return self.extract_from_top(self.sort_volume(self.data), percent)
        #return self.data.sort_values('volume', ascending=False).head(int(self.length * percent))

    def averaged_trajectory_data(self):
        return self.data.groupby(['trial', 'cycle', 'reprica'], as_index=False).mean()

    def sort_volume(self, data, asc=False):
        return data.sort_values('volume', ascending=asc)

    def extract_from_top(self, data, percent):
        return data.head(int(len(data) * percent * 0.01))

    def sorted_points_of_low_density(self, percent):
        return self.extract_from_top(self.sort_volume(self.data, asc=True), percent)

    def extract_from_bottom(self, data, percent):
        return data.tail(int(len(data) * percent * 0.01))
