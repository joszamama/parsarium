# Small valid ASCII PLY 1.0 meshes for Parsarium's ascii_ply cell.
# Header and body are coupled structurally: each branch fixes the vertex
# count, vertex properties, face count and face indices together.

<start> ::= "ply\n" "format ascii 1.0\n" <comment>{0,2} <mesh>

<comment> ::= "comment " <comment_text> "\n"
<comment_text> ::= "Parsarium Fandango ASCII PLY" | "generated mesh" | "units metres"

<mesh> ::= <triangle_xyz> | <triangle_rgb> | <quad_xyz> | <quad_rgb>

# One triangle over three vertices.
<triangle_xyz> ::= "element vertex 3\n" <xyz_props> "element face 1\n" <face_prop> "end_header\n" \
                   <vertex_xyz>{3} <triangle_face>
<triangle_rgb> ::= "element vertex 3\n" <xyz_props> <rgb_props> "element face 1\n" <face_prop> "end_header\n" \
                   <vertex_rgb>{3} <triangle_face>

# A quad split into two triangles over four vertices.
<quad_xyz> ::= "element vertex 4\n" <xyz_props> "element face 2\n" <face_prop> "end_header\n" \
               <vertex_xyz>{4} <quad_faces>
<quad_rgb> ::= "element vertex 4\n" <xyz_props> <rgb_props> "element face 2\n" <face_prop> "end_header\n" \
               <vertex_rgb>{4} <quad_faces>

<xyz_props> ::= "property float x\n" "property float y\n" "property float z\n"
<rgb_props> ::= "property uchar red\n" "property uchar green\n" "property uchar blue\n"
<face_prop> ::= "property list uchar " <index_type> " vertex_indices\n"
<index_type> ::= "int" | "uint"

<vertex_xyz> ::= <coord> " " <coord> " " <coord> "\n"
<vertex_rgb> ::= <coord> " " <coord> " " <coord> " " <u8> " " <u8> " " <u8> "\n"
<coord> ::= "0" | "1" | "-1" | "0.5" | "-0.5" | "1.25" | "2.0"
<u8> ::= "0" | "64" | "128" | "255"

<triangle_face> ::= "3 0 1 2\n" | "3 1 2 0\n" | "3 2 0 1\n"
<quad_faces> ::= "3 0 1 2\n3 0 2 3\n" | "3 0 1 3\n3 1 2 3\n"
