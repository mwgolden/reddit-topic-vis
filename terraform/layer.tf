resource "aws_lambda_layer_version" "project_dependencies" {
 layer_name =  "reddit_data_viz_project_dependencies"
 filename = "../build/reddit-data-dependencies.zip"
 source_code_hash = filebase64sha256("../build/reddit-data-dependencies.zip")
 compatible_runtimes = ["python3.12"]
 description = "Common dependencies for the reddit data visualiztion project [PyYaml]"
}