resource "aws_cloudwatch_event_rule" "ingestion" {
  name = "reddit-ingestion-complete"
  description = "Capture Reddit download completion events"
  event_pattern = jsonencode({
    "source": ["reddit.ingestion"]
  })
}