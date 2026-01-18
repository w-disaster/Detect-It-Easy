import subprocess
import os
import json
from pathlib import Path
from tqdm import tqdm 
from multiprocessing import Pool
import pickle


def get_filenames(base_path: Path) -> list[Path]:
    datasets = os.listdir(base_path)
    bin_filenames: list[Path] = []
    for dataset in datasets:
        families = os.listdir(base_path / dataset)
        for family in families:
            bin_filenames.extend([base_path / dataset / family / f for f in os.listdir(base_path / dataset / family)])
    print(f"{len(bin_filenames)} PE listed.")
    return bin_filenames

def dump_data(data: any):
    output_filename = os.getenv("DIEC_RESULTS_FILENAME")
    if output_filename:
        with open(output_filename, "wb") as f:
            pickle.dump(data, f)

def run_single_diec(filename: Path):
    result = subprocess.run(
        ["/usr/bin/diec", "-d", "-j", str(filename)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False
    )

    try:
        result_as_j = json.loads(result.stdout)
        packers = [result["name"] for result in result_as_j["detects"] if "type" in result and result["type"] == "Packer"]
        protectors =  [result["name"] for result in result_as_j["detects"] if "type" in result and result["type"] == "Protector"]
    except:
        packers, protectors = [], []
    return (filename, packers, protectors)

def run_diec(bin_filenames: list[Path]):
    n_proc = os.getenv("N_PROC")
    with Pool(int(n_proc) if n_proc else 60) as pool:
        results = list(
            tqdm(
                pool.imap(run_single_diec, bin_filenames),
                total=len(bin_filenames)
            )
        )
    return results



if __name__ == "__main__":
        
    base_path: str = os.getenv("BASE_BIN_DIR")
    if base_path:
        # Get absolute paths of the binaries
        bin_filenames: list[Path] = get_filenames(Path(base_path))
        # Run diec
        diec_results = run_diec(bin_filenames)
        # Save results
        dump_data(diec_results)
    else:
        print("No path specified. Exiting...")