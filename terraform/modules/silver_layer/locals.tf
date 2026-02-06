locals {
    lambda_events = {
     comments = var.event_source_config.comment_load_event
     posts =  var.event_source_config.post_load_event
    }
}