import bpy, bmesh, math, sys, os
from mathutils import Vector, Matrix

OUT = sys.argv[sys.argv.index('--')+1]
ONLY = sys.argv[sys.argv.index('--')+2] if len(sys.argv) > sys.argv.index('--')+2 else ''
os.makedirs(OUT, exist_ok=True)
ELEV = math.radians(24)
KING_H = 0.92
LINE = 1.0
LINECOL = (0.03, 0.03, 0.05)
# FIDE 장비 규정의 스탠턴 기물 키(cm): 킹 9.5 · 퀸 8.5 · 비숍 7 · 나이트 6 · 룩 5.5 · 폰 5
TARGET = {'p': 5.0, 'n': 6.0, 'b': 7.0, 'r': 5.5, 'q': 8.5, 'k': 9.5}
# 받침 지름(칸 너비 대비): 아이 눈에 잘 보이게 조금 통통하게, 룩은 낮고 넓은 성탑
BASE_D = {'p': .50, 'n': .54, 'b': .54, 'r': .56, 'q': .58, 'k': .60}
BASE_R = {'p': .30, 'n': .33, 'b': .31, 'r': .33, 'q': .34, 'k': .35}
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
        cut(ob, box('slit', (.32, .5, .03), (.09*math.cos(math.radians(-62)), .09*math.sin(math.radians(-62)), .70), (0, math.radians(-50), math.radians(-62))))
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

def srgb(h):
    c = [int(h[i:i+2], 16)/255 for i in (0, 2, 4)]
    return tuple(x/12.92 if x <= .04045 else ((x+.055)/1.055)**2.4 for x in c)

# 툰 재질: 빛의 양을 3단계 색으로 끊어 칠하고(하이라이트·반사 없음), 외곽선은 Freestyle로
def toon(name, cols, stops=(0.0, 0.30, 0.62)):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); dif = nt.nodes.new('ShaderNodeBsdfDiffuse')
    s2r = nt.nodes.new('ShaderNodeShaderToRGB'); ramp = nt.nodes.new('ShaderNodeValToRGB'); em = nt.nodes.new('ShaderNodeEmission')
    ramp.color_ramp.interpolation = 'CONSTANT'
    el = ramp.color_ramp.elements
    while len(el) < len(cols): el.new(0.5)
    for e, pos, c in zip(el, stops, cols): e.position = pos; e.color = (*srgb(c), 1)
    nt.links.new(dif.outputs[0], s2r.inputs[0]); nt.links.new(s2r.outputs[0], ramp.inputs[0])
    nt.links.new(ramp.outputs[0], em.inputs[0]); nt.links.new(em.outputs[0], out.inputs[0])
    return m

def materials(color):
    if color == 'w':
        return toon('body', ('c2b29a', 'ebe1cd', 'fffcf4')), toon('eye', ('1b1830', '1b1830', '2d2a3e'))
    return toon('body', ('15172b', '2b2e4f', '4b5080')), toon('eye', ('f4ecdc', 'f4ecdc', 'ffffff'))

def scene():
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_EEVEE'
    sc.render.use_freestyle = True; sc.render.line_thickness_mode = 'ABSOLUTE'; sc.render.line_thickness = LINE
    vl = sc.view_layers[0]; vl.use_freestyle = True; fs = vl.freestyle_settings; fs.crease_angle = math.radians(128)
    ls = fs.linesets[0] if fs.linesets else fs.linesets.new('L')
    ls.select_by_visibility = True; ls.select_by_edge_types = True
    ls.select_silhouette = True; ls.select_border = True; ls.select_crease = True; ls.select_external_contour = True
    if ls.linestyle is None: ls.linestyle = bpy.data.linestyles.new('LS')
    ls.linestyle.color = LINECOL; ls.linestyle.thickness = LINE
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
    sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 3.0; sun.angle = math.radians(3)
    so = bpy.data.objects.new('sun', sun); sc.collection.objects.link(so); so.rotation_euler = (math.radians(50), math.radians(-28), math.radians(-35))
    bg.inputs[1].default_value = 0.25

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
        s = KING_H*TARGET[t]/TARGET['k']/top; sxy = BASE_D[t]/2/BASE_R[t]
        body, eye = materials(c)
        for ob in [o for o in bpy.data.objects if o.type == 'MESH']:
            ob.scale = (ob.scale[0]*sxy, ob.scale[1]*sxy, ob.scale[2]*s); ob.location = Vector((ob.location[0]*sxy, ob.location[1]*sxy, ob.location[2]*s))
        for ob in parts:
            if ob.type == 'MESH':
                ob.data.materials.clear(); ob.data.materials.append(eye if ob.get('eye') else body)
        ls = bpy.context.scene.view_layers[0].freestyle_settings.linesets[0].linestyle
        ls.color = srgb('2d2a3e') if c == 'w' else srgb('07080f')
        bpy.context.scene.render.filepath = os.path.join(OUT, f'{c}{t}.png')
        bpy.ops.render.render(write_still=True)
        print('done', c, t, round(top, 3))
