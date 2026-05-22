from typing import TypedDict
from mcp.server.fastmcp import FastMCP, Context

# Create the MCP server
mcp = FastMCP("MCP Demo")


# ---------- Structured output for one of our tools ----------
class TrainingEstimate(TypedDict):
    dataset_size_gb: float
    gpu_type: str
    estimated_hours: float
    recommendation: str


# ---------- TOOL 1 ----------
@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


# ---------- TOOL 2 ----------
@mcp.tool()
async def estimate_training_time(
    dataset_size_gb: float,
    gpu_type: str,
    ctx: Context
) -> TrainingEstimate:
    """Estimate model training time based on dataset size and GPU type."""
    await ctx.info(f"Estimating training time for {dataset_size_gb} GB on {gpu_type}")

    gpu = gpu_type.strip().upper()

    if gpu == "A100":
        speed_factor = 2.0
        recommendation = "Good choice for large-scale training."
    elif gpu == "V100":
        speed_factor = 1.2
        recommendation = "Reasonable, but slower than A100."
    else:
        speed_factor = 0.7
        recommendation = "Consider a stronger GPU for faster iteration."

    estimated_hours = dataset_size_gb / speed_factor

    return {
        "dataset_size_gb": dataset_size_gb,
        "gpu_type": gpu,
        "estimated_hours": round(estimated_hours, 2),
        "recommendation": recommendation,
    }


# ---------- RESOURCE ----------
@mcp.resource("info://gpu-guide")
def gpu_guide() -> str:
    """Basic GPU guidance for ML workloads."""
    return (
        "A100 GPUs are generally preferred for large deep learning workloads. "
        "V100 is still useful, while lower-end GPUs may slow experimentation."
    )


# ---------- PROMPT ----------
@mcp.prompt(title="ML Status Summary")
def summarize_training_plan(model_name: str, gpu_type: str) -> str:
    """Reusable prompt template for summarizing a training plan."""
    return f"""
Write a concise project update for training model '{model_name}' on GPU type '{gpu_type}'.

Include:
- expected training setup
- likely bottlenecks
- one optimization recommendation
""".strip()


if __name__ == "__main__":
    # For local desktop-style integration use stdio:
    mcp.run(transport="stdio")