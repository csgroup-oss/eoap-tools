cwlVersion: v1.2
class: CommandLineTool

label: Generate STAC catalog
doc: Create STAC catalog from directory of files.

baseCommand: ["eoap-tools", "stac", "generate-catalog"]
arguments: ["--output", "_stac_catalog"]

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
  input_dir:
    type: Directory
    inputBinding:
      position: 1
outputs:
  stac_catalog:
    type: Directory
    outputBinding:
      glob: "_stac_catalog"

s:softwareVersion: "0.1.0"
s:codeRepository: https://github.com/csgroup-oss/eoap-tools
s:license: https://spdx.org/licenses/Apache-2.0
s:copyrightHolder: "CS GROUP - FRANCE"

$namespaces:
  s: https://schema.org/
$schemas:
  - http://schema.org/version/latest/schemaorg-current-http.rdf
