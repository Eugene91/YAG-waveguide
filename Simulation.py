import meep as mp
import numpy as np
import math
import argparse


PML = 2 # thickness of perfectly matched layer 


def build_geometry(a_axis, b_axis, core_rad, sx, sy, sz, n=1.822, dn=-0.004, number_of_ellipses=18):
    
    geometry = []
    
    geometry.append(mp.Block(size=mp.Vector3(sx,sy,sz),
                center=mp.Vector3(0,0,0),         
                material=mp.Medium(index=n)))

    # add ellipses around the core's circumference 
    for angle in np.arange(0, 2*math.pi, 2*math.pi/number_of_ellipses):
        
        vert=[]

        for x in np.arange(-a_axis,a_axis+0.1,0.1):
            vert.append(mp.Vector3(x,-(b_axis/a_axis)*(a_axis**2-x**2)**(1/2)))

        for x in np.arange(a_axis-0.1,-a_axis,-0.1):
            vert.append(mp.Vector3(x,(b_axis/a_axis)*(a_axis**2-x**2)**(1/2))) 


        geometry.append(mp.Prism(vert,
                            height=sz,
                            center=mp.Vector3((core_rad+a_axis)*math.cos(angle),(core_rad+b_axis)*math.sin(angle),0),
                                 material=mp.Medium(index=n+dn)))
    return geometry

    
    


def main(args):
    
    wvg = args.wvg     # pulse carrier wavelength
    fcen = 1/wvg       # pulse center frequency
    df = args.df       # pulse width (in frequency)
    ref_index = args.n # core refractive index
    dn = args.dn       # difference in refractive index between the core and the ellipsoids
    core_rad = args.core # core radius
    a_axis = args.a    # first axis of ellipsoid
    b_axis = args.b    # second axis of ellipsoid
    t_sim = args.time  # simulation time
    N = args.N         # number of ellipses
    
    sx = 2*core_rad + 4*a_axis + 2  # computaional size in x direction
    sy = 2*core_rad + 4*b_axis + 2  # computaional size in y direction
    sz = 4                   # computaional size in z direction
        
    source_sx = 2*core_rad + 4*a_axis      # source size in x direction
    source_sy = 2*core_rad + 4*b_axis      # source size in y direction
    
    
    
    kpoint = mp.Vector3(0, 0, wvg) # source wave vector
    wvg_parity = mp.ODD_Y 
    
    
    # define the source property
    # use of EigenModeSource automatically force meep to
    # run eigen mode solver
    sources = [mp.EigenModeSource(src = mp.ContinuousSource(frequency=fcen),
                          center = mp.Vector3(0,0,0),
                          size = mp.Vector3(source_sx, source_sy, 0),
                          eig_band = 1,
                          direction = mp.Z,
                          eig_kpoint = kpoint,
                          eig_parity = wvg_parity,
                          eig_match_freq=True)]
    # define geomtry
    geometry = build_geometry(a_axis, b_axis, core_rad, sx, sy, sz, n=ref_index, dn=dn, number_of_ellipses=N)
    # computational cell size
    cell_size = mp.Vector3(sx+2*PML,sy+2*PML,sz+PML)

    vol = mp.Volume(mp.Vector3(0,0,0), size=mp.Vector3(sx+2*PML, sy+2*PML, 0.5))
    
    sim = mp.Simulation(resolution = 20,
                    cell_size = cell_size,
                    sources = sources,
                    geometry = geometry,
                    filename_prefix = args.name,
                    eps_averaging = False    
                   )

    sim.run(mp.at_beginning(mp.output_epsilon),
        mp.to_appended("ey", mp.at_every(0.1, mp.output_efield_y)),
        mp.in_volume(vol, mp.to_appended("ey", mp.at_every(0.1, mp.output_efield_y))),
        until = t_sim)
    
    




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-wvg', dest='wvg', type=float, default=0.795, help='wavelength of the waveguide in um')
    parser.add_argument('-df', dest='df', type=float, default=0.25, help='Pulse width')
    parser.add_argument('-n', dest='n', type=float, default=1.822, help='Material refractive index')
    parser.add_argument('-dn', dest='dn', type=float, default=-0.004, help='Difference in refractive index between material and laser written part')
    parser.add_argument('-t', dest='time', type=float, default=10, help='Simulation time')
    parser.add_argument('-c', dest='core', type=float, default=8, help='Core radius')
    parser.add_argument('-N', dest='N', type=int, default=18, help='Number of ellipses')
    parser.add_argument('-a', dest='a', type=float, default=1, help='Semi-minor axis of laser-printed ellipses')
    parser.add_argument('-b', dest='b', type=float, default=4, help='Semi-major axis of laser printed ellipses')
    parser.add_argument('-res', dest='res', type=int, default=20, help='Number of ellipses')
    parser.add_argument("-name", dest="name", default="YAG",type=str, help="File name prefix for saved files")
    
    
    
    args = parser.parse_args()
    main(args) 