# Valid ASCII PLY 1.0 meshes and point clouds for Parsarium's ascii_ply cell.
#
# A file is a polygon mesh (vertex and face elements), a mesh with an extra
# edge element after the faces, or a point cloud (vertices only, with no face
# element or with "element face 0"). Each of these comes in six vertex
# layouts: x y z, then optional nx ny nz normals, then optional uchar
# red green blue (and alpha). The vertex layout and the presence of the face
# and edge elements are fixed per alternative, so the header always declares
# exactly the properties and elements the body holds.
#
# Counts and indices are `where` constraints that Fandango repairs directly:
# every element count equals the number of rows that follow, and every face
# and edge row is rewritten to distinct vertex indices below the vertex count.
# A face with more corners than the mesh has vertices is cut down to as many
# corners as there are vertices (never fewer than three).

def rows(node, prefix):
    if str(node.symbol).startswith(prefix):
        return 1
    return sum(rows(child, prefix) for child in node.children)

def dec(n):
    return str(n)

def vertices(start):
    return rows(start, '<vtx_')

# Distinct indices below n, taken in order from the generated ones.
def distinct(raw, n, k):
    used = []
    for value in raw[:k]:
        index = value % n
        while index in used:
            index = (index + 1) % n
        used.append(index)
    return used

def fit_face(face, start):
    tokens = [int(t) for t in str(face).split()]
    n = vertices(start)
    k = min(tokens[0], n)
    return ' '.join(str(v) for v in [k] + distinct(tokens[1:], n, k))

def fit_edge(edge, start):
    tokens = [int(t) for t in str(edge).split()]
    return ' '.join(str(v) for v in distinct(tokens, vertices(start), 2))

<start> ::= "ply\n" "format ascii 1.0\n" <meta>{0,3} <model>

# Grammar weights: plain mesh 19/24, mesh with an edge element 4/24, point
# cloud 1/24. Point clouds satisfy their constraints sooner, so Fandango's
# search keeps proportionally more of them than these weights give.
<model> ::= <surface> | <surface_more> | <other>
<surface_more> ::= <surface>
<other> ::= <edged> | <rare>
<rare> ::= <surface> | <rarer>
<rarer> ::= <surface> | <cloud>

<surface> ::= <s_p> | <s_pn> | <s_pc> | <s_pa> | <s_pnc> | <s_pna>
<edged> ::= <e_p> | <e_pn> | <e_pc> | <e_pa> | <e_pnc> | <e_pna>
<cloud> ::= <c_p> | <c_pn> | <c_pc> | <c_pa> | <c_pnc> | <c_pna>

<s_p> ::= <vhead> <xyz_props> <face_head> <end> <rows_p> <faces>
<s_pn> ::= <vhead> <xyz_props> <normal_props> <face_head> <end> <rows_pn> <faces>
<s_pc> ::= <vhead> <xyz_props> <rgb_props> <face_head> <end> <rows_pc> <faces>
<s_pa> ::= <vhead> <xyz_props> <rgba_props> <face_head> <end> <rows_pa> <faces>
<s_pnc> ::= <vhead> <xyz_props> <normal_props> <rgb_props> <face_head> <end> <rows_pnc> <faces>
<s_pna> ::= <vhead> <xyz_props> <normal_props> <rgba_props> <face_head> <end> <rows_pna> <faces>

<e_p> ::= <vhead> <xyz_props> <face_head> <edge_head> <end> <rows_p> <faces> <edges>
<e_pn> ::= <vhead> <xyz_props> <normal_props> <face_head> <edge_head> <end> <rows_pn> <faces> <edges>
<e_pc> ::= <vhead> <xyz_props> <rgb_props> <face_head> <edge_head> <end> <rows_pc> <faces> <edges>
<e_pa> ::= <vhead> <xyz_props> <rgba_props> <face_head> <edge_head> <end> <rows_pa> <faces> <edges>
<e_pnc> ::= <vhead> <xyz_props> <normal_props> <rgb_props> <face_head> <edge_head> <end> <rows_pnc> <faces> <edges>
<e_pna> ::= <vhead> <xyz_props> <normal_props> <rgba_props> <face_head> <edge_head> <end> <rows_pna> <faces> <edges>

<c_p> ::= <vhead> <xyz_props> <empty_faces>? <end> <rows_p>
<c_pn> ::= <vhead> <xyz_props> <normal_props> <empty_faces>? <end> <rows_pn>
<c_pc> ::= <vhead> <xyz_props> <rgb_props> <empty_faces>? <end> <rows_pc>
<c_pa> ::= <vhead> <xyz_props> <rgba_props> <empty_faces>? <end> <rows_pa>
<c_pnc> ::= <vhead> <xyz_props> <normal_props> <rgb_props> <empty_faces>? <end> <rows_pnc>
<c_pna> ::= <vhead> <xyz_props> <normal_props> <rgba_props> <empty_faces>? <end> <rows_pna>

