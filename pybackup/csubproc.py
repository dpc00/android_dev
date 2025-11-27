"""Module for continuous subprocess management.
modified by phil.
"""
import json
import subprocess
import types
from collections import deque
from collections.abc import Generator
from queue import Empty, Queue
from threading import Thread
from typing import IO, AnyStr

# logger = logging.getLogger(__name__)

Qi1 = types.new_class("Qi1", bases=(str,))
Qi2 = types.new_class("Qi2", bases=(str,))


class ContinuousSubprocess:
    """Creates a process to execute a wanted command and
    yields a continuous output stream for consumption.
    """

    def __init__(self, command_string: str) -> None:
        """Constructor.

        :param command_string: A command to execute in a separate process.
        """
        self.__command_string = command_string
        self.__process: subprocess.Popen | None = None

    @property
    def command_string(self) -> str:
        """Property for command string.

        :return: Command string.
        """
        return self.__command_string

    def terminate(self) -> None:
        if not self.__process:
            raise ValueError("Process is not running.")

        self.__process.terminate()

    def execute(
        self,
        shell: bool = True,
        path: str | None = None,
        max_error_trace_lines: int = 1000,
        *args,
        **kwargs,
    ) -> Generator[str, None, None]:
        """Executes a command and yields a continuous output from the process.

        :param shell: Boolean value to specify whether to
        execute command in a new shell.
        :param path: Path where the command should be executed.
        :param max_error_trace_lines: Maximum lines to return in case of an error.
        :param args: Other arguments.
        :param kwargs: Other named arguments.

        :return: A generator which yields output strings from an opened process.
        """
        # Check if the process is already running
        # (if it's set, then it means it is running).
        if self.__process:
            raise RuntimeError(
                "Process is already running. "
                "To run multiple processes initialize a second object."
            )

        with subprocess.Popen(
            self.__command_string,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=shell,
            cwd=path,
            *args,
            **kwargs,
            bufsize=1,
        ) as process:
            # Indicate that the process has started and is now running.
            self.__process = process

            # Initialize a mutual queue that will hold stdout and stderr messages.
            q1 = Queue()
            q2 = Queue()
            # Initialize a limited queue to hold last N of lines.
            dq = deque(maxlen=max_error_trace_lines)

            # Create a parallel thread that will read stdout stream.
            stdout_thread = Thread(
                target=ContinuousSubprocess.__read_stream, args=[process.stdout, q1]
            )
            stdout_thread.start()

            # Create a parallel thread that will read stderr stream.
            stderr_thread = Thread(
                target=ContinuousSubprocess.__read_stream, args=[process.stderr, q2]
            )
            stderr_thread.start()

            # logger.info(
            #    "Successfully started threads to capture stdout and stderr streams."
            # )

            while process.poll() is None:
                while not q1.empty():
                    try:
                        item = q1.get(False)
                        dq.append(item)
                        yield Qi1(item)
                    except Empty:
                        pass

                while not q2.empty():
                    try:
                        item = q2.get(False)
                        dq.append(item)
                        yield Qi2(item)
                    except Empty:
                        pass

            # Close streams.
            process.stdout.close()
            process.stderr.close()

            return_code = process.wait()

        # Make sure both threads have finished.
        stdout_thread.join()
        if stdout_thread.is_alive():
            raise RuntimeError("Stdout thread is still alive!")

        stderr_thread.join()
        if stderr_thread.is_alive():
            raise RuntimeError("Stderr thread is still alive!")

        # Indicate that the process has finished as is no longer running.
        self.__process = None

        if return_code:
            error_trace = list(dq)
            raise subprocess.CalledProcessError(
                returncode=return_code,
                cmd=self.__command_string,
                output=json.dumps(
                    {
                        "message": "An error has occurred while running the specified command.",
                        "trace": error_trace,
                        "trace_size": len(error_trace),
                        "max_trace_size": max_error_trace_lines,
                    }
                ),
            )

    @staticmethod
    def __read_stream(stream: IO[AnyStr], queue: Queue):
        try:
            for line in iter(stream.readline, ""):
                if line != "":
                    queue.put(line)
                else:
                    break
        # It is possible to receive: ValueError: I/O operation on closed file.
        except ValueError:
            # logger.exception("Got error while reading from a process stream.")
            pass
