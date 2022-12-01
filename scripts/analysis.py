from tessellation import Tessellation

class Analyser(Tessellation):

    def __init__(self, points):
        super.__init__(points)

    def v_volume(self):
        if self.v_model is None:
            self.voronoi_cal()
            return self.v_show_data()
        else:
            return self.v_show_data()

    def d_volume(self):
        if self.d_model is None:
            self.delaunay_cal()
            return self.d_show_data()
        else:
            return self.d_show_data()

    def kde_density(self):
        if self.kde_model is None:
            self.kernel_density_estimation()
            return self.kde_show_data()
        else:
            return self.kde_show_data()

    def display_voronoi(self, dimention, what):
        if self.v_model is None:
            self.voronoi_cal()
            return self.v_display(dimention, what)
        else:
            return self.v_display(dimention, what)

    def display_delaunay(self, dimention, what):
        if self.v_model is None:
            self.voronoi_cal()
            return self.d_display(dimention, what)
        else:
            return self.d_display(dimention, what)




