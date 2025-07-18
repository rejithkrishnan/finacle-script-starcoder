from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.server.server import run_server

# --- Server Configuration ---

# 1. Define the arguments for the vLLM engine
# This points to the local folder containing your merged model.
engine_args = AsyncEngineArgs(model='./merged-finacle-model') 

# 2. Create the asynchronous LLM engine
engine = AsyncLLMEngine.from_engine_args(engine_args)

# 3. Run the server
# This starts a web server compatible with the OpenAI API on http://localhost:8000
run_server(
    engine=engine,
    host='127.0.0.1',
    port=8000,
    log_level='info',
    # We don't need these extra endpoints for our use case
    disable_log_stats=True, 
    disable_log_requests=True
)