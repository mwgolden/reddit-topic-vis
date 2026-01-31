output "ingestion_completion_event" {
    description = "Event emitted when ingestion is complete"
    value = {
        name = aws_cloudwatch_event_rule.ingestion.name
        arn = aws_cloudwatch_event_rule.ingestion.arn
    }

}