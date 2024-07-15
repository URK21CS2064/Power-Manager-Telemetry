# Power Management Tool

In the era of 5G and edge computing, the deployment of devices across various locations has led to a significant increase in power consumption. This rise emphasizes the urgent need for corporations and governments worldwide to implement strategies for achieving net-zero power consumption. Furthermore, with electricity prices on the rise, understanding and managing the total power drawn by systems is becoming increasingly crucial for both economic and environmental reasons.

## Project Objectives

This project aims to address the challenges of power management by focusing on the following objectives:

1. **Research Open-Source Tools**: Identify and evaluate available open-source tools that can be utilized for accurate power measurement.
2. **Document System Knobs**: Catalog the various configurable parameters within a system that can influence power consumption metrics.
3. **Telemetry Data Collection**: Gather telemetry data from key components such as the CPU, memory, Network Interface Card (NIC), and Thermal Design Power (TDP).
4. **Power Utilization Measurement**: Measure and record system power utilization, focusing specifically on CPU, NIC, and TDP based on varying input parameters related to system utilization percentages.

## Team Member
Sarvesh Kumar R

## College Mentor
Basil Xavier

## Key Features

1. **CPU Metrics Monitoring**: The tool offers real-time monitoring of CPU utilization, allowing users to see usage percentages for each individual core. Additionally, it visualizes C-states, which represent various levels of CPU idle modes, helping to identify opportunities for energy savings.

   ![CPU Metric Plots](images/cpu.png)
   <div align="center">CPU Metric Plots</div>

2. **Memory Usage Insights**: The application tracks system RAM usage, providing information on memory currently in use versus available memory. This helps users pinpoint memory-intensive applications and assess potential bottlenecks. Disk usage statistics are also monitored for better data management.

   ![Memory Usage Plots](images/memory.png)
   <div align="center">Memory Usage Plots</div>

3. **Temperature and Power Mode Switching**: The tool continuously monitors the temperatures of critical components (CPU, GPU, etc.) to ensure they remain within safe operational limits. Users can switch between various power modes (performance, balanced, power-saving) based on their current needs, optimizing power consumption effectively.

   ![Temperature Plots](images/temp.png)
   <div align="center">Temperature Plots</div>

4. **Battery and NIC Power Consumption**: Detailed battery statistics (percentage, time remaining, power state) allow users to manage battery usage more effectively. Monitoring NIC power consumption provides insights into the energy impact of network activities.

   ![Battery Usage Plots](images/battery.png)
   <div align="center">Battery Usage Plots</div>

5. **GPU Metrics Tracking**: The tool also tracks various GPU metrics, including power consumption, supply voltage, and temperature, giving users insights into the power efficiency of their graphics-related tasks.

   ![GPU Metric Plots](images/gpu.png)
   <div align="center">GPU Metric Plots</div>

## Docker Integration

Utilizing Docker for containerization ensures a consistent and portable environment for running the Python GUI application. This approach helps mitigate dependency issues and eases deployment across different systems.

### Steps to Use Docker

1. **Create a Dockerfile**: This file describes the necessary environment for running your application.
2. **Build the Docker Image**: Use the Dockerfile to create an image that encapsulates your application and its dependencies.
3. **Run the Container**: Start a container from your image, specifying parameters such as CPU loading percentage and the duration of the test.

## Installation Steps

1. **Install System Dependencies**:
   - Download the `install_dependencies.sh` script from the repository and execute the following commands in your terminal:
     ```bash
     chmod +x install_dependencies.sh
     ./install_dependencies.sh
     ```

2. **Install Docker**:
   - Download the `Step1-install_docker.sh` script and run:
     ```bash
     chmod +x Step1-install_docker.sh
     ./Step1-install_docker.sh
     ```

3. **Create Dockerfile**:
   - Create a Dockerfile using the command:
     ```bash
     vi Dockerfile
     ```
   - Copy the contents from `Step2-Create Dockerfile` into your new Dockerfile.

4. **Download Application Code**:
   - Access the `GUI_code` folder in the repository, download the files, and execute the application.

```python
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
Tools Utilized
The Power Management Tool leverages several powerful libraries and tools to present accurate real-time data through intuitive visualizations:

psutil: A cross-platform library for retrieving information on running processes and system utilization metrics, including CPU, memory, and disk.
tkinter: The standard GUI toolkit for Python, which provides the components necessary for creating interactive applications.
turbostat: A command-line tool that reports processor





## Tools Utilized

The Power Management Tool leverages several powerful libraries and tools to present accurate real-time data through intuitive visualizations:

- **psutil**: A cross-platform library for retrieving information on running processes and system utilization metrics, including CPU, memory, and disk.
- **tkinter**: The standard GUI toolkit for Python, which provides the components necessary for creating interactive applications.
- **turbostat**: A command-line tool that reports processor frequency and power statistics, offering insights into CPU performance.
- **Docker**: A platform for developing and deploying applications in isolated containers, ensuring consistency across different environments.
- **matplotlib**: A versatile plotting library for creating a wide range of visualizations, from static graphs to interactive charts.
- **lm-sensors**: A suite of tools for monitoring hardware sensor data, useful for temperature and fan speed monitoring.
- **upower**: A daemon that provides information about power devices and manages power-related operations.

## Conclusion

The Power Management Tool is designed to empower users with real-time insights into system performance and energy consumption. By leveraging detailed monitoring capabilities, users can optimize their systems for efficiency and sustainability. This tool not only aids individual users in managing power consumption but also contributes to broader eco-friendly practices in computing.

Explore the repository for more detailed information and usage instructions, and start optimizing your system today!
