from surfplot import Plot
import os

def plot_maps(map, range=None, cmap='viridis', cbar=True):
    # Surface mesh files
    surf_mesh = os.path.join('resources','surface_meshes','fs_LR_32K','fs_LR.32k.{hemi}.very_inflated.surf.gii')

    # Glasser atlas files
    surf_atlas = os.path.join('resources','surface_atlases','Glasser_2016.32k.{hemi}.label.gii')

    kws = {'location': 'bottom', 'label_direction': 45, 'decimals': 2,
    'fontsize': 8, 'n_ticks': 7, 'shrink': 0.5, 'aspect': 40}
    
    # plot surface mesh
    p = Plot(surf_lh=surf_mesh.format(hemi='L'), surf_rh=surf_mesh.format(hemi='R'), brightness = 0.7, size=(1600, 400), zoom=1.2, layout='row')
    # plot the map
    p.add_layer({'left': map.format(hemi='L'), 'right': map.format(hemi='R')}, cbar=cbar, color_range=range, cmap=cmap)
    # plot atlas borders
    p.add_layer({'left': surf_atlas.format(hemi='L'), 'right': surf_atlas.format(hemi='R')}, cmap='gray', as_outline=True, cbar=False)
    fig = p.build(cbar_kws=kws)