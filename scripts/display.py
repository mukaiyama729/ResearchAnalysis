import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as a3
from scipy.spatial import ConvexHull
from .table import Table


class Displayer:

    def __init__(self, dimention):
        self.dimention = dimention

    def v_points(self, points):
        if self.dimention == 2:
            fig, (ax1, ax2)= plt.subplots(2)
            pass
        elif self.dimention == 3:
            fig = plt.figure(figsize=(10,10))
            ax = fig.add_subplot(111, projection='3d')
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            ax.set_title('Atomic positions of interest')
            x, y, z = points[:,0], points[:,1], points[:,2]
            ax.plot(x, y, z, "o", ms=5, mew=0.5, label='point')
            plt.show()

    def v_vertices(self, vertices):
        if self.dimention == 2:
            pass
        elif self.dimention == 3:
            fig = plt.figure(figsize=(10,10))
            ax = fig.add_subplot(111, projection='3d')
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            ax.set_title('Vertices of Voronoi cells')
            x, y, z = vertices[:, 0], vertices[:, 1], vertices[:, 2]
            ax.plot(x, y, z, "o", color="green", ms=4, mew=0.5)
            plt.show()

    def v_ridge_points(self, ridge_points, points):
        if self.dimention == 2:
            pass
        elif self.dimention == 3:
            fig = plt.figure(figsize=(10,10))
            ax = fig.add_subplot(111, projection='3d')

            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            ax.set_title('Pairs of atoms between which each Voronoi ridge plane lies')
            for pair in points[ridge_points]:
                ax.plot(pair[:, 0], pair[:, 1], pair[:, 2], color='C0')
            plt.show()

    def v_ridge_vertices(self, ridge_vertices, v_vertices):
        if self.dimention == 2:
            pass
        elif self.dimention == 3:
            fig = plt.figure(figsize=(10,10))
            ax = fig.add_subplot(111, projection='3d')
            ax.set_xlabel('a')
            ax.set_ylabel('b')
            ax.set_zlabel('c')
            ax.set_aspect('equal')
            ax.set_xlim(-10,10)
            ax.set_ylim(-10,10)
            ax.set_zlim(-10,10)
            ax.set_title('Voronoi ridge planes')
            ridgenum = 0
            for i in np.array(ridge_vertices):
                #-1を含むものを取り除く
                if -1 not in i:
                    vertices = v_vertices[i]
                    xy, z = vertices[:, :-1], vertices[:, -1]
                    ridgenum += 1
                    poly=a3.art3d.Poly3DCollection([vertices],alpha=0.3)
                    poly.set_edgecolor('b')
                    poly.set_facecolor([0.5, 0.5, 1])
                    ax.add_collection3d(poly)
            plt.show()

    def v_region_and_points(self, vertices, regions, point_region):
        fig = plt.figure(figsize=(10,10))
        ax = fig.add_subplot(111, projection='3d')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('Voronoi ridge planes')
        '''
        ax.set_xlim(-10,10)
        ax.set_ylim(-10,10)
        ax.set_zlim(-10,10)
        '''

        for p in range(len(point_region)):
            color = f'C{p//2}' # 'C0' or 'C1'
            # Voronoi regionの頂点から凸包(convex hull)を求めてその面を表示
            if -1 in tuple(regions[point_region[p]]):
                continue
            ch = ConvexHull(vertices[regions[point_region[p]]])
            poly = a3.art3d.Poly3DCollection(
                ch.points[ch.simplices],
                alpha=0.3,
                facecolor=color,
                edgecolor='b'
            )
            ax.add_collection3d(poly)

            chpnts = ch.points[ch.vertices]
            ax.plot(
                chpnts[:, 0],
                chpnts[:, 1],
                chpnts[:, 2],
                ".",
                color=color,
                ms=10,
                mew=0.5
            )

    def d_points(self, points):
        if self.dimention == 2:
            pass
        elif self.dimention == 3:
            fig = plt.figure(figsize=(10,10))
            ax = fig.add_subplot(111, projection='3d')
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            ax.set_title('Atomic positions of interest')
            x, y, z = points[:,0], points[:,1], points[:,2]
            ax.plot(x, y, z, "o", ms=5, mew=0.5, label='point')
            plt.show()

    def d_region_and_points(self, points, d_vertices):
        fig = plt.figure(figsize=(10,10))
        ax = fig.add_subplot(111, projection='3d')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_title('Delaunay planes')

        for n, pair in enumerate(d_vertices):
            color = f'C{n//2}'
            ch = ConvexHull(points[pair])
            poly = a3.art3d.Poly3DCollection(
                ch.points[ch.simplices],
                alpha=0.1,
                facecolor=color,
                edgecolor='b'
            )
            ax.add_collection3d(poly)
            chpnts = ch.points[ch.vertices]
            ax.plot(chpnts[:, 0], chpnts[:, 1], chpnts[:, 2], ".", color=color, ms=10, mew=0.5)

    def kde_d_model_drawing(self, points, d_model, kde_model):
        if self.dimention == 2:
            fig = plt.figure(facecolor="w", figsize=(10,10))
            ax = fig.add_subplot(111, title="kernel density estimation and Delaunay tessellation")
            _x = points[:,0]
            _y = points[:,1]
            xlim = (np.min(_x) - 0.1, np.max(_x) + 0.1)
            ylim = (np.min(_y) - 0.1, np.max(_y) + 0.1)
            x = np.linspace(xlim[0], xlim[1], int((xlim[1] - xlim[0])) * 10 )
            y = np.linspace(ylim[0], ylim[1], int((ylim[1] - ylim[0])) * 10 )
            xx, yy = np.meshgrid(x, y)
            meshdata = np.vstack([xx.ravel(), yy.ravel()])
            z = kde_model.evaluate(meshdata)
            ax.scatter(points[:, 0], points[:, 1], c="b")

            higher_list = list(Table.take_higher(
                d_model.point_volume_dict,
                per=99
                ).keys()
            )
            ax.scatter(points[higher_list][:,0], points[higher_list][:,1], c='r')
            ax.contourf(
                xx,
                yy,
                z.reshape(len(y), len(x)),
                cmap="Blues",
                alpha=0.5
            )

            for n, pair in enumerate(d_model.vertices):
                #color = f'C{n//2}'
                three_points = points[pair]
                poly = pat.Polygon(
                    three_points,
                    alpha = 0,
                    linestyle=':'

                )
                ax.add_patch(poly)
                ax.plot(
                    three_points[:,0],
                    three_points[:,1],
                    lw=0.5,
                    linestyle='--',
                    color='green',
                    alpha=0.5
                )
            plt.show()
