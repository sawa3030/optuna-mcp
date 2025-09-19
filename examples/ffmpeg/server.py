import re
import time
import traceback

import ffmpeg
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("FFmpeg")


@mcp.tool()
def run_ffmpeg(
    input_file: str, refs: int, qcomp: float, qdiff: int, me_range: int, x264opts: str
) -> str:
    """Run ffmpeg and returns the value of SSIM (Strucutural SIMilarity) and the elapsed time.

    Arguments:
    - input_file: Path to the input video file
    - refs: Number of reference frames (1-16)
    - qcomp: Quantizer compression (0.0-1.0)
    - qdiff: Max QP difference between frames (1-51)
    - me_range: Motion estimation range (4-64)
    - x264opts: FFmpeg x264 options string in the same format as FFmpeg command line
                (e.g. 'keyint=12:b-adapt=...')
    """
    start = time.time()
    try:
        enc = ffmpeg.input(
            input_file, t=50
        )  # Use only the first 50 seconds instead of the entire video for demo purposes.
        enc = enc.output(
            "-",
            f="null",
            tune="ssim",
            ssim=1,
            an=None,
            vcodec="libx264",
            s="320x240",
            vb="100k",
            refs=refs,
            qcomp=qcomp,
            qdiff=qdiff,
            me_range=me_range,
            x264opts=x264opts,
        )
        _, stderr = enc.run(capture_stderr=True)

        elapsed = time.time() - start
        ssim_mean = re.search("SSIM Mean Y:([0-9.]+)", stderr.decode("utf-8")).group(1)

        return f"SSIM (mean): {ssim_mean}, Elapsed: {elapsed} seconds"
    except Exception as e:
        stacktrace = "\n".join(traceback.format_tb(e.__traceback__))
        return f"Error: {e}, {traceback}: {traceback}"


if __name__ == "__main__":
    mcp.run()
