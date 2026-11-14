#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <loaders/include/bkp_loaders.h>
#include <system/include/bkp_log.h>
#include <math/include/bkp_vertex_geometries.h>

/* Capture the geometry passed to the GPU upload boundary. Parsing stays in
 * upstream bkp_loader_ply.c; this harness makes a graphics device unnecessary. */
static size_t observed_vertices, observed_indices;
static BkpVec3 *observed_positions;
static uint32_t *observed_face;

BkpBool bkpMakeMeshBufferEx(BkpGpuAdapter adapter, size_t vertexCount,
  BkpVec3 *positions, BkpVec3 *normals, BkpVec3 *UVs, BkpVec3 *tangents,
  BkpVec4 *colors, size_t indiceCount, uint32_t *indices, uint16_t *indices16,
  BkpVertexGeometryInfo *geoInfo, size_t scratchGroupId, int recomputeNormals) {
  (void)adapter; (void)normals; (void)UVs; (void)tangents; (void)colors;
  (void)geoInfo; (void)scratchGroupId; (void)recomputeNormals;
  observed_vertices = vertexCount;
  observed_indices = indiceCount;
  observed_positions = malloc(vertexCount * sizeof(*observed_positions));
  observed_face = malloc(indiceCount * sizeof(*observed_face));
  if ((!observed_positions && vertexCount) || (!observed_face && indiceCount)) return BKP_FALSE;
  memcpy(observed_positions, positions, vertexCount * sizeof(*observed_positions));
  for (size_t i = 0; i < indiceCount; ++i)
    observed_face[i] = indices ? indices[i] : indices16[i];
  return BKP_TRUE;
}

void bkp_modelPushMesh(BkpModel *model, BkpModelMesh *mesh) {
  model->meshes = realloc(model->meshes, sizeof(*mesh) * (model->meshCount + 1));
  model->meshes[model->meshCount++] = *mesh;
}
BkpNode *bkp_modelNodeSlot(BkpModel *model) {
  model->nodes = realloc(model->nodes, sizeof(*model->nodes) * (model->nodeCount + 1));
  return &model->nodes[model->nodeCount++];
}
BkpTangentBitangent bkpCalculateTangent(BkpVec3 *p1, BkpVec3 *p2, BkpVec3 *p3,
  BkpVec3 *uv1, BkpVec3 *uv2, BkpVec3 *uv3) {
  (void)p1; (void)p2; (void)p3; (void)uv1; (void)uv2; (void)uv3;
  BkpTangentBitangent result = {0}; return result;
}
void bkp_log(int level, const char *tag, const char *colors, const char *fName,
  const char *funcName, int fLine, const char *message, ...) {
  (void)level; (void)tag; (void)colors; (void)fName; (void)funcName;
  (void)fLine; (void)message;
}
int main(int argc, char **argv) {
  if (argc != 2) return 2;
  BkpModel model = {0};
  if (!bkpLoadPly(NULL, argv[1], &model, 0)) return 1;
  if (observed_vertices < 2 || observed_indices < 3 || model.meshCount == 0) return 1;
  printf("{\"vertices\":%zu,\"indices\":%zu,\"meshes\":%u,\"face\":[%u,%u,%u],\"second_x\":%.1f}\n",
    observed_vertices, observed_indices, model.meshCount,
    observed_face[0], observed_face[1], observed_face[2], observed_positions[1].x);
  free(observed_positions); free(observed_face);
  free(model.meshes); free(model.nodes); free(model.rootNodes);
  return 0;
}
