import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import socket

# Setup the plot
fig, axs = plt.subplots(4, 1, figsize=(10, 8))
fig.suptitle("Real-Time System Health Monitoring")

# Initialize lists to hold data for plotting
cpu_usage = []
memory_usage = []
disk_usage = []
net_sent = []
net_recv = []

# Initial network counters
net_io = psutil.net_io_counters()
prev_sent = net_io.bytes_sent
prev_recv = net_io.bytes_recv

def get_size(bytes):
    """Convert bytes to a human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024

def update(frame):
    global prev_sent, prev_recv

    # Update CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_usage.append(cpu_percent)
    if len(cpu_usage) > 60:
        cpu_usage.pop(0)
    axs[0].cla()
    axs[0].plot(cpu_usage, label=f'CPU Usage: {cpu_percent:.1f}%')
    axs[0].set_ylim(0, 100)
    axs[0].legend(loc='upper right')
    axs[0].set_title("CPU Usage (%)")
    axs[0].set_ylabel("Usage (%)")

    # Update Memory usage
    memory_info = psutil.virtual_memory()
    memory_usage.append(memory_info.percent)
    if len(memory_usage) > 60:
        memory_usage.pop(0)
    axs[1].cla()
    axs[1].plot(memory_usage, label=f'Memory Usage: {memory_info.percent:.1f}%',
                color='orange')
    axs[1].set_ylim(0, 100)
    axs[1].legend(loc='upper right')
    axs[1].set_title("Memory Usage (%)")
    axs[1].set_ylabel("Usage (%)")

    # Update Disk usage
    partitions = psutil.disk_partitions()
    if partitions:
        partition = partitions[0]
        partition_usage = psutil.disk_usage(partition.mountpoint)
        disk_usage.append(partition_usage.percent)
        if len(disk_usage) > 60:
            disk_usage.pop(0)
        axs[2].cla()
        axs[2].plot(disk_usage, label=f'Disk Usage: {partition_usage.percent:.1f}%',
                    color='green')
        axs[2].set_ylim(0, 100)
        axs[2].legend(loc='upper right')
        axs[2].set_title("Disk Usage (%)")
        axs[2].set_ylabel("Usage (%)")
    else:
        axs[2].cla()
        axs[2].set_title("Disk Usage (%)")
        axs[2].set_ylabel("Usage (%)")
        axs[2].text(0.5, 0.5, "No disk partition found", horizontalalignment='center',
                    verticalalignment='center', transform=axs[2].transAxes)

    # Update Network usage
    net_io = psutil.net_io_counters()
    net_sent.append(net_io.bytes_sent - prev_sent)
    net_recv.append(net_io.bytes_recv - prev_recv)
    prev_sent = net_io.bytes_sent
    prev_recv = net_io.bytes_recv
    if len(net_sent) > 60:
        net_sent.pop(0)
        net_recv.pop(0)
    axs[3].cla()
    axs[3].plot(net_sent, label=f'Bytes Sent: {get_size(net_sent[-1])}',
                color='red')
    axs[3].plot(net_recv, label=f'Bytes Received: {get_size(net_recv[-1])}',
                color='blue')
    axs[3].legend(loc='upper right')
    axs[3].set_title("Network Usage (Bytes per second)")
    axs[3].set_ylabel("Bytes")

    # Improve layout
    plt.subplots_adjust(hspace=0.5)

if __name__ == "__main__":
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"Hostname: {hostname}")
    print(f"IP Address: {ip_address}")
    print("="*40)

    ani = FuncAnimation(fig, update, interval=1000, cache_frame_data=False)
    plt.show()
