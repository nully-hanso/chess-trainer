import bpy, bmesh, math, sys, os
from mathutils import Vector, Matrix

OUT = sys.argv[sys.argv.index('--')+1]
ONLY = sys.argv[sys.argv.index('--')+2] if len(sys.argv) > sys.argv.index('--')+2 else ''
os.makedirs(OUT, exist_ok=True)
ELEV = math.radians(24)
KING_H = 0.92
TARGET = {'p': .44, 'n': .58, 'b': .61, 'r': .67, 'q': .70, 'k': .74}
W, H = 288, 360

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def arc(cz, R, a0, a1, n=10, cx=0.0):
    return [(cx + R*math.cos(math.radians(a0+(a1-a0)*i/n)), cz + R*math.sin(math.radians(a0+(a1-a0)*i/n))) for i in range(n+1)]

def base(rb):
    return [(0, 0), (rb, 0), (rb, .03)] + arc(.05, .022, -60, 60, 6, rb-.012) + [(rb*.9, .075), (rb*.9, .088)] + arc(.105, .02, -90, 60, 5, rb*.78) + [(rb*.68, .13)]

def lathe(name, prof, seg=72):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    vs = [bm.verts.new((r, 0, z)) for r, z in prof]
    for a, b in zip(vs, vs[1:]): bm.edges.new((a, b))
    bmesh.ops.spin(bm, geom=bm.verts[:]+bm.edges[:], cent=(0, 0, 0), axis=(0, 0, 1), angle=math.tau, steps=seg, use_merge=True)
    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-5)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(ob)
    smooth(ob); return ob

def smooth(ob, ang=50):
    for p in ob.data.polygons: p.use_smooth = True
    m = ob.modifiers.new('sm', 'SMOOTH_BY_ANGLE') if hasattr(bpy.types, 'NodesModifier') and False else None
    try:
        bpy.context.view_layer.objects.active = ob; ob.select_set(True)
        bpy.ops.object.shade_smooth_by_angle(angle=math.radians(ang))
        ob.select_set(False)
    except Exception as e: print('smooth', e)

def box(name, size, loc, rot=(0, 0, 0), bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    ob = bpy.context.active_object; ob.name = name; ob.scale = size
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        m = ob.modifiers.new('bv', 'BEVEL'); m.width = bevel; m.segments = 3
        smooth(ob, 40)
    return ob

def sphere(name, r, loc):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=32, ring_count=16)
    ob = bpy.context.active_object; ob.name = name; bpy.ops.object.shade_smooth(); return ob

def cut(ob, cutter):
    m = ob.modifiers.new('cut', 'BOOLEAN'); m.operation = 'DIFFERENCE'; m.object = cutter
    try: m.solver = 'EXACT'
    except: pass
    cutter.hide_render = True; cutter.hide_viewport = True

def build(t):
    parts = []
    if t == 'p':
        prof = base(.30) + [(.165, .15), (.115, .33), (.175, .36), (.18, .38), (.11, .40)] + arc(.485, .115, -48, 90, 14)
        parts.append(lathe('pawn', prof))
    elif t == 'r':
        prof = base(.33) + [(.21, .15), (.18, .20), (.165, .66), (.185, .70), (.225, .73), (.225, .905), (.165, .905), (.165, .86), (0, .86)]
        ob = lathe('rook', prof); parts.append(ob)
        for i, a in enumerate((0, 60, 120)):
            cut(ob, box(f'c{i}', (.7, .065, .2), (0, 0, .96), (0, 0, math.radians(a))))
    elif t == 'b':
        prof = base(.31) + [(.175, .15), (.12, .41), (.20, .445), (.205, .47), (.13, .49), (.10, .51), (.13, .54), (.165, .60), (.17, .65), (.15, .70), (.11, .75), (.06, .785), (.03, .795)] + arc(.82, .03, -60, 90, 8)
        ob = lathe('bishop', prof); parts.append(ob)
        cut(ob, box('slit', (.32, .5, .03), (.09, 0, .70), (0, math.radians(-50), 0)))
    elif t == 'q':
        prof = base(.34) + [(.205, .15), (.13, .50), (.215, .545), (.215, .575), (.14, .60), (.15, .66), (.225, .80), (.205, .82), (.15, .825), (.09, .85), (.075, .87)] + arc(.905, .042, -50, 90, 8)
        parts.append(lathe('queen', prof))
        for i in range(9):
            a = math.tau*i/9
            parts.append(sphere(f'cr{i}', .036, (.205*math.cos(a), .205*math.sin(a), .825)))
    elif t == 'k':
        prof = base(.35) + [(.215, .15), (.14, .52), (.225, .565), (.225, .595), (.15, .62), (.16, .68), (.225, .78), (.21, .80), (.13, .81), (.10, .835), (0, .845)]
        parts.append(lathe('king', prof))
        parts.append(box('cv', (.06, .06, .2), (0, 0, .93), bevel=.012))
        parts.append(box('ch', (.16, .06, .055), (0, 0, .955), bevel=.012))
    elif t == 'n':
        prof = base(.33) + [(.225, .15), (.225, .19), (.16, .205), (0, .21)]
        parts.append(lathe('nbase', prof))
        P = [(.16, .19), (.19, .32), (.19, .45), (.165, .57), (.12, .67), (.075, .75), (.055, .80), (.045, .87), (.0, .80), (-.06, .77), (-.13, .715), (-.19, .65), (-.235, .585), (-.24, .555), (-.215, .53), (-.14, .525), (-.07, .50), (-.03, .46), (-.07, .40), (-.13, .32), (-.165, .25), (-.17, .19)]
        me = bpy.data.meshes.new('head'); bm = bmesh.new()
        vs = [bm.verts.new((x, -.085, z)) for x, z in P]
        f = bm.faces.new(vs)
        r = bmesh.ops.extrude_face_region(bm, geom=[f])
        for v in [e for e in r['geom'] if isinstance(e, bmesh.types.BMVert)]: v.co.y += .17
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new('head', me); bpy.context.collection.objects.link(ob)
        m = ob.modifiers.new('bv', 'BEVEL'); m.width = .045; m.segments = 5; m.limit_method = 'ANGLE'
        m2 = ob.modifiers.new('ss', 'SUBSURF'); m2.levels = 1; m2.render_levels = 2
        smooth(ob, 60); parts.append(ob)
        # mane ridge
        for i in range(6):
            u = i/5
            x = .17 - .12*u; z = .40 + .40*u
            parts.append(sphere(f'mn{i}', .04, (x, 0, z)))
        for sy in (-1, 1):
            e = sphere(f'eye{sy}', .022, (-.075, sy*.098, .70)); e['eye'] = True; parts.append(e)
        for ob in parts: ob.rotation_euler.z += math.radians(-28)
    return parts