# Header
<meta> ::= "comment " <words> "\n" | "obj_info " <words> "\n"
<words> ::= <word> (" " <word>){0,4}
<word> ::= r"[A-Za-z][a-z0-9]{0,7}"
<end> ::= "end_header\n"

<vhead> ::= "element vertex " <vertex_count> "\n"
<vertex_count> ::= r"[0-9]+"
<xyz_props> ::= "property float x\nproperty float y\nproperty float z\n" | "property double x\nproperty double y\nproperty double z\n"
<normal_props> ::= "property float nx\nproperty float ny\nproperty float nz\n"
<rgb_props> ::= "property uchar red\nproperty uchar green\nproperty uchar blue\n"
<rgba_props> ::= <rgb_props> "property uchar alpha\n"

<face_head> ::= "element face " <face_count> "\n" <face_prop>
<empty_faces> ::= "element face 0\n" <face_prop>
<face_count> ::= r"[0-9]+"
<face_prop> ::= "property list " <count_type> " " <index_type> " " <index_name> "\n"
<count_type> ::= "uchar" | <other_count_type>
<other_count_type> ::= "int" | "uint"
<index_type> ::= "int" | "uint" | <other_index_type>
<other_index_type> ::= "int" | "uchar"
<index_name> ::= "vertex_indices" | "vertex_index"

<edge_head> ::= "element edge " <edge_count> "\n" "property int vertex1\nproperty int vertex2\n"
<edge_count> ::= r"[0-9]+"

# Body: 3 to 60 vertices, 1 to 60 faces, 1 to 20 edges
<rows_p> ::= <vtx_p>{3,60}
<rows_pn> ::= <vtx_pn>{3,60}
<rows_pc> ::= <vtx_pc>{3,60}
<rows_pa> ::= <vtx_pa>{3,60}
<rows_pnc> ::= <vtx_pnc>{3,60}
<rows_pna> ::= <vtx_pna>{3,60}
<vtx_p> ::= <xyz> "\n"
<vtx_pn> ::= <xyz> " " <normal> "\n"
<vtx_pc> ::= <xyz> " " <rgb> "\n"
<vtx_pa> ::= <xyz> " " <rgb> " " <u8> "\n"
<vtx_pnc> ::= <xyz> " " <normal> " " <rgb> "\n"
<vtx_pna> ::= <xyz> " " <normal> " " <rgb> " " <u8> "\n"

<xyz> ::= <coord> " " <coord> " " <coord>
<coord> ::= "-"? <magnitude>
<magnitude> ::= r"[0-9]" | r"[1-9][0-9]" | r"[0-9]\.[0-9]{1,4}" | r"[1-9][0-9]\.[0-9]{1,3}"
<normal> ::= <unit> " " <unit> " " <unit>
<unit> ::= "-"? ("0" | "1" | r"0\.[0-9]{1,4}" | "1.0")
<rgb> ::= <u8> " " <u8> " " <u8>
<u8> ::= "0" | r"[1-9][0-9]?" | r"1[0-9][0-9]" | r"2[0-4][0-9]" | r"25[0-5]"

<faces> ::= <face_row>{1,60}
<face_row> ::= <face> "\n"
<face> ::= <triangle> | <quad> | <other_face>
<other_face> ::= <triangle> | <quad> | <pentagon> | <hexagon>
<triangle> ::= "3" (" " <raw_index>){3}
<quad> ::= "4" (" " <raw_index>){4}
<pentagon> ::= "5" (" " <raw_index>){5}
<hexagon> ::= "6" (" " <raw_index>){6}
<raw_index> ::= "0" | r"[1-9][0-9]?"

<edges> ::= <edge_row>{1,20}
<edge_row> ::= <edge> "\n"
<edge> ::= <raw_index> " " <raw_index>

where forall <v> in <vertex_count>: <v> == dec(vertices(<start>))
where forall <f> in <face_count>: <f> == dec(rows(<start>, '<face_row>'))
where forall <e> in <edge_count>: <e> == dec(rows(<start>, '<edge_row>'))
where forall <f> in <face_row>: <f>.<face> == fit_face(<f>.<face>, <start>)
where forall <e> in <edge_row>: <e>.<edge> == fit_edge(<e>.<edge>, <start>)
