from tasks.task import BaseTask
from typing import Any, List
from e2epyppg.e2e_ppg_pipeline import e2e_hrv_extraction
import pandas as pd
import numpy as np
import os

# from datetime import datetime


class PPGHRExtraction(BaseTask):
    """
    **Description:**

            This task extracts heart rate (HR) from PPG signal for a specific patient. 
            It utilizes an end-to-end PPG processing pipeline (`e2e_ppg_pipeline`) for HR extraction. 
            It returns an array of json objects in string format, each containing HR and corresponding timestamps extracted from the PPG signal.
            If the signal is too noisy it returns a message in string format indicating that HR cannot be extracted reliably. 

    """
    name: str = "ppg_hr_extraction"
    chat_name: str = "PPGHrExtraction"
    description: str = (
        "When a request for extracting heart rate (HR) from PPG signal for a specific patient is received, "
        "call this analysis tool. This tool is specifically designed to load PPG signal, extract HR from PPG signal using an end to end processing pipeline, and return the results. "
        "It returns an array of json objects in string format, each containing HR and corresponding timestamp extracted from the PPG signal. "
        "If the signal is too noisy it returns a message in string format for user indicating that the signal is too noisy and HR cannot be extracted reliably!"
    )
    dependencies: List[str] = []
    inputs: List[str] = ["User ID in string. It can be refered as user, patient, individual, participant, etc. Start with 'par_' following with a number (e.g., 'par_1').",
                         "Date and time of the data in string with the following format: `%Y%m%d%H%M`"]
    outputs: List[str] = ["Returns an array of json objects in string format, each containing HR and corresponding timestamp extracted from the PPG signal, "
                           "or a message in string format for user indicating that the signal is too noisy, and HR cannot be extracted reliably"]

    output_type: bool = False
    # False if planner should continue. True if after this task the planning should be
    # on pause or stop. examples are when you have a task that asks user to provide more information
    return_direct: bool = False

    # file_name: str = "ppg.csv"
    local_dir: str = "data/"
    columns_to_keep: List[str] = [
        "ppg",
        "shiftedTime"
    ]




    def _get_data(
        self,
        local_dir: str,
        file_name: str,
        usecols: List[str] = None,
    ) -> pd.DataFrame:
        # Construct the full file path
        local_dir = os.path.join(os.getcwd(), local_dir)
        file_path = os.path.join(local_dir, file_name)

        # Determine the delimiter by reading a single line
        try:
            with open(file_path, 'r') as f:
                first_line = f.readline()
                delimiter = ',' if ',' in first_line else ' '  # Determine if comma or space delimiter
        except FileNotFoundError as e:
            # Return an empty DataFrame if the file is not found
            print(f"File not found: {e}")
            return pd.DataFrame(columns=usecols if usecols else None)
        except Exception as e:
            # Catch other unexpected errors and return an empty DataFrame
            print(f"Error reading file: {e}")
            return pd.DataFrame(columns=usecols if usecols else None)


         # Read the file into a DataFrame with the identified delimiter
        try:
            if usecols:
                df = pd.read_csv(file_path, usecols=usecols, delim_whitespace=(delimiter == ' '))
            else:
                df = pd.read_csv(file_path, delim_whitespace=(delimiter == ' '))
        except Exception as e:
            # Handle errors during the DataFrame creation
            print(f"Error loading data into DataFrame: {e}")
            return pd.DataFrame(columns=usecols if usecols else None)
        
        return df
    
    def segment_signal_with_timestamps(self, signal, timestamps, segment_length, to_discard):
        """
        Segments a signal and its corresponding timestamps into fixed-length segments.
        
        Parameters:
            signal (list or np.ndarray): The input signal array.
            timestamps (list or np.ndarray): The timestamps corresponding to the signal.
            segment_length (int): The length of each segment.
            to_discard (int): A length of signal to be discarded from begining and end.
        
        Returns:
            list of tuple: A list of tuples where each tuple contains a segment and its timestamp.
        """
        # Convert signal and timestamps to numpy arrays if they aren't already
        signal = np.array(signal)[to_discard:-to_discard]
        timestamps = np.array(timestamps)[to_discard:-to_discard]
        
        # Calculate the number of complete segments
        num_segments = len(signal) // segment_length
        
        # Create the segments and calculate timestamps
        segments = []
        for i in range(num_segments):
            segment = signal[i * segment_length:(i + 1) * segment_length]
            segment_timestamps = timestamps[i * segment_length:(i + 1) * segment_length]
            segment_time = segment_timestamps[0]  # Start time of the segment
            segments.append((segment, segment_time))
        
        return segments


    def _execute(
        self,
        inputs: List[Any],
    ) -> str:
        
        user_id = inputs[0].strip()
        date = inputs[1].strip()
        file_name = date + '_Data.csv'
        full_dir = os.path.join(
            self.local_dir, user_id
        )

        # Load data using _get_data method
        df = self._get_data(
            local_dir=full_dir,
            file_name=file_name,
            usecols=self.columns_to_keep
            )
        
        if df.empty or self.columns_to_keep[0] not in df.columns or self.columns_to_keep[1] not in df.columns:
            return "Data could not be loaded or necessary columns are missing!"


        sampling_rate = 20 # Hz
        segments_length_sec = 60 # seconds
        to_discard_sec = 30 # seconds
        to_discard_samples = to_discard_sec * sampling_rate

        # Set the desired window length for HR extraction (in seconds)
        window_length_sec = 30 # seconds
        peak_detection_method = 'nk'


        sig = df[self.columns_to_keep[0]].values
        timestamps = df[self.columns_to_keep[1]].values

        segment_length = segments_length_sec*sampling_rate
        segments = self.segment_signal_with_timestamps(sig, timestamps, segment_length, to_discard_samples)
        
        hr_data = []
        for segment_signal, segment_timestamp in segments:
            # Call the end-to-end function
            hrv_data = e2e_hrv_extraction(segment_signal, sampling_rate, window_length_sec, peak_detection_method)

            if hrv_data is not None:
                hr = hrv_data['HR'].mean()

                hr_data.append({'Timestamp': segment_timestamp, 'HR': hr})

        if hr_data:
            return pd.DataFrame(hr_data).to_json(orient="records")
            
        else:
            return 'The signal is too noisy and heart rate cannot be extracted reliably!'
