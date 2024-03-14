# AI Chess player
# Nicholas Yukio Menezes Sugimoto
# 04 October 2023

import agent
import time

LOWER = 0 # Human (or AI under training)
UPPER = 1 # AI

agent_lower = agent.mind(LOWER)
start_time = time.time()
sc = agent_lower.minimax(5, -999999, +999999, LOWER, LOWER)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Eval: {sc}")
print(f"Elapsed time in seconds: {elapsed_time}")