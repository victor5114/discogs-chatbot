data "aws_lambda_function" "discogs_bot_command_dispatcher" {
  function_name = "discogs-bot-DispatcherFunction-1861LSSDUN7MY"
}

data "aws_iam_role" "discogs_bot_command_dispatcher_role" {
  name = "discogs-bot-DispatcherFunctionRole-JL2YJOQT7WEC"
}



# data "aws_lambda_function" "discogs_bot_search_release" {
#   function_name = "discogs_bot-HelloWorldFunction-18HUPKDM9A5LO"
# }

# data "aws_lambda_function" "discogs_bot_add_to_wantlist" {
#   function_name = "discogs_bot-HelloWorldFunction-18HUPKDM9A5LO"
# }