def materials(color):
    def mat(name, rgb, rough, coat=.3):
        m = bpy.data.materials.new(name); m.use_nodes = True
        b = m.node_tree.nodes.get('Principled BSDF')
        b.inputs['Base Color'].default_value = (*rgb, 1)
        b.inputs['Roughness'].default_value = rough
        for k, v in (('Coat Weight', coat), ('Subsurface Weight', .08 if color == 'w' else 0), ('Specular IOR Level', .5)):
            if k in b.inputs: b.inputs[k].default_value = v
        return m
    if color == 'w':
        return mat('body', (0.80, 0.70, 0.54), .42), mat('eye', (0.08, 0.06, 0.1), .2)
    return mat('body', (0.022, 0.024, 0.06), .32, .6), mat('eye', (0.95, 0.9, 0.8), .2)

def scene():
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.samples = 96; sc.cycles.use_denoising = True
    sc.render.film_transparent = True
    sc.render.resolution_x, sc.render.resolution_y = W, H
    sc.view_settings.view_transform = 'Standard'
    sc.world = bpy.data.worlds.new('w'); sc.world.use_nodes = True
    bg = sc.world.node_tree.nodes['Background']; bg.inputs[0].default_value = (0.75, 0.8, 0.9, 1); bg.inputs[1].default_value = 0.55
    cam = bpy.data.cameras.new('cam'); cam.type = 'ORTHO'; cam.ortho_scale = 1.25
    co = bpy.data.objects.new('cam', cam); sc.collection.objects.link(co); sc.camera = co
    zt = 0.245/math.cos(ELEV); d = 10
    co.location = (0, -d*math.cos(ELEV), zt + d*math.sin(ELEV))
    co.rotation_euler = (math.pi/2 - ELEV, 0, 0)
    def light(name, typ, energy, loc, size=1.0, color=(1, 1, 1)):
        L = bpy.data.lights.new(name, typ); L.energy = energy; L.color = color
        if typ == 'AREA': L.size = size
        o = bpy.data.objects.new(name, L); sc.collection.objects.link(o); o.location = loc
        o.rotation_euler = (Vector((0, 0, .45)) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    light('key', 'AREA', 200, (-2.2, -2.6, 3.0), 2.2, (1, .97, .92))
    light('fill', 'AREA', 45, (2.6, -2.2, 1.4), 2.5, (.85, .9, 1))
    light('rim', 'AREA', 220, (1.2, 2.6, 2.2), 1.5, (1, 1, 1))

for t in 'pnbrqk':
    if ONLY and t not in ONLY: continue
    for c in 'wb':
        reset(); scene()
        parts = build(t)
        bpy.context.view_layer.update()
        top = 0
        for ob in parts:
            if ob.hide_render: continue
            dg = bpy.context.evaluated_depsgraph_get(); ev = ob.evaluated_get(dg)
            for v in ev.to_mesh().vertices: top = max(top, (ob.matrix_world @ v.co).z)
        s = KING_H*TARGET[t]/TARGET['k']/top
        body, eye = materials(c)
        for ob in [o for o in bpy.data.objects if o.type == 'MESH']:
            ob.scale = [x*s for x in ob.scale]; ob.location = Vector(ob.location)*s
        for ob in parts:
            if ob.type == 'MESH':
                ob.data.materials.clear(); ob.data.materials.append(eye if ob.get('eye') else body)
        bpy.context.scene.view_settings.exposure = -0.35 if c == 'w' else 0.0
        bpy.context.scene.render.filepath = os.path.join(OUT, f'{c}{t}.png')
        bpy.ops.render.render(write_still=True)
        print('done', c, t, round(top, 3))
