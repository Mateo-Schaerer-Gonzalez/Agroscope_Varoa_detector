import sys
import os

# Ensure root of the project is in Python path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from classes.detector import Detector
from utils.tools import get_frames, convert_yolo_to_coords
from classes.MiteManager import MiteManager
from classes.PlotterModular import Plotter  # Use backwards compatible import
from utils.tools import read_counter, reset_counter, write_counter



def _create_reanalysis_directory(results_base):
    """Create a new reanalysis directory with incremental naming."""
    i = 1
    while True:
        reanalyze_path = os.path.join(results_base, f"reanalysis{i}")
        if not os.path.exists(reanalyze_path):
            os.makedirs(reanalyze_path)
            print(f"reanalysis{i} created...")
            return reanalyze_path
        i += 1


def _process_single_recording(detector, frames, num_per_plate, name, ground_truth, 
                            results_folder, discobox_run, recording_number):
    """Process a single recording and generate its plots and data."""
    # Guard clause: Check if frames exist (frames should be a single numpy stack here)
    if frames is None or len(frames) == 0:
        raise ValueError("No frames provided for processing")
    
    os.makedirs(results_folder, exist_ok=True)
    
    # Run detection
    detector.run_detection(frames[0])
    
    # Create stage manager
    stage = MiteManager(
        coordinate_file=f"Zoning/coordinates{num_per_plate}.txt",
        mites_detection=detector.result,
        frames=frames,
        name=name
    )
    
    stage.update_mite_status(ground_truth)
    stage.save_data(recording_count=recording_number)
    
    # Create plotter and generate outputs
    plotter = Plotter(
        stage=stage,
        output_folder=results_folder,
        discobox_run=discobox_run
    )
    
    plotter.save_frame0_detection(frames[0], thickness=2)
    plotter.make_survival_graph(recording_number=recording_number)
    plotter.create_recording_pdf(recording_count=recording_number)
    
    stage.save()
    return plotter, stage


def _generate_summary_reports(plotter, stage):
    """Generate summary reports and plots."""
    plotter.make_survival_time_graph()
    plotter.plot_variability_by_mite()
    plotter.excel_summary_mites()
    plotter.excel_summary_recordings()
    stage.reset()


def reanalyze_recording(results_base, num_per_plate, detector, frames_by_recording, 
                       discobox_run, name, ground_truth):
    """Reanalyze recordings and generate comprehensive reports."""
    # Guard clauses - frames_by_recording is a list of numpy stacks
    if not frames_by_recording or len(frames_by_recording) == 0:
        raise ValueError("No recordings provided for reanalysis")
    
    if not detector:
        raise ValueError("Detector not provided")
    
    reanalyze_path = _create_reanalysis_directory(results_base)
    
    plotter = None
    stage = None
    
    # Process each recording
    for i, frames in enumerate(frames_by_recording):
        recording_number = i + 1
        results_folder = os.path.join(reanalyze_path, f"recording{recording_number}")
        
        plotter, stage = _process_single_recording(
            detector, frames, num_per_plate, name, ground_truth,
            results_folder, discobox_run, recording_number
        )
    
    # Generate summary reports if we processed any recordings
    if plotter and stage:
        _generate_summary_reports(plotter, stage)

   


def analyze_recording(results_base, num_per_plate, detector, frames, discobox_run, 
                     name, num_recordings, ground_truth, count, time_between_recording):
    """Analyze a single recording session."""
    # Guard clauses - frames is a single numpy stack
    if frames is None or len(frames) == 0:
        raise ValueError("No frames provided for analysis")
    
    if not detector:
        raise ValueError("Detector not provided")
    
    if count <= 0:
        raise ValueError("Count must be greater than 0")

    results_folder = os.path.join(results_base, "results", f"recording{count}")
    
    plotter, stage = _process_single_recording(
        detector, frames, num_per_plate, name, ground_truth,
        results_folder, discobox_run, count
    )
    
    # Update plotter with time between recordings
    plotter.time_between_recording = time_between_recording

    # Generate summary reports if this is the final recording
    if count >= num_recordings:
        _generate_summary_reports(plotter, stage)


def _determine_results_base(folder_path, discobox_run, output_folder=None):
    """Determine the base path for results."""
    if output_folder:
        return output_folder
    return folder_path if discobox_run else "outputs"


def _validate_predict_inputs(folder_path, name, num_per_plate):
    """Validate inputs for predict function."""
    if not folder_path:
        raise ValueError("Folder path must be provided")
    
    if not name:
        raise ValueError("Name must be provided")

def predict(folder_path, name, num_per_plate, reanalyze=False, discobox_run=False, 
           num_recordings=2, count=2, time_between_rec=1, output_folder=None):
    """Main prediction function that orchestrates the analysis process."""
    # Guard clauses
    _validate_predict_inputs(folder_path, name, num_per_plate)
    
    try:
        detector = Detector()
        frames = get_frames(folder_path, discobox_run, reanalyze)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize detector or load frames: {e}")
    
    # Guard clause for frames - can be either a single stack or list of stacks
    if frames is None:
        raise ValueError("No frames were loaded from the specified folder")
    
    # For reanalyze: frames is a list of stacks, for analyze: frames is a single stack
    if reanalyze and (not isinstance(frames, list) or len(frames) == 0):
        raise ValueError("No frame stacks were loaded for reanalysis")
    elif not reanalyze and len(frames) == 0:
        raise ValueError("No frames were loaded for analysis")
    
    ground_truth = ""  # alive or dead
    results_base = _determine_results_base(folder_path, discobox_run, output_folder)
    
    if reanalyze:
        reanalyze_recording(results_base, num_per_plate, detector, frames, 
                          discobox_run, name, ground_truth)
    else:
        analyze_recording(results_base, num_per_plate, detector, frames, discobox_run, 
                        name, num_recordings, ground_truth, count, time_between_rec)

    

if __name__ == "__main__":
    # Example usage - this will only run when script is executed directly
    # Uncomment the line below to run a test analysis
    # predict("Datasets/long_run_test_final/", "test", num_per_plate=1, reanalyze=True)
    print("Varroa Detector - Use the GUI application (launch_gui.py) for interactive analysis")