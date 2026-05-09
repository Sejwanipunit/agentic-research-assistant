import subprocess
import sys
import tempfile
import os
from langchain_core.tools import tool

@tool
def code_executor(code: str) -> str:
    """
    Execute Python code and return the output.
    Use this when you need to perform calculations, data processing,
    demonstrate code examples, or verify logic programmatically.
    
    Args:
        code: Valid Python code to execute
        
    Returns:
        stdout output of the code, or error message if execution fails
    """
    
    try:
        #Use a temporary file to safely execute the code.
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            delete=False
        ) as f:
            f.write(code)
            temp_path = f.name
            
        # Run the temp file in a subprocess with a timeout
        result =  subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=10,
            env={
                **os.environ,
                "PYTHONDONTWRITEBYTECODE": "1"
            }
        )
        
        #clear the temp file
        os.unlink(temp_path)
        
        #Return stdout if successful, else return stderr
        if result.returncode == 0:
            output = result.stdout.strip()
            return output if output else "Code executed successfully with no output."
        else:
            return f"Error executing code: {result.stderr.strip()}"
        
    except subprocess.TimeoutExpired:
        return "Error: Code execution timed out."
    except Exception as e:
        return f"Unexpected error during code execution: {str(e)}"