/* field.js — the Harvest Map "field": a few thousand grains drifting on the
   wind, simulated and drawn on the GPU with WebGPU (Chrome 113+).
   Product asset, not mock chrome. Degrades to a CSS gradient when WebGPU is
   missing (data-gpu="off"), draws a single still frame under reduced motion,
   and reads its colour from the canvas's CSS `color` so themes just work. */
(async function () {
  const canvas = document.querySelector('canvas.field-canvas');
  if (!canvas) return;
  const off = () => { canvas.dataset.gpu = 'off'; };
  if (!('gpu' in navigator)) return off();
  let device, ctx;
  try {
    const adapter = await navigator.gpu.requestAdapter();
    if (!adapter) return off();
    device = await adapter.requestDevice();
    ctx = canvas.getContext('webgpu');
  } catch (e) { return off(); }
  const format = navigator.gpu.getPreferredCanvasFormat();
  ctx.configure({ device, format, alphaMode: 'premultiplied' });
  canvas.dataset.gpu = 'on';
  // Any validation error means the field is not drawing: say so and fall back to the CSS gradient.
  device.addEventListener('uncapturederror', (e) => { console.error('field.js: ' + e.error.message); off(); });

  const N = 4000;
  const particles = new Float32Array(N * 4);
  for (let i = 0; i < N; i++) {
    particles[i * 4] = Math.random() * 2.2 - 1.1;
    particles[i * 4 + 1] = Math.random() * 2.2 - 1.1;
    particles[i * 4 + 2] = 0;
    particles[i * 4 + 3] = Math.random();
  }
  const pbuf = device.createBuffer({ size: particles.byteLength, usage: GPUBufferUsage.STORAGE | GPUBufferUsage.COPY_DST });
  device.queue.writeBuffer(pbuf, 0, particles);
  const ubuf = device.createBuffer({ size: 32, usage: GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST });

  const wgsl = `
    struct P { pos: vec2f, vel: f32, seed: f32 };
    struct U { time: f32, dt: f32, aspect: f32, size: f32, color: vec4f };
    @group(0) @binding(0) var<storage, read_write> ps: array<P>;
    @group(0) @binding(0) var<storage, read> psr: array<P>; // vertex stages may only read storage
    @group(0) @binding(1) var<uniform> u: U;
    fn hash21(p: vec2f) -> f32 { var q = fract(p * vec2f(123.34, 456.21)); q += dot(q, q + 45.32); return fract(q.x * q.y); }
    fn noise(p: vec2f) -> f32 {
      let i = floor(p); let f = fract(p); let w = f * f * (3.0 - 2.0 * f);
      return mix(mix(hash21(i), hash21(i + vec2f(1, 0)), w.x), mix(hash21(i + vec2f(0, 1)), hash21(i + vec2f(1, 1)), w.x), w.y);
    }
    @compute @workgroup_size(64) fn step(@builtin(global_invocation_id) id: vec3u) {
      let i = id.x; if (i >= arrayLength(&ps)) { return; }
      var p = ps[i];
      let a = noise(p.pos * 1.8 + vec2f(u.time * 0.04, p.seed)) * 6.2832;
      let wind = vec2f(cos(a), sin(a)) * 0.06 + vec2f(0.05, 0.012);
      p.pos += wind * u.dt * (0.6 + p.seed);
      if (p.pos.x > 1.1) { p.pos.x = -1.1; }
      if (p.pos.y > 1.1) { p.pos.y = -1.1; }
      if (p.pos.y < -1.1) { p.pos.y = 1.1; }
      ps[i] = p;
    }
    struct VOut { @builtin(position) pos: vec4f, @location(0) uv: vec2f, @location(1) fade: f32, @location(2) wx: f32 };
    @vertex fn vs(@builtin(vertex_index) vi: u32, @builtin(instance_index) ii: u32) -> VOut {
      let corners = array<vec2f, 6>(vec2f(-1,-1), vec2f(1,-1), vec2f(-1,1), vec2f(-1,1), vec2f(1,-1), vec2f(1,1));
      let p = psr[ii]; let c = corners[vi];
      let s = u.size * (0.5 + p.seed);
      var o: VOut;
      o.pos = vec4f(p.pos + c * vec2f(s, s * u.aspect), 0.0, 1.0);
      o.uv = c; o.fade = 0.25 + 0.75 * fract(p.seed * 7.0 + u.time * 0.15); o.wx = p.pos.x;
      return o;
    }
    @fragment fn fs(i: VOut) -> @location(0) vec4f {
      // Grains thin out towards the left so the title sits on clean canvas; the field gathers on the right.
      let side = smoothstep(-0.7, 0.6, i.wx);
      let d = length(i.uv); let a = smoothstep(1.0, 0.5, d) * i.fade * side;
      return vec4f(u.color.rgb * a, a);
    }`;
  const mod = device.createShaderModule({ code: wgsl });
  const compute = device.createComputePipeline({ layout: 'auto', compute: { module: mod, entryPoint: 'step' } });
  const render = device.createRenderPipeline({
    layout: 'auto',
    vertex: { module: mod, entryPoint: 'vs' },
    fragment: { module: mod, entryPoint: 'fs', targets: [{ format, blend: { color: { srcFactor: 'one', dstFactor: 'one-minus-src-alpha' }, alpha: { srcFactor: 'one', dstFactor: 'one-minus-src-alpha' } } }] },
    primitive: { topology: 'triangle-list' },
  });
  const cbind = device.createBindGroup({ layout: compute.getBindGroupLayout(0), entries: [{ binding: 0, resource: { buffer: pbuf } }, { binding: 1, resource: { buffer: ubuf } }] });
  const rbind = device.createBindGroup({ layout: render.getBindGroupLayout(0), entries: [{ binding: 0, resource: { buffer: pbuf } }, { binding: 1, resource: { buffer: ubuf } }] });

  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const w = Math.max(1, Math.floor(canvas.clientWidth * dpr)), h = Math.max(1, Math.floor(canvas.clientHeight * dpr));
    if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
  }
  new ResizeObserver(resize).observe(canvas);
  resize();

  const color = new Float32Array(4);
  function readColor() {
    const m = getComputedStyle(canvas).color.match(/[\d.]+/g) || [194, 65, 12];
    color[0] = m[0] / 255; color[1] = m[1] / 255; color[2] = m[2] / 255; color[3] = 1;
  }
  const u = new Float32Array(8);
  const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let last = performance.now(), frames = 0;
  function frame(now) {
    const dt = Math.min(0.05, (now - last) / 1000); last = now;
    if (frames++ % 30 === 0) readColor();
    u[0] = now / 1000; u[1] = still ? 0 : dt; u[2] = canvas.width / canvas.height; u[3] = 0.006;
    u.set(color, 4);
    device.queue.writeBuffer(ubuf, 0, u);
    const enc = device.createCommandEncoder();
    const cp = enc.beginComputePass(); cp.setPipeline(compute); cp.setBindGroup(0, cbind); cp.dispatchWorkgroups(Math.ceil(N / 64)); cp.end();
    const rp = enc.beginRenderPass({ colorAttachments: [{ view: ctx.getCurrentTexture().createView(), clearValue: { r: 0, g: 0, b: 0, a: 0 }, loadOp: 'clear', storeOp: 'store' }] });
    rp.setPipeline(render); rp.setBindGroup(0, rbind); rp.draw(6, N); rp.end();
    device.queue.submit([enc.finish()]);
    if (!still && !document.hidden) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
  document.addEventListener('visibilitychange', () => { if (!document.hidden && !still) { last = performance.now(); requestAnimationFrame(frame); } });
})();
