cwlVersion: v1.2
class: CommandLineTool

label: Prepare STAC assets
doc: Receive STAC item/catalog and dump the assets in output directory.

baseCommand: ["eoap-tools", "stac", "prepare-assets"]
arguments: ["--output", "_assets"]

hints:
  DockerRequirement:
    dockerPull: eoepca/eoap-tools:0.1.0
requirements:
  ResourceRequirement:
    coresMin: 1
    coresMax: 1
    ramMin: 512
    ramMax: 512

inputs:
  stac_item:
    type: Directory
    inputBinding:
      position: 1
outputs:
  assets_dir:
    type: Directory
    outputBinding:
      glob: "_assets"

s:softwareVersion: "0.1.0"
s:codeRepository: https://github.com/csgroup-oss/eoap-tools
s:license: https://spdx.org/licenses/Apache-2.0
s:copyrightHolder: "CS GROUP - FRANCE"

$namespaces:
  s: https://schema.org/
$schemas:
  - http://schema.org/version/latest/schemaorg-current-http.rdf
