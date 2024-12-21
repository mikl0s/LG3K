
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import Progress

def run_with_progress(modules, config):
    total_logs = config.get("total_logs", 1000)
    split_size = config.get("split_size", 100)
    max_threads = config.get("max_threads", 4)

    num_files = (total_logs + split_size - 1) // split_size
    progress = Progress()

    with progress:
        task = progress.add_task("Generating logs", total=num_files)

        with ThreadPoolExecutor(max_threads) as executor:
            futures = []
            for module_name, generate_log in modules.items():
                for _ in range(num_files):
                    futures.append(
                        executor.submit(generate_log)
                    )

            for future in as_completed(futures):
                progress.advance(task)

                # Handle log result (e.g., save to file)
                log = future.result()
                print(log)  # Replace with actual file writing logic
