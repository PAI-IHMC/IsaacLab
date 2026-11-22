* Fixed per-environment duplication of instanced visual geometry under the Fabric Scene Delegate on Kit 108 and
  later by re-enabling ``/app/usdrt/population/utils/mergeMaterials`` in the Isaac Lab Kit app files. Kit 108 changed
  its default to ``false``, so assets that bind an identical material in every environment were populated with a full
  copy of their visual meshes per environment.
