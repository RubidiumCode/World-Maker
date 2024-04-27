use pyo3::prelude::*;
use rand::{Rng, SeedableRng};
use rand::rngs::StdRng;

struct Vector2D{
    x: f64,
    y: f64
}

fn random_vector(ix: i64, iy: i64) -> Vector2D {
    let seed: u64 = (ix * iy) as u64;
    let mut r = StdRng::seed_from_u64(seed); 
    let mut angle: f64 = r.gen();
    angle *= 6.283185;
    
    let v = Vector2D{
        x: angle.sin(),
        y: angle.cos()
    };
    v
}

fn dot_gradient(ix: i64, iy: i64, x: f64, y: f64) -> f64{
    let gradient = random_vector(ix, iy);
    let dx = x - ix as f64;
    let dy = y - iy as f64;

    dx * gradient.x + dy * gradient.y
}

fn interpolate(a0: f64, a1: f64, w: f64) -> f64{
    (a1 - a0) * (3.0 - w * 2.0) * w * w + a0
}

#[pyfunction]
fn perlin_noise(x: f64, y: f64) -> PyResult<f64>{
    let x0: i64 = x as i64;
    let y0: i64 = y as i64;
    let x1: i64 = x0 + 1;
    let y1: i64 = y0 + 1;

    let sx = x - x0 as f64;
    let sy = y - y0 as f64;

    let n0 = dot_gradient(x0, y0, x, y);
    let n1 = dot_gradient(x1, y0, x, y);
    let ix0 = interpolate(n0, n1, sx);

    let n0 = dot_gradient(x0, y1, x, y);
    let n1 = dot_gradient(x1, y1, x, y);
    let ix1 = interpolate(n0, n1, sx);

    Ok(interpolate(ix0, ix1, sy))

}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(perlin_noise, m)?)?;
    Ok(())
}
