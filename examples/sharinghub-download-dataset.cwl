cwlVersion: v1.2
class: CommandLineTool

label: Download SharingHub dataset
doc: Clone SharingHub dataset repository and configure DVC.

baseCommand: ["eoap-tools", "sharinghub", "download-dataset"]
arguments: ["--output", "_dataset"]

hints:
  DockerRequirement:
    dockerPull: eoepca/eoap-tools:0.1.0
requirements:
  EnvVarRequirement:
    envDef:
      DVC_SITE_CACHE_DIR: /tmp/dvc
      EOAP_TOOLS__ACCESS_TOKEN: $( inputs.access_token )
      EOAP_TOOLS__ACCESS_KEY_ID: $( inputs.access_key_id )
      EOAP_TOOLS__SECRET_ACCESS_KEY: $( inputs.secret_access_key )
  NetworkAccess:
    networkAccess: true
  ResourceRequirement:
    coresMin: 1
    coresMax: 4
    ramMin: 1024
    ramMax: 2048

inputs:
  url:
    type: string
    doc: Repository URL of the dataset to download.
    inputBinding:
      position: 1
  version:
    type: string?
    doc: Version of the dataset (Git revision).
    inputBinding:
      prefix: --version
  pull:
    type: boolean
    doc: Pull with DVC.
    default: false
    inputBinding:
      prefix: --pull
  user:
    type: string?
    doc: Username used to download the repository.
    inputBinding:
      prefix: --user
  access_token:
    type: string?
    doc: Access token used to download the repository.
    default: ""
  access_key_id:
    type: string?
    doc: Access Key ID for DVC S3 configuration.
    default: ""
  secret_access_key:
    type: string?
    doc: Secret Access Key for DVC S3 configuration.
    default: ""
outputs:
  output_dataset:
    type: Directory
    outputBinding:
      glob: "_dataset"

s:softwareVersion: "0.1.0"
s:codeRepository: https://github.com/csgroup-oss/eoap-tools
s:license: https://spdx.org/licenses/Apache-2.0
s:copyrightHolder: "CS GROUP - FRANCE"

$namespaces:
  s: https://schema.org/
$schemas:
  - http://schema.org/version/latest/schemaorg-current-http.rdf
