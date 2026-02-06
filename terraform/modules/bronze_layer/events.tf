resource "aws_cloudwatch_event_rule" "bronze_comments_load" {
  name = "reddit-bronze-comments-load-complete"
  description = "Capture Reddit bronze comments load"
  event_pattern = jsonencode({
  "source": ["reddit.bronze"],
  "detail": {
    "table": ["comments"]
  }
})
}

resource "aws_cloudwatch_event_rule" "bronze_posts_load" {
  name = "reddit-bronze-posts-load-complete"
  description = "Capture Reddit bronze posts load"
  event_pattern = jsonencode({
  "source": ["reddit.bronze"],
  "detail": {
    "table": ["posts"]
  }
})
}