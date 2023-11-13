from surfplot import Plot
import os

def plot_maps(map):
    # Surface mesh files
    surf_mesh = os.path.join('..','resources','surface_meshes','fs_LR.32k.{hemi}.very_inflated.surf.gii')

    # Glasser atlas files
    surf_atlas = os.path.join('..','resources','surface_atlases','Glasser_2016.32k.{hemi}.label.gii')

    kws = {'location': 'bottom', 'label_direction': 45, 'decimals': 2,
    'fontsize': 8, 'n_ticks': 7, 'shrink': 0.5, 'aspect': 40}
    
    # plot surface mesh
    p = Plot(surf_lh=surf_mesh.format(hemi='L'), surf_rh=surf_mesh.format(hemi='R'), brightness = 0.7, size=(1600, 400), zoom=1.2, layout='row')
    # plot the map
    p.add_layer({'left': map.format(hemi='L'), 'right': map.format(hemi='R')}, cbar=True)
    # plot atlas borders
    p.add_layer({'left': surf_atlas.format(hemi='l'), 'right': surf_atlas.format(hemi='r')}, cmap='gray', as_outline=True, cbar=False)
    fig = p.build(cbar_kws=kws)