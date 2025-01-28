import subprocess
import time
import os

def start_streamlit():
    # Start Streamlit app
    streamlit_process = subprocess.Popen(["streamlit", "run", "Login.py"])
    return streamlit_process

def start_data_collector():
    # Start DataCollector script
    data_collector_process = subprocess.Popen(["python", "DataCollector.py"])
    return data_collector_process

if __name__ == "__main__":
    # Start both services
    streamlit_process = start_streamlit()
    data_collector_process = start_data_collector()

    try:
        while True:
            # Check if processes are still running
            if streamlit_process.poll() is not None:
                print("Streamlit process has stopped. Restarting...")
                streamlit_process = start_streamlit()

            if data_collector_process.poll() is not None:
                print("DataCollector process has stopped. Restarting...")
                data_collector_process = start_data_collector()

            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopping services...")
        streamlit_process.terminate()
        data_collector_process.terminate()
        streamlit_process.wait()
        data_collector_process.wait()
        print("Services stopped.")