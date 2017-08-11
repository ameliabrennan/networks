# Testing out capabilities of running CanvasDataCli calls from within Python
# Works but relies on secrets being within the user's system (sync requests will be rejected otherwise)
# Note sure why the table list arguments are not working (have used direct dump of all the files)

import subprocess, os
import canvas_schema_tools
import tools_for_lists

print("Testing Canvas API calls from within Python, will run the following commands...")

def run_canvas_sync():
  result = False
  try:
    sync_args = "canvasDataCli sync -c " + config_file_name
    print(sync_args)
    sync_result = subprocess.check_call(sync_args, shell=True)
    return(sync_result)
  except:
    return(result)

def run_canvas_unpack(table_name):
  result = False
  try:
    unpack_args = "canvasDataCli unpack -c " + config_file_name + " -f " + table_name
    unpack_result = subprocess.check_call(unpack_args, shell=True)    
    return(unpack_result)
  except:
    return(result)

####

skip_list = ['requests']

config_file_name = os.path.normpath("H:/CanvasData/") + os.path.normpath("/") + "config.js"

table_list = canvas_schema_tools.return_canvas_table_list()
table_list = tools_for_lists.remove_list_from_list(table_list, skip_list)

unpack_result = run_canvas_sync()

#unpack_args = "canvasDataCli unpack -c " + config_file_name + " -f " + "account_dim assignment_dim assignment_fact assignment_group_dim assignment_group_fact assignment_group_rule_dim assignment_override_dim assignment_override_fact assignment_override_user_dim assignment_override_user_fact assignment_override_user_rollup_fact assignment_rule_dim communication_channel_dim communication_channel_fact conversation_dim conversation_message_dim conversation_message_participant_fact course_dim course_section_dim course_ui_canvas_navigation_dim course_ui_navigation_item_dim course_ui_navigation_item_fact discussion_entry_dim discussion_entry_fact discussion_topic_dim discussion_topic_fact enrollment_dim enrollment_fact enrollment_rollup_dim enrollment_term_dim external_tool_activation_dim external_tool_activation_fact file_dim file_fact group_dim group_fact group_membership_dim group_membership_fact module_completion_requirement_dim module_completion_requirement_fact module_dim module_fact module_item_dim module_item_fact module_prerequisite_dim module_prerequisite_fact module_progression_dim module_progression_fact pseudonym_dim pseudonym_fact quiz_dim quiz_fact quiz_question_answer_dim quiz_question_answer_fact quiz_question_dim quiz_question_fact quiz_question_group_dim quiz_question_group_fact quiz_submission_dim quiz_submission_fact quiz_submission_historical_dim quiz_submission_historical_fact requests role_dim schema.json score_dim score_fact submission_comment_dim submission_comment_fact submission_comment_participant_dim submission_comment_participant_fact submission_dim submission_fact user_dim wiki_dim wiki_fact wiki_page_dim wiki_page_fact"
#unpack_result = subprocess.check_call(unpack_args, shell=True)
print("Successful unpacked list: ")
unpacked_table_list = []
for table_name in table_list:
  unpack_result = run_canvas_unpack(table_name)
  if (unpack_result != None):
    unpacked_table_list.append(table_name)

print(unpacked_table_list)