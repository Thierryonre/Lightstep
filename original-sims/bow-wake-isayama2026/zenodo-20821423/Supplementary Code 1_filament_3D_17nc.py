# -*- coding: utf-8 -*-
"""
3D filamentary density generator for EPOCH
+ 2D slice plots with unified color scale
+ 3D scatter visualization (point cloud)
+ 3D box surface visualization (6 faces full plot)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from math import atan
from scipy.ndimage import gaussian_filter
from scipy.stats import truncnorm
from mpl_toolkits.mplot3d import Axes3D   # noqa: F401
from matplotlib.cm import get_cmap
from matplotlib.colors import Normalize

# ============================================================
# ===================== GLOBAL SETTINGS ======================
# ============================================================

PLOT_VMIN_NNC = 0.0
PLOT_VMAX_NNC = 15.0
SCATTER_STRIDE = 4
SCATTER_NNC_MIN = 0.5

# --------------------------- random seed ---------------------------
seed_number = 1711
rng = np.random.default_rng(seed_number)

# --------------------------- physical constants ---------------------------
um = 1e-6
c = 2.99792458e8
pi = 4.0 * atan(1.0)
me = 9.1093837139e-31
e_charge = 1.602176634e-19
lambda0 = 0.81 * um
freq = c / lambda0
epsilon0 = 8.85418782e-12
omega = 2 * pi * freq
nc = epsilon0 * me * omega**2 / e_charge**2   # critical density
print("nc =", nc, "[m^-3]")

# --------------------------- grid and domain ---------------------------
nx, ny, nz = 2500, 250, 250
dx = 0.08 * um
dy = 0.08 * um
dz = 0.08 * um

sim_range = {
    'xmin': -10.0 * um,
    'xmax': -10.0 * um + dx * (nx - 1),
    'ymin': -10.0 * um,
    'ymax': -10.0 * um + dy * (ny - 1),
    'zmin': -10.0 * um,
    'zmax': -10.0 * um + dz * (nz - 1),
}

# plasma (target) region
target_range = {
    'xmin': 0.0 * um,
    'xmax': 100.0 * um,
    'ymin': sim_range['ymin'],
    'ymax': sim_range['ymax'],
    'zmin': sim_range['zmin'],
    'zmax': sim_range['zmax'],
}

def to_index_x(x):
    return int(np.clip((x - sim_range['xmin']) / (sim_range['xmax'] - sim_range['xmin']) * (nx - 1), 0, nx - 1))

def to_index_y(y):
    return int(np.clip((y - sim_range['ymin']) / (sim_range['ymax'] - sim_range['ymin']) * (ny - 1), 0, ny - 1))

def to_index_z(z):
    return int(np.clip((z - sim_range['zmin']) / (sim_range['zmax'] - sim_range['zmin']) * (nz - 1), 0, nz - 1))

tx0, tx1 = to_index_x(target_range['xmin']), to_index_x(target_range['xmax'])
ty0, ty1 = to_index_y(target_range['ymin']), to_index_y(target_range['ymax'])
tz0, tz1 = to_index_z(target_range['zmin']), to_index_z(target_range['zmax'])

# --------------------------- filament parameters ---------------------------
num_filaments = 20000
steps_per_filament = 2000

turn_std_theta = 0.2
turn_std_phi   = 0.2
phi_max = np.deg2rad(90.0)

step_pix = 1.0
filament_sigma_pix   = 0.2
post_blur_sigma_pix  = 0.1
gamma                = 1.4
bg_level             = 0.1
final_scale_nc = 17.0

# --------------------------- filament generator ---------------------------
def generate_filament_field_3d(nx, ny, nz,
                               tx0, tx1, ty0, ty1, tz0, tz1,
                               rng, return_intermediates=False):

    field = np.zeros((nx, ny, nz), dtype=np.float32)

    rad = max(1, int(3 * filament_sigma_pix))
    gxs = np.arange(-rad, rad + 1)
    gys = np.arange(-rad, rad + 1)
    gzs = np.arange(-rad, rad + 1)
    GX, GY, GZ = np.meshgrid(gxs, gys, gzs, indexing='ij')
    brush = np.exp(-(GX**2 + GY**2 + GZ**2) / (2 * filament_sigma_pix**2)).astype(np.float32)

    for i_fil in range(num_filaments):
        if i_fil % 200 == 0:
            print("Filament", i_fil, "/", num_filaments, flush=True)

        px = float(rng.integers(tx0, tx1+1))
        py = float(rng.integers(ty0, ty1+1))
        pz = float(rng.integers(tz0, tz1+1))

        theta = rng.uniform(0, 2*np.pi)
        phi   = rng.uniform(-phi_max, phi_max)

        for _ in range(steps_per_filament):
            x0 = int(round(px))
            y0 = int(round(py))
            z0 = int(round(pz))

            if x0 < 0 or x0 >= nx or y0 < 0 or y0 >= ny or z0 < 0 or z0 >= nz:
                break

            xs = slice(max(0, x0-rad), min(nx, x0+rad+1))
            ys = slice(max(0, y0-rad), min(ny, y0+rad+1))
            zs = slice(max(0, z0-rad), min(nz, z0+rad+1))

            bx0 = rad - (x0 - xs.start)
            by0 = rad - (y0 - ys.start)
            bz0 = rad - (z0 - zs.start)

            field[xs, ys, zs] += brush[
                bx0:bx0+(xs.stop-xs.start),
                by0:by0+(ys.stop-ys.start),
                bz0:bz0+(zs.stop-zs.start)
            ]

            theta += rng.normal(0, turn_std_theta)
            phi   += rng.normal(0, turn_std_phi)

            vx = np.cos(phi)*np.cos(theta)
            vy = np.cos(phi)*np.sin(theta)
            vz = np.sin(phi)

            px += step_pix * vx
            py += step_pix * vy
            pz += step_pix * vz

            if px < tx0: px = tx0 + (tx0 - px); theta += np.pi
            if px > tx1: px = tx1 - (px - tx1); theta += np.pi
            if py < ty0: py = ty0 + (ty0 - py); theta = -theta
            if py > ty1: py = ty1 - (py - ty1); theta = -theta
            if pz < tz0: pz = tz0 + (tz0 - pz); phi = -phi
            if pz > tz1: pz = tz1 - (pz - tz1); phi = -phi

    if post_blur_sigma_pix > 0:
        field = gaussian_filter(field, post_blur_sigma_pix, mode='nearest')

    m = field[tx0:tx1+1, ty0:ty1+1, tz0:tz1+1]
    vmax = np.percentile(m, 90.0) if m.size else 1.0
    if vmax <= 0:
        vmax = 1.0

    norm_map = np.clip(field / vmax, 0, 1)
    gamma_map = norm_map ** gamma

    mask = np.zeros_like(field)
    mask[tx0:tx1+1, ty0:ty1+1, tz0:tz1+1] = 1.0
    out = mask * (bg_level + (1-bg_level)*gamma_map)

    if return_intermediates:
        return out, norm_map, field
    return out

# --------------------------- truncated Gaussian ---------------------------
def map_to_truncated_gaussian_rescale_3d(field,
                                         tx0, tx1, ty0, ty1, tz0, tz1,
                                         mu, sigma, final_scale_nc):

    mask = np.zeros_like(field, dtype=bool)
    mask[tx0:tx1+1, ty0:ty1+1, tz0:tz1+1] = True
    vals = field[mask].astype(np.float64)

    order = np.argsort(vals)
    ranks = np.empty_like(order)
    ranks[order] = np.arange(1, len(vals)+1)
    u = ranks / (len(vals)+1.0)

    a, b = (0.0-mu)/sigma, np.inf
    multipliers = truncnorm.ppf(u, a, b, loc=mu, scale=sigma)

    mean0 = multipliers.mean()
    if mean0 != 0:
        multipliers *= (1.0/mean0)

    out = np.zeros_like(field, dtype=np.float64)
    out[mask] = multipliers * final_scale_nc * nc
    return out, multipliers, u

# --------------------------- save species ---------------------------
def save_species_densities_3d(electron_3d, output_dir, tag):
    ratio_carbon = 4.0/41.0
    ratio_proton = 5.0/41.0
    ratio_oxy    = 2.0/41.0

    carbon_3d = electron_3d * ratio_carbon
    proton_3d = electron_3d * ratio_proton
    oxy_3d    = electron_3d * ratio_oxy

    def save_3d(arr, path):
        arr_out = np.transpose(arr, (2, 1, 0))  # (z,y,x) for EPOCH
        arr_out.astype(np.float64).tofile(path)

    save_3d(electron_3d, os.path.join(output_dir, f"electron_density_3d_{tag}.bin"))
    save_3d(carbon_3d,    os.path.join(output_dir, f"carbon_density_3d_{tag}.bin"))
    save_3d(proton_3d,    os.path.join(output_dir, f"proton_density_3d_{tag}.bin"))
    save_3d(oxy_3d,       os.path.join(output_dir, f"oxy_density_3d_{tag}.bin"))

# --------------------------- histogram of density ---------------------------
def save_final_density_hist_3d(density_3d, tx0, tx1, ty0, ty1, tz0, tz1, output_dir, tag):
    dens_target = density_3d[tx0:tx1+1, ty0:ty1+1, tz0:tz1+1].ravel()
    dens_target_nnc = dens_target[dens_target > 0] / nc
    if dens_target_nnc.size == 0:
        return

    plt.figure(figsize=(7,5))
    plt.hist(dens_target_nnc, bins=100, density=True, alpha=0.6)
    plt.xlabel("n / nc")
    plt.ylabel("PDF")
    plt.title("Final Density Distribution")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"hist_density_{tag}.png"), dpi=300)
    plt.close()

# --------------------------- slice plots (unified color scale) ---------------------------
def save_slice_plots(density_3d, sim_range, output_dir, tag="fil3d"):
    iz_mid = density_3d.shape[2] // 2
    iy_mid = density_3d.shape[1] // 2
    ix_mid = density_3d.shape[0] // 2

    vmin_nnc = PLOT_VMIN_NNC
    vmax_nnc = PLOT_VMAX_NNC

    # xy
    plt.figure(figsize=(7,5))
    plt.imshow((density_3d[:,:,iz_mid]/nc).T,
               origin='lower', cmap='jet',
               extent=(sim_range['xmin']/um, sim_range['xmax']/um,
                       sim_range['ymin']/um, sim_range['ymax']/um),
               vmin=vmin_nnc, vmax=vmax_nnc)
    plt.colorbar(label='n/nc')
    plt.xlabel("x [um]")
    plt.ylabel("y [um]")
    plt.title("XY slice (z mid)")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"slice_xy_{tag}.png"), dpi=300)
    plt.close()

    # xz
    plt.figure(figsize=(7,5))
    plt.imshow((density_3d[:,iy_mid,:]/nc).T,
               origin='lower', cmap='jet',
               extent=(sim_range['xmin']/um, sim_range['xmax']/um,
                       sim_range['zmin']/um, sim_range['zmax']/um),
               vmin=vmin_nnc, vmax=vmax_nnc)
    plt.colorbar(label='n/nc')
    plt.xlabel("x [um]")
    plt.ylabel("z [um]")
    plt.title("XZ slice (y mid)")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"slice_xz_{tag}.png"), dpi=300)
    plt.close()

    # yz
    plt.figure(figsize=(7,5))
    plt.imshow((density_3d[ix_mid,:,:]/nc).T,
               origin='lower', cmap='jet',
               extent=(sim_range['ymin']/um, sim_range['ymax']/um,
                       sim_range['zmin']/um, sim_range['zmax']/um),
               vmin=vmin_nnc, vmax=vmax_nnc)
    plt.colorbar(label='n/nc')
    plt.xlabel("y [um]")
    plt.ylabel("z [um]")
    plt.title("YZ slice (x mid)")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"slice_yz_{tag}.png"), dpi=300)
    plt.close()

# --------------------------- 3D scatter plot (unified color scale) ---------------------------
def save_3d_scatter_plot(density_3d, sim_range, output_dir,
                         tag="fil3d", stride=SCATTER_STRIDE, nnc_min=SCATTER_NNC_MIN):

    n_nc = density_3d / nc
    nx_local, ny_local, nz_local = n_nc.shape

    ix = np.arange(0, nx_local, stride)
    iy = np.arange(0, ny_local, stride)
    iz = np.arange(0, nz_local, stride)

    IX, IY, IZ = np.meshgrid(ix, iy, iz, indexing='ij')
    vals = n_nc[IX, IY, IZ]

    mask = vals >= nnc_min
    if not np.any(mask):
        return

    IX = IX[mask]
    IY = IY[mask]
    IZ = IZ[mask]
    vals = np.clip(vals[mask], PLOT_VMIN_NNC, PLOT_VMAX_NNC)

    x_um = sim_range['xmin']/um + IX*(dx/um)
    y_um = sim_range['ymin']/um + IY*(dy/um)
    z_um = sim_range['zmin']/um + IZ*(dz/um)

    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111, projection='3d')

    sc = ax.scatter(x_um, y_um, z_um,
                    c=vals, s=2, cmap='jet',
                    vmin=PLOT_VMIN_NNC, vmax=PLOT_VMAX_NNC)

    cbar = fig.colorbar(sc, ax=ax, shrink=0.6)
    cbar.set_label("n/nc")

    ax.set_xlabel("x [um]")
    ax.set_ylabel("y [um]")
    ax.set_zlabel("z [um]")
    ax.set_title(f"3D point cloud (stride={stride})")

    ax.view_init(elev=20, azim=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"scatter3d_{tag}.png"), dpi=300)
    plt.close()

# --------------------------- 3D box surfaces (unified color scale) ---------------------------
def save_3d_box_surfaces(density_3d, sim_range, output_dir,
                         tag="fil3d", alpha_face=0.8):

    vmin_nnc = PLOT_VMIN_NNC
    vmax_nnc = PLOT_VMAX_NNC

    n_nc = density_3d / nc
    nx_, ny_, nz_ = n_nc.shape

    x_idx = np.arange(tx0, tx1 + 1)
    y_idx = np.arange(0, ny_)
    z_idx = np.arange(0, nz_)

    x_arr = sim_range['xmin']/um + x_idx * (dx/um)
    y_arr = sim_range['ymin']/um + y_idx * (dy/um)
    z_arr = sim_range['zmin']/um + z_idx * (dz/um)

    cmap = get_cmap('jet')
    norm = Normalize(vmin=vmin_nnc, vmax=vmax_nnc)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # x = x0 (plasma front)
    Y_x0, Z_x0 = np.meshgrid(y_arr, z_arr, indexing='ij')
    X_x0 = np.full_like(Y_x0, x_arr[0])
    slice_x0 = np.clip(n_nc[tx0, :, :], vmin_nnc, vmax_nnc)
    colors_x0 = cmap(norm(slice_x0)); colors_x0[..., 3] = alpha_face
    ax.plot_surface(X_x0, Y_x0, Z_x0, facecolors=colors_x0,
                    rstride=1, cstride=1, linewidth=0, antialiased=False, shade=False)

    # x = x1
    Y_x1, Z_x1 = np.meshgrid(y_arr, z_arr, indexing='ij')
    X_x1 = np.full_like(Y_x1, x_arr[-1])
    slice_x1 = np.clip(n_nc[tx1, :, :], vmin_nnc, vmax_nnc)
    colors_x1 = cmap(norm(slice_x1)); colors_x1[..., 3] = alpha_face
    ax.plot_surface(X_x1, Y_x1, Z_x1, facecolors=colors_x1,
                    rstride=1, cstride=1, linewidth=0, antialiased=False, shade=False)

    # y = y0
    X_y0, Z_y0 = np.meshgrid(x_arr, z_arr, indexing='ij')
    Y_y0 = np.full_like(X_y0, y_arr[0])
    slice_y0 = np.clip(n_nc[tx0:tx1+1, 0, :], vmin_nnc, vmax_nnc)
    colors_y0 = cmap(norm(slice_y0)); colors_y0[..., 3] = alpha_face
    ax.plot_surface(X_y0, Y_y0, Z_y0, facecolors=colors_y0,
                    rstride=1, cstride=1, linewidth=0, antialiased=False, shade=False)

    # y = y1
    X_y1, Z_y1 = np.meshgrid(x_arr, z_arr, indexing='ij')
    Y_y1 = np.full_like(X_y1, y_arr[-1])
    slice_y1 = np.clip(n_nc[tx0:tx1+1, -1, :], vmin_nnc, vmax_nnc)
    colors_y1 = cmap(norm(slice_y1)); colors_y1[..., 3] = alpha_face
    ax.plot_surface(X_y1, Y_y1, Z_y1, facecolors=colors_y1,
                    rstride=1, cstride=1, linewidth=0, antialiased=False, shade=False)

    # z = z0
    X_z0, Y_z0 = np.meshgrid(x_arr, y_arr, indexing='ij')
    Z_z0 = np.full_like(X_z0, z_arr[0])
    slice_z0 = np.clip(n_nc[tx0:tx1+1, :, 0], vmin_nnc, vmax_nnc)
    colors_z0 = cmap(norm(slice_z0)); colors_z0[..., 3] = alpha_face
    ax.plot_surface(X_z0, Y_z0, Z_z0, facecolors=colors_z0,
                    rstride=1, cstride=1, linewidth=0, antialiased=False, shade=False)

    # z = z1
    X_z1, Y_z1 = np.meshgrid(x_arr, y_arr, indexing='ij')
    Z_z1 = np.full_like(X_z1, z_arr[-1])
    slice_z1 = np.clip(n_nc[tx0:tx1+1, :, -1], vmin_nnc, vmax_nnc)
    colors_z1 = cmap(norm(slice_z1)); colors_z1[..., 3] = alpha_face
    ax.plot_surface(X_z1, Y_z1, Z_z1, facecolors=colors_z1,
                    rstride=1, cstride=1, linewidth=0, antialiased=False, shade=False)

    # colorbar
    mappable = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    mappable.set_array([])
    cbar = fig.colorbar(mappable, ax=ax, shrink=0.6)
    cbar.set_label("n/nc")

    ax.set_xlabel("x [um]")
    ax.set_ylabel("y [um]")
    ax.set_zlabel("z [um]")
    ax.set_title("3D plasma box surfaces")

    try:
        ax.set_box_aspect([
            x_arr[-1] - x_arr[0],
            y_arr[-1] - y_arr[0],
            z_arr[-1] - z_arr[0],
        ])
    except Exception:
        pass

    ax.view_init(elev=20, azim=-45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"box_surfaces3d_{tag}.png"), dpi=300)
    plt.close()

# --------------------------- main ---------------------------
if __name__ == "__main__":

    root_outdir = "/vol0004/mdt1/data/hp240019/u14248/epoch_inputs/filament_density"
    tag = "fil3d_n17_1"
    outdir = os.path.join(root_outdir, tag)
    os.makedirs(outdir, exist_ok=True)

    print("Generating filaments...")
    filament_field_3d, norm_map_3d, accum_map_3d = generate_filament_field_3d(
        nx, ny, nz, tx0, tx1, ty0, ty1, tz0, tz1, rng, return_intermediates=True
    )

    print("Mapping to truncated Gaussian...")
    density_3d, multipliers, u = map_to_truncated_gaussian_rescale_3d(
        filament_field_3d, tx0, tx1, ty0, ty1, tz0, tz1, mu=1.0, sigma=2.0,
        final_scale_nc=final_scale_nc
    )

    print("Saving species 3D data...")
    save_species_densities_3d(density_3d, outdir, tag)

    save_final_density_hist_3d(density_3d, tx0, tx1, ty0, ty1, tz0, tz1, outdir, tag)

    print("Saving 2D slice plots...")
    save_slice_plots(density_3d, sim_range, outdir, tag)

    print("Saving 3D scatter plot...")
    save_3d_scatter_plot(density_3d, sim_range, outdir, tag,
                         stride=SCATTER_STRIDE, nnc_min=SCATTER_NNC_MIN)

    print("Saving 3D box surface plot...")
    save_3d_box_surfaces(density_3d, sim_range, outdir, tag=tag, alpha_face=0.8)

    print("Done.")
