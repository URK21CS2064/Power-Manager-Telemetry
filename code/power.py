import psutil
import time
import csv
import logging
import multiprocessing

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def measure_system_performance(utilization_target, duration_seconds):
    start_time = time.time()
    end_time = start_time + duration_seconds
    performance_data = []

    with open('system_performance_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time (s)', 'CPU Utilization (%)', 'Memory Usage (%)', 'NIC Sent (bytes)', 'NIC Received (bytes)', 'Simulated Power Consumption (W)'])

        while time.time() < end_time:
            try:
                # Measure CPU and memory usage
                cpu_usage = psutil.cpu_percent(interval=1)
                memory_info = psutil.virtual_memory()
                memory_usage = memory_info.percent
                network_info = psutil.net_io_counters()
                bytes_sent = network_info.bytes_sent
                bytes_received = network_info.bytes_recv
                
                # Simulate power consumption
                simulated_power = (cpu_usage / 100.0) * 50  # Adjusted simulated power consumption

                # Write to CSV
                writer.writerow([
                    f"{time.time() - start_time:.2f}", 
                    f"{cpu_usage}", 
                    f"{memory_usage}", 
                    f"{bytes_sent}", 
                    f"{bytes_received}", 
                    f"{simulated_power}"
                ])

                # Collect data for analysis
                performance_data.append({
                    'cpu_usage': cpu_usage,
                    'memory_usage': memory_usage,
                    'bytes_sent': bytes_sent,
                    'bytes_received': bytes_received,
                    'simulated_power': simulated_power
                })

                # Log performance data
                logging.info(
                    f"Time: {time.time() - start_time:.2f}s | CPU Usage: {cpu_usage}% | Memory Usage: {memory_usage}% | NIC Sent: {bytes_sent} bytes | NIC Received: {bytes_received} bytes | Simulated Power: {simulated_power:.2f} W"
                )

                # Adjust sleep duration based on target utilization
                time.sleep((utilization_target / 100.0) - 1)  # Adjusted sleep to fit the utilization target

            except Exception as e:
                logging.error(f"Error: {str(e)}")

    # Calculate and log average performance metrics
    avg_power = sum(d['simulated_power'] for d in performance_data) / len(performance_data)
    avg_cpu = sum(d['cpu_usage'] for d in performance_data) / len(performance_data)
    avg_memory = sum(d['memory_usage'] for d in performance_data) / len(performance_data)
    avg_sent = sum(d['bytes_sent'] for d in performance_data) / len(performance_data)
    avg_received = sum(d['bytes_received'] for d in performance_data) / len(performance_data)

    logging.info(f"Average CPU Usage: {avg_cpu:.2f}%")
    logging.info(f"Average Memory Usage: {avg_memory:.2f}%")
    logging.info(f"Average NIC Sent: {avg_sent:.2f} bytes")
    logging.info(f"Average NIC Received: {avg_received:.2f} bytes")
    logging.info(f"Average Simulated Power Consumption: {avg_power:.2f} W")

def cpu_stress():
    while True:
        pass  # Infinite loop to generate CPU load

if __name__ == "__main__":
    # Get the number of CPU cores
    num_cores = multiprocessing.cpu_count()
    print(f"Starting load on {num_cores} cores.")
    
    # Start a process on each core to generate load
    processes = []
    for _ in range(num_cores):
        p = multiprocessing.Process(target=cpu_stress)
        p.start()
        processes.append(p)
    
    # Example usage: Measure system performance at 40% utilization for 60 seconds
    measure_system_performance(40, 60)
    
    # Keep generating load indefinitely
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Terminating CPU stress tests.")
        for p in processes:
            p.terminate()
        for p in processes:
            p.join()
