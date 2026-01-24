variable "api_token_cache_tables" {
  type = object({
    api_config_table = string,
    api_token_cache_table = string
  })
}