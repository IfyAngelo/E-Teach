# from fastapi import APIRouter, Depends, Request,  BackgroundTasks
# import socketio
# import socketio.exceptions
# from app.controllers import PSController
# from app.schemas.requests.poll_sensei import ChatPS, PSTests, PSProcessResponse, PSReport
# from core.cache import Cache

# from core.factory import Factory
# from core.sockets.socket_events import sio, endpoint_trigger

# et_lesson_plan = APIRouter()


# @et_lesson_plan.get("/variable/{survey_id}")
# async def create_variable(
#     survey_id: str,
#     ps_controller: PSController = Depends(Factory().get_poll_sensei_controller),
# ):
#     variable = await ps_controller.create_variable(survey_id=survey_id)
#     return variable


# @et_lesson_plan.post("/run-test")
# @Cache.cached(prefix="run-analysis", ttl=60)
# async def run_stats_test(
#     request: Request,
#     ps_run_analysis: PSTests,
#     background_task: BackgroundTasks,
#     ps_controller: PSController = Depends(Factory().get_poll_sensei_controller),
# ):
#     stats_test = await ps_controller.run_stats_test(
#         survey_id=ps_run_analysis.survey_id, data=ps_run_analysis.data, variable_id=ps_run_analysis.variable_id
#     )
#     # Retrieve the `conversation_id` for the survey_id

#     conversation_id = ps_run_analysis.conversation_id
#     user_id = ps_run_analysis.user_id
#     stats_test.update({"user_id": user_id, "conversation_id": conversation_id})
        
#     async def schedule_emit():
#         # Create a separate client to connect to the server
#         client_sio = socketio.Client()
#         try:
#             survey_id = stats_test.get("survey_id")
#             conversation_id = stats_test.get("conversation_id")
#             user_id = stats_test.get("user_id")
#             results = stats_test["test_results"]
#             descriptions = ""
#             for result in results:

#                 description = result["test_results"].get("description")
#                 if not description:
#                     description = ""
#                 descriptions += description + ", "
#             response = {
#                 "reply_text": descriptions,
#                 "actions": "",
#                 "data": {},
#                 "survey_id": survey_id,
#                 "conversation_id": conversation_id,
#                 "user_id": user_id
#             }
#             print("Connecting as client...")
#             client_sio.connect(f"https://ai-api-staging.pollsensei.ai?user_id={user_id}")  # Connect to self
#             print("Connected!")

#             # Send message to user_id room
#             client_sio.emit("endpoint_trigger", response,)
            
#         except socketio.exceptions.ConnectionError as e:
#             print(f"Error in client connection: {e}")
#             print(f"could not connect as client sending message from server, message:{response}")
#             await sio.emit("ai_message", response, to=user_id)

#         finally:
#             print("Disconnecting client...")
#             client_sio.disconnect()
#             print("Client disconnected.")

#     sio.start_background_task(schedule_emit)
#     #background_task.add_task(schedule_emit)
#     return stats_test