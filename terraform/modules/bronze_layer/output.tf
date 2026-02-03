output "bronze_comments_load_event" {
    description = "Event emitted when comments are loaded to bronze table"
    value = {
        name = aws_cloudwatch_event_rule.bronze_comments_load.name
        arn = aws_cloudwatch_event_rule.bronze_comments_load.arn
    }
}

output "bronze_posts_load_event" {
    description = "Event emitted when posts are loaded to bronze table"
    value = {
        name = aws_cloudwatch_event_rule.bronze_posts_load.name
        arn = aws_cloudwatch_event_rule.bronze_posts_load.arn
    }
}